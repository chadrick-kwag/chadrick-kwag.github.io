---
title: '"SkeletonNet: Shape Pixel to Skeleton Pixel" paper review'
date: '2020-08-18T00:00:00+00:00'
lastmod: '2020-08-18T00:00:00+00:00'
slug: skeletonnet-shape-pixel-to-skeleton-pixel-paper-review
categories:
- paper-review
tags:
- paper-review
- skeletonnet
draft: false
---
arxiv [link](https://arxiv.org/ftp/arxiv/papers/1907/1907.01683.pdf)

my comments

- very similar to unet, with some modifications to network architecture:
  - during downsampling convolutions, paddings are applied so no minor dimension reductions occur. This allows downsampling results to be directly concatenated with same-level upsampling results.
  - New concept called ‘side layers’ are introduced. Each level’s output tensor which have difference shapes, will be processed to a tensor with the same width/height of the final output. This is called the side layer. Each side layers will be merged and then combined with the ‘normal’ down-upsampled output tensor to produce the final output. This will allow deep level output tensors to have a more direct relationship with the final output which can be interpreted as low-resolution tensor’s information becoming more influential.
