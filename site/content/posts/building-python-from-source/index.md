---
title: building python from source
date: '2019-01-03T00:00:00+00:00'
lastmod: '2019-01-03T00:00:00+00:00'
slug: building-python-from-source
categories: []
tags: []
draft: false
---
prepare installing packages (assuming Ubuntu environment)

```generic
$ sudo apt install build-essential
$ sudo apt install libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev
$ sudo apt install libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev libffi-dev tk-dev
```

download and installing python source

```generic
$ tar -xf Python-src.tar.xz
$ cd Python-??
$ ./configure --enable-optimizations
$ make -j 8
$ sudo make altinstall
```

`altinstall` is recommended in order to avoid messing up the existing python executable.
