---
title: is it okay to calculate loss in cpu and backpropagate in torch?
date: '2021-03-03T00:00:00+00:00'
lastmod: '2021-03-03T00:00:00+00:00'
slug: is-it-okay-to-calculate-loss-in-cpu-and-backpropagate-in-torch
categories:
- machine-learning
tags:
- calculate-loss-in-cpu
- gpu-cpu
- torch
draft: false
---
When using torch, while it is common to run the network in gpu, I wasn’t always so sure if it was mandatory for me to calculate the loss on the same gpu as the output at all times. If I can do loss calculation in cpu, then it would help to reduce my gpu memory consumption.

I did a simple test and the short answer is: yes I can calculate loss in cpu.

```python
import torch # tested with torch 1.4.0

class Simplenet(torch.nn.Module):

    def \_\_init\_\_(self):
        super().\_\_init\_\_()

        self.fc1 = torch.nn.Linear(3,1)

    def forward(self, x):
        y = self.fc1(x)

        return y

device = torch.device('cuda:0')

\_input = torch.FloatTensor(\[1,2,3\]).to(device)
\_input = \_input.unsqueeze(0)

net = Simplenet()
net.to(device)

optim = torch.optim.Adam(net.parameters())

gt = torch.FloatTensor(\[0,0,0\])
gt = gt.unsqueeze(0)

for \_ in range(10):
    optim.zero\_grad()
    out = net(\_input)

    # print(out)

    # calc loss

    loss = out.cpu() - gt
    loss = loss.pow(2).sqrt()
    loss = loss.mean()

    print(f'loss: {loss.item()}')

    loss.backward()

    optim.step()

"""
here is the output:
loss: 0.4778975248336792
loss: 0.47089752554893494
loss: 0.46389755606651306
loss: 0.4568975865840912
loss: 0.44989752769470215
loss: 0.4428974688053131
loss: 0.43589749932289124
loss: 0.42889752984046936
loss: 0.4218975305557251
loss: 0.41489753127098083

"""
```

We can verify that even moving the network output tensors to cpu and then calculating loss, it still backpropagates perfectly well.

I guess this method does hurt computation speed since it is done in cpu and not in gpu. But still, if the loss calculation is complicated or memory consuming, then this solution may help user to save precious gpu memory.
