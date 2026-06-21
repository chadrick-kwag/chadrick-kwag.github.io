---
title: Properly setting dataloader and callback for validation in pytorch DDP
date: '2022-07-05T00:00:00+00:00'
lastmod: '2022-07-05T00:00:00+00:00'
slug: properly-setting-dataloader-and-callback-for-validation-in-pytorch-ddp
categories:
- machine-learning
tags:
- callback
- dataloader
- ddp
- pytorch
- validation
draft: false
---
pytorch distributed data parallel(DDP) is very useful and relatively well provided for creating a distributed training setup. However, the provided documentations and tutorial are mostly about “training” part and didn’t talk much about validation callbacks that run during training.

It is easy to think just using `DistributedSampler` for the validation dataloader would do all the work for you like it did in training dataloader, but it doesn’t. There are two main problems.

## problem 1: data padding is done by default

looking in to the [source code](https://pytorch.org/docs/stable/_modules/torch/utils/data/distributed.html#DistributedSampler) of `DistributedSampler`, we can see that when the len(dataset) is not cleanly divisable by `num_replicas` (equal to world size), it extends the indices by reiterating it from the start until the extended indices list is divisible.

Perhaps this is okay for training, but for validation it isn’t, unless you don’t mind a few “repeated” samples affecting the overall validation metric.

This automatic data padding can be avoided by implementing a custom Sampler which doesn’t do this. [Here](https://github.com/SeungjunNah/DeepDeblur-PyTorch/blob/master/src/data/sampler.py) is a custom sampler implementation that does exactly this. Use this instead of `DistributedSampler` and you can force the sampler to not add padding data.

## problem 2: length of dataloader mismatch across ranks

Let’s assume that we have solved problem1 by using the suggested custom Sampler.

In this case, we confront the second problem when the length of the dataset is not divisible by world size, which unfortunately would be most likely in most cases.

For example, say a valid dataset has 5 samples, and we use world_size=2(two gpus), and a batch size of 2 for dataloader.

A dataloader will be created for each rank, and at one step it will consume 2 samples.

In this case, rank0 dataloader will iterate twice, thereby consuming 3 samples(indices 0,2,4). The rank1 dataloader will iterate only once, thereby consuming 2 samples(indices 1,3).

If we gather validation metric results in each rank to rank0 at each dataloader step, the unequal total step size of each rank’s dataloader is going to be a problem. Because of this, it would not be wise to use collective operation at each dataloader step to sync a batch of validation metrics across all ranks, because it could cause a hang at the very last step of rank0 dataloader while other ranks' dataloaders are already finished.

So instead, I decided to use point-to-point communication between ranks to send validation metrics to rank0 at each dataloader step.

Here is the part of callback code for this feature

import torch  
import torch.distributed as dist  
​  
​  
class Callback:  
   def __init__(self, dataloader, rank, world_size):  
       self.dataloader = dataloader  
       self.rank = rank  
       self.world_size = world_size  
​  
   def ddp_iterate_unfinished_recv(  
       self, other_rank_finished_dict, device, metric_list  
  ):  
       """  
      iterate through other ranks, and if receiving data from other rank is not finished, attempt receiving  
      """  
​  
       batch_size = self.dataloader.batch_size  
​  
       for other_rank, finished in other_rank_finished_dict.items():  
           if not finished:  
               other_metric_list_tensor = torch.zeros(  
                  (batch_size,), dtype=torch.float32  
              ).to(device)  
               other_batch_size_tensor = torch.zeros((1,), dtype=torch.int).to(device)  
               other_finished_tensor = torch.zeros((1,), dtype=torch.bool).to(device)  
​  
               dist.recv(other_metric_list_tensor, other_rank, tag=1)  
               dist.recv(other_batch_size_tensor, other_rank, tag=2)  
               dist.recv(other_finished_tensor, other_rank, tag=3)  
​  
               if other_finished_tensor == True:  
                   other_rank_finished_dict[other_rank] = True  
               else:  
                   other_batch_size = other_batch_size_tensor[0].item()  
                   valid_metric_list = other_metric_list_tensor[  
                      :other_batch_size  
                  ].tolist()  
​  
                   if valid_metric_list:  
                       metric_list.extend(valid_metric_list)  
​  
   def __call__(self, global_step):  
​  
       self.model.eval()  
​  
       # gathering metric for each sample  
       metric_list = []  
​  
       # prepare other rank finished dict  
       other_rank_finished_dict = {}  
       other_ranks = list(range(1, self.world_size))  # no need to at 0 (rank0)  
       for r in other_ranks:  
           other_rank_finished_dict[r] = False  
​  
       device = torch.device(f"cuda:{self.rank}")  
​  
       # print(“start iterating dataloader”)  
​  
       for data in self.dataloader:  
​  
           with torch.no_grad():  
               net_output = self.model(**data)  
​  
           # calculate metric for each sample  
           _metric_list = self.calculate_metric_batch(net_output, data)  
​  
           if self.trainer.rank != 0:  
               # for non 0 ranks, send data to rank0  
               batch_size = self.dataloader.batch_size  
​  
               original_length = len(_metric_list)  
​  
               # if metric_list’s batch size is smaller than expected batch size, then fill in dummy values to match expected batch size  
               if len(_metric_list) < batch_size:  
                   new_metric_list = [0.0] * batch_size  
                   new_metric_list[: len(_metric_list)] = _metric_list  
                   _metric_list = new_metric_list  
​  
               # send data to rank 0  
               _metric_list_tensor = torch.FloatTensor(_metric_list).to(device)  
               batch_size_tensor = torch.IntTensor([original_length]).to(device)  
               finished_tensor = torch.BoolTensor([False]).to(device)  
​  
               dist.send(_metric_list_tensor, 0, tag=1)  
               dist.send(batch_size_tensor, 0, tag=2)  
               dist.send(finished_tensor, 0, tag=3)  
​  
           else:  
               # rank0. calculated locally so simply extend to overall metric list  
               metric_list.extend(_metric_list)  
               self.ddp_iterate_unfinished_recv(  
                   other_rank_finished_dict, device, metric_list  
              )  
​  
       # handle any unfinished recv only in rank0  
       if self.trainer.rank == 0:  
           while True:  
               no_need = all(other_rank_finished_dict.values())  
               if not no_need:  
                   self.ddp_iterate_unfinished_recv(  
                       other_rank_finished_dict, device, metric_list  
                  )  
               else:  
                   break  
       else:  
           # for non-0 ranks, send termination signal to rank0  
           _metric_list_tensor = torch.FloatTensor([0.0] * batch_size).to(device)  
           batch_size_tensor = torch.IntTensor([0]).to(device)  
           finished_tensor = torch.BoolTensor([True]).to(device)  
​  
           dist.send(_metric_list_tensor, 0, tag=1)  
           dist.send(batch_size_tensor, 0, tag=2)  
           dist.send(finished_tensor, 0, tag=3)

       torch.distributed.barrier()  
​  
       if self.rank == 0:  
​  
           average_metric = sum(metric_list) / len(metric_list)  
​  
           print(f"» average metric: {average_metric}")  
​

Of course, there is another way: calculate overall validation metric across local data in each rank and then send it to rank0 after the dataloader is completely finished. Then rank0 will recalculate the overall validation metric considering the number of samples processed and local average metrics sent from other ranks. In this scenario, collective operation is a feasible option.

Another solution would be to simply run the entire validation callback only at rank0, while other ranks will be idle or move on to the next training step.
