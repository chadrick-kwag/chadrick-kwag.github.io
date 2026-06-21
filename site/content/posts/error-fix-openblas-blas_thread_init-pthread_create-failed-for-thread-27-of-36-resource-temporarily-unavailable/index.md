---
title: 'error fix: "OpenBLAS blas_thread_init: pthread_create failed for thread 27
  of 36: Resource temporarily unavailable"'
date: '2020-08-04T00:00:00+00:00'
lastmod: '2020-08-04T00:00:00+00:00'
slug: error-fix-openblas-blas_thread_init-pthread_create-failed-for-thread-27-of-36-resource-temporarily-unavailable
categories: []
tags: []
draft: false
---
## Problem

When I tried to run a python script using numpy, it gave the following error.

```generic
$ python t3\_batch.py
OpenBLAS blas\_thread\_init: pthread\_create failed for thread 27 of 36: Resource temporarily unavailable
OpenBLAS blas\_thread\_init: RLIMIT\_NPROC 514120 current, 514120 max
OpenBLAS blas\_thread\_init: pthread\_create failed for thread 28 of 36: Resource temporarily unavailable
OpenBLAS blas\_thread\_init: RLIMIT\_NPROC 514120 current, 514120 max
OpenBLAS blas\_thread\_init: pthread\_create failed for thread 29 of 36: Resource temporarily unavailable
OpenBLAS blas\_thread\_init: RLIMIT\_NPROC 514120 current, 514120 max
OpenBLAS blas\_thread\_init: pthread\_create failed for thread 30 of 36: Resource temporarily unavailable
OpenBLAS blas\_thread\_init: RLIMIT\_NPROC 514120 current, 514120 max
OpenBLAS blas\_thread\_init: pthread\_create failed for thread 31 of 36: Resource temporarily unavailable
OpenBLAS blas\_thread\_init: RLIMIT\_NPROC 514120 current, 514120 max
OpenBLAS blas\_thread\_init: pthread\_create failed for thread 32 of 36: Resource temporarily unavailable
OpenBLAS blas\_thread\_init: RLIMIT\_NPROC 514120 current, 514120 max
```

## Solution

found a solution from [here](https://github.com/xianyi/OpenBLAS/issues/1668#issuecomment-402728065)

from the shell, execute the following

```generic
export OMP\_NUM\_THREADS=1
export USE\_SIMPLE\_THREADED\_LEVEL3= 1
```
