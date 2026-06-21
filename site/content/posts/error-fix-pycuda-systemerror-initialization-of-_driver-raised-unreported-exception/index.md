---
title: 'error fix: pycuda "SystemError: initialization of _driver raised unreported
  exception"'
date: '2021-11-19T00:00:00+00:00'
lastmod: '2021-11-19T00:00:00+00:00'
slug: error-fix-pycuda-systemerror-initialization-of-_driver-raised-unreported-exception
categories: []
tags:
- driver
- error
- pycuda
draft: false
---
# Background

I installed pycuda with `pip install pycuda==2020.01` and it installed without any errors.

However when running the code, I got the following error.

```generic
in <module> from pycuda.\_driver import \* # noqa 
SystemError: initialization of \_driver raised unreported exception
```

appartenly importing pycuda itself was causing error.

# Fix

I removed the install pycuda.

```generic
pip uninstall pycuda
```

downloaded pycuda source files(version 2020.01) and build&installed it from source.

```generic
$ tar xzf pycuda-2020.1.tar.gz
$ cd pycuda-2020.1
$ python configure.py --cuda-root=/usr/local/cuda
$ make install
```

After doing this, the above error did not occur.
