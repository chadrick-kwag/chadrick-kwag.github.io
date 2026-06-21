---
title: calculating gradient for selected tensors in pytorch
date: '2020-07-13T00:00:00+00:00'
lastmod: '2020-07-13T00:00:00+00:00'
slug: calculating-gradient-for-selected-tensors-in-pytorch
categories:
- machine-learning
tags:
- select-gradient-calculation
draft: false
---
```python
import torch

# create test net

test\_input = torch.randn((1,3,2,2))

test\_gt = torch.ones((1,1,1,1))

conv1 = torch.nn.Conv2d(3, 2, kernel\_size=2)
conv2 = torch.nn.Conv2d(2,1, kernel\_size=1)

a = conv1(test\_input)
b = conv2(a)

loss = test\_gt - b

print(conv1.weight.grad)
print(conv2.weight.grad)

output = torch.autograd.grad(loss, \[conv2.weight, conv1.weight\])
print(output)

print(conv1.weight.grad)
print(conv2.weight.grad)

print('after manual grad update')
if conv2.weight.grad is None:
    conv2.weight.grad = output\[0\]
else:
    conv2.weight.grad += output\[0\]

print(conv2.weight.grad)


```

the above is an example code of showing how to calculate gradients for a few wanted tensors. In this case, I only wanted to calculate the gradient of `conv2.weight` so that I can later on update only this weight with the amount calculated based on the the gradient produced by the loss function.
