---
title: EfficientDet paper review
date: '2020-06-06T00:00:00+00:00'
lastmod: '2020-06-06T00:00:00+00:00'
slug: efficientdet-paper-review
categories:
- paper-review
tags:
- efficientdet
- paper-review
draft: false
---
paper link: <https://arxiv.org/pdf/1911.09070.pdf>

## BiFPN

multiple bifpn layers for scaling

use depth-wise convolution layers

bidirectional cross-scale connections + weighted feature fusion.

## weighted feature fusion

- different weight for each resolution features
- learnable weights

summarize that there are three different approaches for doing weighted feature fusion

- unbounded fusion: because it is unbounded, can cause training instability
- softmax-based fusion: better than unbounded fusion, since it normalizes the weights thus removing training instability. But through experiments, found that it is very slow.
- fast normalized fusion: much faster than softmax fusion

experiments show that this give similar performance to softmax while much faster.

## efficient det

- bifpn + optimized backbone
- one stage detector paradigm
- use EfficientNet as backbone
- multiple bifpn layers
- on the final stage, each layer features are fed to box/class networks.
- box/class network weights are shared

## compound scaling

if the user wants to scale efficientdet, then it should scale the network width, depth, input resolution all together based on scale coefficient.  
jointly scaling.

- bifpn network: width and depth scaling
- box/class prediction network: width fixed to match bifpn network. linearly increase depth
- input image resolution: linearly increase

## ablation study

both bifpn and backbone is crucial

bifpn uses depth-wise conv layers

## comments

paper doesn’t mention about box/class network specifics. just mention that it does use anchors.
