---
title: finding out package and versions in apt
date: '2020-08-06T00:00:00+00:00'
lastmod: '2020-08-06T00:00:00+00:00'
slug: finding-out-package-and-versions-in-apt
categories:
- linux
tags:
- apt
- package
- version
draft: false
---
search available packages with keyword

```generic
$ apt-cache search <keyword>
```

list available versions of a package. For example, if I want to list all available versions for package libcudnn7

```generic
$ apt list -a libcudnn7
```

Before running this, running `apt update` is recommended.

After finding a specific version that I want to install, then install the packge with a specific version like this

```generic
$ apt install libcudnn7=7.6.5.32-1+cuda10.1
```
