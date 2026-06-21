---
title: 'paper review: "Semantic Segmentation using Adversarial Networks"'
date: '2021-03-08T00:00:00+00:00'
lastmod: '2021-03-08T00:00:00+00:00'
slug: paper-review-semantic-segmentation-using-adversarial-networks
categories:
- paper-review
tags:
- adversarial
- adversarial-training
- segmentation
draft: false
---
<https://arxiv.org/pdf/1611.08408.pdf>

## key point

use adversarial net to distinguish if input masks are from segmentation net or ground truth.

---

![](images/1.png)

this allows to add auxiliary loss, like below:

![](images/2.png)

where

- mce: multi class cross-entropy
- bce: binary cross entropy
- s(): segmentation network
- a(): adversarial network
- y: ground truth
- x: input
- s(x): segmentation network output for given input

however, the paper gives a confusing explanation of how the above loss function can achieve both segmentation network and adversarial network optimization.

The paper states the following loss is the target function for improving adversarial network.

![](images/3.png)

And the following is target function for improving segmentation network.

![](images/4.png)

the first term is a normal loss function for segmentation network. The intention of the second term is to disturb adversarial network to predict segmentation output as segmentation output.

However, adding the loss for adversarial network and loss for segmentation network doesn’t exactly match to the overall loss stated above.

When using the segmentation network output as input of adversarial network, the original image should be masked by each class segmentation network output. This can be depicted as following:

![](images/5.png)

Using this approach, the authors show that by applying adversarial learning to semantic segmentation, it gained some regularizing effect.

![](images/6.png)

Here, we can see that by applying adversarial training, the trained model is less likely to overfit (left figure) and able to be more generalized (right figure).

Below is an example comparison of adversarial training.

![](images/7-1.png)
