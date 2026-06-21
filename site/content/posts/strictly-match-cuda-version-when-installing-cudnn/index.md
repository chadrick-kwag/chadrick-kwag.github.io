---
title: strictly match cuda version when installing cudnn
date: '2019-07-07T00:00:00+00:00'
lastmod: '2019-07-07T00:00:00+00:00'
slug: strictly-match-cuda-version-when-installing-cudnn
categories:
- machine-learning
tags: []
draft: false
---
I was naive to think that a cudnn version built for CUDA 10.1 will work with CUDA 10.0 installed in my machine. This mismatch will not produce any explicit error messages when building and training a tensorflow model. However, I notices that the loss does not reduce even after a noticable amount of steps and epochs.

When I replaced my cudnn to a version that was targeted to CUDA 10.0, and reran the training session, the loss does significantly reduce at the beginning.
