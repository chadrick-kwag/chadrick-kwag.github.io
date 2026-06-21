---
title: installing latest nvidia driver in ubuntu
date: '2019-05-03T00:00:00+00:00'
lastmod: '2019-05-03T00:00:00+00:00'
slug: installing-latest-nvidia-driver-in-ubuntu
categories: []
tags:
- nvidia-driver
draft: false
---
sometimes when in need of upgrading the nvidia driver in ubuntu to some latest versions, the desired version is not yet available in the vanilla PPAs is ubuntu.

In my case, I needed to install nvidia driver 410 in order to work with the latest tensorflow release.

Although there is the option of manually downloading the nvidia driver installation script from the nvidia offical website, it turns out that this does not work and keeps giving me the following error.

```generic
unable to load: nvidia-installer ncurses v6 user interface
```

After some googling, I found [this thread](https://devtalk.nvidia.com/default/topic/1031213/linux/problem-installing-nvidia-390-42-driver-on-ubuntu-16-04/) which complained about the same problem that I ran into and provided with a solution

```generic
$ sudo add-apt-repository ppa:graphics-drivers/ppa
$ sudo apt update
$ sudo apt install nvidia-410
```

**However even this gets stuck halfway.** I have failed to capture the entire error message but it was about it not able to overwrite a .json file because the current nvidia driver version was using it. Here is the error message that is similar to what I got.

```generic
dpkg: error processing archive /tmp/apt-dpkg-install-AFcdAv/12-libnvidia-gl-396\_396.54-0ubuntu0~gpu18.04.1\_amd64.deb (--unpack):
trying to overwrite '/usr/share/egl/egl\_external\_platform.d/10\_nvidia\_wayland.json', which is also in package nvidia-396 396.37-0ubuntu1
```

Even `sudo apt -f install` didn’t do it. It still kept running into the same problem. Out of frustration I rebooted. However, now I got into the login loop which was cause by the display manager not able to utilize the gpu properly because the nvidia driver is now broken.

I entered the console mode with `Ctrl+Alt+F3' and this time, did apt fix install by forcing any overwrites with the following command:

```generic
$ sudo apt install -f -o Dpkg::Options::="--force-overwrite" install
```

Now with this command, it will overwrite any files thus it doesn’t get stuck like in the previous attempts. And fortunately the installation completed without any errors. Rebooted and now I have the latest 410 version driver working.

## TL;DR

do the following

```generic
$ sudo add-apt-repository ppa:graphics-drivers/ppa
$ sudo apt update
$ sudo apt install nvidia-410

(optional)
$ sudo apt install -f -o Dpkg::Options::="--force-overwrite" install
```

Another interesting thought: I found was a possible approach to make the NVIDIA’s official `.run` installation script to work. After the fuss I went through above, I found a thread that suggested that the reason why `.run` installation script kept giving out installation failed error was due to fact that the display manager was using the current driver and the installation requires that there are no programs that are using the current driver version.

Thus the suggested approach was to move to console mode, stop the display manager service and then execute the `.run` script. I haven’t tried it but I believe it is very promising since, in theory it would allow me to have avoided the problem I faced above.
