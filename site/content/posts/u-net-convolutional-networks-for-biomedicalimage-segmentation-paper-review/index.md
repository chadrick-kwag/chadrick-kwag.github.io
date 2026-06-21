---
title: '"U-Net: Convolutional Networks for BiomedicalImage Segmentation" paper review'
date: '2020-08-18T00:00:00+00:00'
lastmod: '2020-08-18T00:00:00+00:00'
slug: u-net-convolutional-networks-for-biomedicalimage-segmentation-paper-review
categories: []
tags:
- paper-review
- unet
draft: false
---
arxiv [link](https://arxiv.org/pdf/1505.04597.pdf)

key points

- paper does not mention how upsampling is done. deconv? interpolation? or it just maybe an alias for ‘interpolation’…
- during downsampling path, it does not do any padding.
- when concatenating downsampling result and upsampling result, the downsampling result has bigger width and height and thus the downsampling result is required to crop from center to be able to concatenate with upsampling result.
