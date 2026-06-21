---


title: downgrading cudnn version to match CUDA version
date: '2019-06-23T00:00:00+00:00'
lastmod: '2019-06-23T00:00:00+00:00'
slug: downgrading-cudnn-version-to-match-cuda-version
categories:
- machine-learning
tags:
- "cuda"
- "cudnn"
- "version"
- "match"
draft: false
---
check current version of cudnn

```generic
$ dpkg -l | grep -i cudnn
ii  libcudnn7                                                        7.5.1.10-1+cuda10.0                          amd64        cuDNN runtime libraries
ii  libcudnn7-dev                                                    7.5.1.10-1+cuda10.0                          amd64        cuDNN development libraries and headers
```

my current gpu uses CUDA10.0 which can be verified from `nvidia-smi`

```generic
$ nvidia-smi<br>
Sun Jun 23 21:13:55 2019       <br>
+-----------------------------------------------------------------------------+<br>
| NVIDIA-SMI 410.104      Driver Version: 410.104      CUDA Version: 10.0     |<br>
|-------------------------------+----------------------+----------------------+<br>
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |<br>
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |<br>
|===============================+======================+======================|<br>
|   0  GeForce GTX 960M    Off  | 00000000:02:00.0 Off |                  N/A |<br>
| N/A   66C    P0    N/A /  N/A |   3974MiB /  4046MiB |     98%      Default |<br>
+-------------------------------+----------------------+----------------------+
```

The current version of cudnn is meant for CUDA10.1.
It seems that this somehow creates a conflict and I cannot load and run my model in tensorflow-gpu 1.13.1.

In order to fix this, I had to downgrade my current cudnn installation version to a version that is compatible with CUDA 10.0

Search for available version of `libcudnn7` package.

```generic
$ sudo apt-cache policy libcudnn7
libcudnn7:
  Installed: 7.5.1.10-1+cuda10.0
  Candidate: 7.5.1.10-1+cuda10.1
  Version table:
     7.5.1.10-1+cuda10.1 500
        500 http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86\_64  Packages
 \*\*\* 7.5.1.10-1+cuda10.0 500
        500 http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86\_64  Packages
        100 /var/lib/dpkg/status
     7.5.0.56-1+cuda10.1 500
        500 http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86\_64  Packages
     7.5.0.56-1+cuda10.0 500
        500 http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86\_64  Packages
     7.4.2.24-1+cuda10.0 500
        500 http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86\_64  Packages
     7.4.1.5-1+cuda10.0 500
        500 http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86\_64  Packages
     7.3.1.20-1+cuda10.0 500
        500 http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86\_64  Packages
     7.3.0.29-1+cuda10.0 500
        500 http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86\_64  Packages
```

There I can see `7.5.1.10-1+cuda10.0` which is cudnn 7.5.1 version that is compatible with CUDA 10.0.

To force downgrading to this specific version, use this command.

```generic
$ sudo apt install libcudnn7=7.5.1.10-1+cuda10.0
```

After this, do the same for `libcudnn7-dev` package, just to make sure.

```generic
$ sudo apt install libcudnn7-dev=7.5.1.10-1+cuda10.0
```

After doing these two, I was able to load and run my model successfully with tensorflow-gpu 1.13.1.

The changes made for two packages will be overriden in the next `apt update && apt upgrade`. To avoid this problem, the user must make `apt` to not update for these two specific packages.
