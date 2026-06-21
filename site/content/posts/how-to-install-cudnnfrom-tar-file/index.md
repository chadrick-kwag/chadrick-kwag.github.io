---
title: how to install cudnn(from tar file)
date: '2019-09-17T00:00:00+00:00'
lastmod: '2019-09-17T00:00:00+00:00'
slug: how-to-install-cudnnfrom-tar-file
categories: []
tags:
- cudnn
- install
draft: false
---
from [nvidia docs](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html)

### [2.3.1. Installing from a Tar File](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html#installlinux-tar)

1. Navigate to your  directory containing the cuDNN Tar file.
2. Unzip the cuDNN package. $ tar -xzvf cudnn-9.0-linux-x64-v7.tgz
3. Copy the following files into the CUDA Toolkit directory, and change the file permissions. $ sudo cp cuda/include/cudnn.h /usr/local/cuda/include $ sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64 $ sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*

I prefer installing from tar file instead of deb file since tar file installation allows users to directly manipulate where the file copy will be applied to. This is something to be careful incase there are multiple CUDA installations unser `/usr/local`
