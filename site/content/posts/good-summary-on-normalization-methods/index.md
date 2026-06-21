---
title: good summary on normalization methods
date: '2020-10-14T00:00:00+00:00'
lastmod: '2020-10-14T00:00:00+00:00'
slug: good-summary-on-normalization-methods
categories: []
tags:
- normalization
draft: false
---
link: <https://towardsdatascience.com/different-normalization-layers-in-deep-learning-1a7214ff71d6>

- Batch Normalization
- Weight Normalization
- Layer Normalization
- Group Normalization
- Weight Standarization

Recently, Siyun Qiao et al. introduced Weight Standardization in their paper [“Micro-Batch Training with Batch-Channel Normalization and Weight Standardization”](https://arxiv.org/pdf/1903.10520.pdf) and found that group normalization when mixed with weight standardization, could outperform or perform equally well as BN even with batch size as small as 1.

In conclusion, Normalization layers in the model often helps to speed up and stabilize the learning process. If training with large batches isn’t an issue and if the network doesn’t have any recurrent connections, Batch Normalization could be used. For training with smaller batches or complex layer such as LSTM, GRU, Group Normalization with Weight Standardization could be tried instead of Batch Normalization.

One important thing to note is, in practice the normalization layers are used in between the Linear/Conv/RNN layer and the ReLU non-linearity(or hyperbolic tangent etc) so that when the activations reach the Non-linear activation function, the activations are equally centered around zero. This would potentially avoid the dead neurons which never get activated due to wrong random initialization and hence can improve training.
