---


title: 'paper review: "EfficientNet: Rethinking Model Scaling for Convolutional Neural
  Networks"'
date: '2021-03-12T00:00:00+00:00'
lastmod: '2021-03-12T00:00:00+00:00'
slug: paper-review-efficientnet-rethinking-model-scaling-for-convolutional-neural-networks
categories:
- paper-review
tags:
- "efficientnet"
- "rethinking"
- "model"
- "scaling"
- "convolutional"
draft: false
---
arxiv: <https://arxiv.org/pdf/1905.11946.pdf>

## key point

- propose ‘compound scaling method’ which scales all width/depth/resolution together which is an efficient scaling method that can be applied to any existing structure
- introduce a new family of baseline structure called ‘EfficientNets’. The very smallest baseline structure was found by authors through NAS, and then the rest of the family are just scaled up using compound scaling method.

---

when scaling a network, it is critical to balance network width/depth/resolution.  
authors found that scaling each with constant ratio gave good results. = compount scaling method

this scaling method can be used on existing structures.  
this work propose a new baseline structure, obtained from NAS, called ‘EfficientNet’

network width: channel #  
network depth: layer #  
resolution: input size

use nas to get good baseline, efficientnet-B0.
main bulding block is mobile inverted bottlenect MBConv, added with squeeze-and-excitation.

**how to find scaling factor?**

step1: starting from baseline, do small grid search of alpha, beta, gamma.  
authors got these values.  
step2: using fixed factors, scale from baseline to create B1 ~ B7 variants.

this two step approach is done to avoid doing too much extensive grid search.

applying compount scaling to existing structures give better results than increasing one of widht/depth/resolution.

efficientnets give better performance with less parameters than existing counterparts. It also exceeds others in transfer learning benchmarks.
