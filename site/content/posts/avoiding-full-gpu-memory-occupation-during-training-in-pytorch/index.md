---


title: avoiding full gpu memory occupation during training in pytorch
date: '2020-04-21T00:00:00+00:00'
lastmod: '2020-04-21T00:00:00+00:00'
slug: avoiding-full-gpu-memory-occupation-during-training-in-pytorch
categories:
- machine-learning
tags:
- "pytorch"
- "gpu-memory-full"
- "pytorch-gpu-memory"
- "torch-gpu-memory"
- "torhc"
draft: false
---
# Problem

While training even a small model, I found that the gpu memory occupation neary reached 100%. This seemed odd and it made me to presume that my pytorch training code was not handling gpu memory management properly.

Here is a pseudo code for my pytorch training script.

```generic
net = Net().cuda()
optimizer = torch.nn.optim.Adam(net.parameters(), lr=1e-3)

for i in range(steps):

    optimizer.zero\_grad()

    batch\_input\_data, batch\_gt\_data = get\_some\_data()

    batch\_input\_tensor = torch.from\_numpy(batch\_input\_data).cuda()
    batch\_gt\_tensor = torch.from\_numpy(batch\_gt\_data).cuda()

    out = net(batch\_input\_tensor)

    loss = loss\_fn(out, batch\_gt\_tensor)

    loss.backward()

    optimizer.step()
```

With this code, not only does my gpu memory occupation reach 100%, in some cases when the batch input data becomes large(either larger batch size or if a single input data is exceptionally larger than others in case where individual input data are variant) it will fail to even get loaded to gpu memory and will fail to proceed and raise and exception.

# Solution

I assumed that finished step tensors which have been loaded to gpu memory are not being released properly. Therefore I manually added gpu memory releasing code lines to the train script and the pseudo code looks like this.

```generic
net = Net().cuda()
optimizer = torch.nn.optim.Adam(net.parameters(), lr=1e-3)

for i in range(steps):

    optimizer.zero\_grad()

    batch\_input\_data, batch\_gt\_data = get\_some\_data()

    batch\_input\_tensor = torch.from\_numpy(batch\_input\_data).cuda()
    batch\_gt\_tensor = torch.from\_numpy(batch\_gt\_data).cuda()

    # added this line
    torch.cuda.empty\_cache()

    out = net(batch\_input\_tensor)

    loss = loss\_fn(out, batch\_gt\_tensor)

    loss.backward()

    optimizer.step()
```

The intention is that when `batch_input_tensor` and `batch_gt_tensor` variable has been allocated with fresh data tensors, the old tensor which these variables held previously will be handled forcefully with the added line of code.

I’m not entirely sure if understanding is correct but this does the job. After make this change, the gpu memory occupation throughout training was on average 20%.

According to the docs, deleting the variables that hold gpu tensors will release gpu memory but simply deleting them alone didn’t release gpu memory instantly. For instant gpu memory release, deleting AND calling `torch.cuda.empty_cache()` was necessary.

In the case above, we are in a training loop and reusing `batch_input_tensor` and `batch_gt_tensor` variables. Because we are reusing the variables, I didn’t manually delete them. But if I wanted to reduce gpu memory usage further, I could update the training code like this.

```generic
net = Net().cuda()
optimizer = torch.nn.optim.Adam(net.parameters(), lr=1e-3)

for i in range(steps):

    optimizer.zero\_grad()

    batch\_input\_data, batch\_gt\_data = get\_some\_data()

    batch\_input\_tensor = torch.from\_numpy(batch\_input\_data).cuda()
    batch\_gt\_tensor = torch.from\_numpy(batch\_gt\_data).cuda()

    out = net(batch\_input\_tensor)
    loss = loss\_fn(out, batch\_gt\_tensor)

    loss.backward()

    # added lines
    del batch\_input\_data
    del batch\_gt\_data
    torch.cuda.empty\_cache()

    optimizer.step()
```

I have manually deleted `batch_input_data` and `batch_gt_data` this time, but this must be done after `loss.backward()` since this is the last line that utilizes the tensors saved in the two variables. If we delete the two variables before this line, then backprop will raise and error.

The key is to delete the variables after any related tensor operations are finished, and call `torch.cuda.empty_cache()` after deleting the variables.
