---
title: relu, gelu , swish, mish activation function comparison
date: '2022-05-25T00:00:00+00:00'
lastmod: '2022-05-25T00:00:00+00:00'
slug: relu-gelu-swish-mish-activation-function-comparison
categories:
- machine-learning
tags:
- activation-function
- gelu
- mish
- relu
- swish
draft: false
---
## RELU(2018)

arxiv: <https://arxiv.org/abs/1803.08375>

f(x) = max(0,x)

## GELU(2016)

despite introduced earlier than relu, in DL literature its popularity came after relu due to its characteristics that compensate for the drawbacks of relu.

Like relu, gelu as no upper bound and bounded below. while relu is suddenly zero in negative input ranges, gelu is much smoother in this region. It is differentiable in all ranges, and allows to have gradients(although small) in negative range.

This is advantageous to relu since relu suffers from ‘dying RELU’ problems where significant amount of neuron in the network become zero and don’t practically do anything.

## swish(2017)

arxiv: <https://arxiv.org/pdf/1710.05941v1.pdf>

f(x) = x*sigmoid(x)

graph is similar to gelu.

![](images/Screenshot-from-2022-05-26-01-17-40.png)

outperforms relu.

no comparison with gelu in paper.

## mish(2019)

arxiv: <https://arxiv.org/vc/arxiv/papers/1908/1908.08681v2.pdf>

f(x) = x*tanh(softplus(x))

graph is similar to gelu and swish.

![](images/Screenshot-from-2022-05-26-01-16-28.png)

according to the paper mish can handle more deeper layered networks than swish, and in other aspects mish is normally slightly better than swish.

![](images/Screenshot-from-2022-05-26-01-17-06.png)

But overall, mish and swish performances are nearly identical.

This work does include gelu in comparison experiments.  
interestingly, among various experiments gelu seems to outperform swish in quite a lot of experiements.
