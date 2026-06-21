---
title: check cuda version build to torch package and find cudnn version used in torch
date: '2020-08-06T00:00:00+00:00'
lastmod: '2020-08-06T00:00:00+00:00'
slug: check-cuda-version-build-to-torch-package-and-find-cudnn-version-used-in-torch
categories:
- machine-learning
tags:
- cuda-version
- cudnn-version
- torch
draft: false
---
use the following python snippet to check cuda version the torch package was built against

```generic
import torch
print(torch.version.cuda)
```

use the following python snippet to check cudnn version used by torch

```generic
import torch
print(torch.backends.cudnn.version())
```
