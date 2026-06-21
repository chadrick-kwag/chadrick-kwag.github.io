---


title: 'paper review: "Fast DenseNet: Towards Efficient and Accurate Text Recognition
  with Fast Dense Networks"'
date: '2020-06-16T00:00:00+00:00'
lastmod: '2020-06-16T00:00:00+00:00'
slug: paper-review-fast-densenet-towards-efficient-and-accurate-text-recognition-with-fast-dense-networks
categories:
- paper-review
tags:
- "fast-densenet"
- "fdensenet-u"
- "fast"
- "densenet"
- "efficient"
draft: false
---
<https://arxiv.org/ftp/arxiv/papers/1912/1912.07016.pdf>

## TLDR: key points

this paper proposes to use densent+CTC for text recognition, and in that process propose some modifications to original densenet which are

- 1. new block, called Fast Dense Block(FDB)
- 2. FDenseNet-U: fast densenet + upsampling block
- 3. use convolution layer with stride 2 instead of maxpooling
- 4. apply depth-wise separable convolution

## Fast Dense Block

- combining good attributes of residual block, dense block, residual dense block.
- uses addition instead of concatenating when merging intermediate results in a single block. This helps to reduce computation. Concatenation layer is only used at the end of the block.

## FDenseNet-U

- does upsampling to compensate for possibly lost information during downsampling.
- Then pass on the result to CTC for text recognition.

## Comments

Unfortunately, since this paper was intented to target text recognition and not simple classification, there is no experiments done to compare classification performance using original densenet vs. Fast DenseNet.
