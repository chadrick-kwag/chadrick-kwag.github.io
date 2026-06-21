---
title: how to handle "no disk space" while installing cuda toolkit
date: '2021-11-18T00:00:00+00:00'
lastmod: '2021-11-18T00:00:00+00:00'
slug: how-to-handle-no-disk-space-while-installing-cuda-toolkit
categories: []
tags:
- cuda-toolkit
- no-disk-space
draft: false
---
## Background

I downloaded another CUDA toolkit(11.4) installation .sh and executed it to install it. However, while installing it was stopped due to no disk space.

The default install location is `/usr/local/cuda-11.4` and unfortunately I only had about 5GB left under `/` while I had a lot of space under `/data`.

```
Filesystem                   Size  Used Avail Use% Mounted on
devtmpfs                      32G     0   32G   0% /dev
tmpfs                         32G  4.0K   32G   1% /dev/shm
tmpfs                         32G  1.4G   31G   5% /run
tmpfs                         32G     0   32G   0% /sys/fs/cgroup
/dev/mapper/aa	              50G   40G   11G  80% /
/dev/sda2                    509M  373M  136M  74% /boot
/dev/sda1                    256M   12M  245M   5% /boot/efi

/dev/mapper/VG00-LV_data     2.0T  1.6T  507G  76% /data
```

At the early stage of installation, there is a screen where I can configure what components I would like to install and where to install it.

I disabled installing other stuff except the tool kit and set the installation location to something like `/data/user/cuda/cuda-11.4`.

However, still the installation failed with `no disk space` error.

I monitored disk space usage during installation and found that even though I set the installation path to `/data/user/cuda/cuda-11.4`, it seemed to utilize disk space under `/`.

## Solution

I created a symbolic link on `/usr/local/cuda-11.4` directing to `/data/user/cuda/cuda-11.4`. And then just executed installation with default settings.

This way, the installation was utilizing `/usr/local/cuda-11.4` but since this actually directs to storage under `/data`, I was able to avoid `no disk space` error.
