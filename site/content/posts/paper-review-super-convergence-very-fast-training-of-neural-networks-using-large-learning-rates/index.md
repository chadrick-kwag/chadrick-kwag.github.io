---
title: 'paper review: "super convergence: very fast training of neural networks using
  large learning rates"'
date: '2020-06-16T00:00:00+00:00'
lastmod: '2020-06-16T00:00:00+00:00'
slug: paper-review-super-convergence-very-fast-training-of-neural-networks-using-large-learning-rates
categories: []
tags:
- paper-review
- super-convergence
- very-fast-training-of-neural-networks-using-large-learning-rates
draft: false
---
<https://arxiv.org/pdf/1708.07120.pdf>

# key idea in one sentence

get min/max learning rate from LR range test, and run one cycle of cyclical learning rate at the start of training to efficiently train networks to find super convergence.

# Notes

> This paper uses a simplification of the second order Hessian-Free optimization to estimate optimal values for the learning rate

> In this work, we use cyclical learning rates (CLR) and the learning rate range test (LR range test)

## cyclical learning rates (CLR)

in one cycle, there are two steps: increasing lr step and decreasing lr step. ‘phase’ could be a more appropriate vocab instead of ‘step’. The changing of lr could be done linearly or in discrete jumps but the author recommends linear changes.

## LR range test

- The LR range test can be used to determine if super-convergence is possible for an architecture
- start with low lr and gradually increase lr. while increasing, the metric(e.g. accuracy) will increase but after some point, further increase in lr will not translate to increase in accuracy. The lr where metric peak appears will be the max lr in CLR. min lr will be set to 1/3 of this max lr value.

## suggested lr policy

use cycle with step size smaller than epoch’s stepsize. Run cycle only one time, where the lr at the end of the cycle if much smaller than the starting lr value of the cycle. Name this lr policy as “1 cycle”

## Comments

what exactly is “super-convergence training”?

---

why is estimating optimal lr section introduced? I mean the 1 cycle policy doesn’t require any complicated equations doesn’t it? the lr min max values are obtained from lr range test. and then just apply the 1 cycle policy.

=> okay got it. so the whole “optimal lr estimation using second hessian” is a tool to obtain estimated optimal lr. Through obtaining estimated optimal lr, I think the author wanted to somewhat theoretically back why the 1 cycle policy is superior to a fixed lr policy. High estimated optimal lr means that small hessian changes are made for same amount of param value change, which in turn implies that SGD is finding flat and wide local minima. (* not found. finding.)

hmm… but doesn’t that indicate high optimal lr = needs more training, local minima not reached? I don’t understand why “SGD is finding flat and wide local minima” is regarded as a “good state”.
