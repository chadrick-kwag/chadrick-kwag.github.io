---
title: '"ValueError: numpy.ndarray size changed, may indicate binary incompatibility."
  error fix'
date: '2021-07-21T00:00:00+00:00'
lastmod: '2021-07-21T00:00:00+00:00'
slug: valueerror-numpy-ndarray-size-changed-may-indicate-binary-incompatibility-error-fix
categories: []
tags:
- binary-incompatibility
- pycocotools
- python
draft: false
---
After installing packages with python and running a torch training script, I encountered the following error.

```generic
ValueError: numpy.ndarray size changed, may indicate binary incompatibility. Expected 88 from C header, got 80 from PyObject
```

This error occurred in `pycocotools` package which was used by `detectron2` package.

My solution was to reinstall `pycocotools` package with special options.

```generic
$ pip uninstall pycocotools
$ pip install pycocotools --no-binary :all: --no-build-isolation
```

after this fix, the above error did not appear. My environment was CentOS7, python3.9.5, x64 machine.
