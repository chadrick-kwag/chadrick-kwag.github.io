---
title: forcing memory release of gpu
date: '2018-12-05T00:00:00+00:00'
lastmod: '2018-12-05T00:00:00+00:00'
slug: forcing-memory-release-of-gpu
categories: []
tags:
- gpu-memeory-release
draft: false
---
identifying which pid is occupying the gpu can be found following this [thread](https://stackoverflow.com/questions/15197286/how-can-i-flush-gpu-memory-using-cuda-physical-reset-is-unavailable).

However, the gpu number in the above link is not identical with the gpu number displayed with `nvidia-smi`.

In my case, the processes that were occupying the gpu memory did not show up in `nvidia-smi` but it showed up with `fuser`. Since the numbering of gpu of the two does not match, I had to manually cross-check to find out which pid I needed to kill.
