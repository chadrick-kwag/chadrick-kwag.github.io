---
title: applying xavier normal initialization to conv/linear layer(module) in pytorch
date: '2020-04-06T00:00:00+00:00'
lastmod: '2020-04-06T00:00:00+00:00'
slug: applying-xavier-normal-initialization-to-conv-linear-layermodule-in-pytorch
categories:
- machine-learning
tags:
- glorot-initialization
- initialization
- pytorch
- xavier-initialization
draft: false
---
in tensorflow, default initialization used is glorot normal initialization which is also known as xavier normal initialization. To use the same setting in pytorch, the following practice should be done.

# 2d convolution module example

```generic
self.conv1 = torch.nn.Conv2d(3, 16, 3, padding=1)

torch.nn.init.xavier\_normal\_(self.conv1.weight)
torch.nn.init.zeros\_(self.conv1.bias)
```

# linear module example

```generic
self.linear2 = torch.nn.Linear(32,1)
torch.nn.init.xavier\_normal\_(self.linear2.weight)
torch.nn.init.zeros\_(self.linear2.bias)
```

pytorch supports other initialization functions, and one can use those initialization functions in other situations as they see fit in a similar fashion as above.
