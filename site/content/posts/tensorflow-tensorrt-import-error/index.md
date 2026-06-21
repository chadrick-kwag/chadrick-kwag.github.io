---


title: tensorflow tensorrt import error
date: '2019-03-18T00:00:00+00:00'
lastmod: '2019-03-18T00:00:00+00:00'
slug: tensorflow-tensorrt-import-error
categories:
- machine-learning
tags:
- "tensorrt"
- "tensorflow"
- "registeralreadylocked"
- "import"
draft: false
---
```generic
2019-03-18 13:01:02.751065: F tensorflow/core/framework/op.cc:55\] Non-OK-status: RegisterAlreadyLocked(op\_data\_factory) status: Already exists: Op with name \_ScopedAllocator

```

the above error shows up whenever I import tensorrt from tensorflow with the following import statement.

```generic
from tensorflow.contrib import tensorrt as tftrt
```

Environment was:

- tensorflow-gpu 1.9.0
- python 3.6.6
- ubuntu 16.04
- CUDA 9.0

## Solution

upgraded to tensorflow 1.10.0. the problem disappeared immediately.

This solution was referred in [this thread](https://github.com/tensorflow/tensorflow/issues/20139).
