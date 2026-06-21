---
title: specifying which gpu to use in tensorflow script
date: '2019-03-18T00:00:00+00:00'
lastmod: '2019-03-18T00:00:00+00:00'
slug: specifying-which-gpu-to-use-in-tensorflow-script
categories:
- machine-learning
tags:
- gpu-select
draft: false
---
```python
import os

os.environ\["CUDA\_DEVICE\_ORDER"\] = "PCI\_BUS\_ID"
os.environ\["CUDA\_VISIBLE\_DEVICES"\] = "2"
```
