---


title: libcupti.so import error
date: '2019-01-09T00:00:00+00:00'
lastmod: '2019-01-09T00:00:00+00:00'
slug: libcupti-so-import-error
categories:
- machine-learning
tags:
- "libcupti"
- "import"
draft: false
---
## error message

2019-01-07 13:20:29.745928: I tensorflow/stream_executor/dso_loader.cc:129] Couldn’t open CUDA library libcupti.so.8.0. LD_LIBRARY_PATH: /usr/lib/oracle/11.2/client64/lib:/usr/local/cuda-8.0/lib64:/usr/local/lib  
2019-01-07 13:20:29.745965: F ./tensorflow/stream_executor/lib/statusor.h:212] Non-OK-status: status_ status: Failed precondition: could not dlopen DSO: libcupti.so.8.0; dlerror: libcupti.so.8.0: cannot open shared object file: No such file or directory  
중지됨 (core dumped)

## solution

the error is due to missing LD_LIBRARY_PATH pointing to `/usr/local/cuda/extras/CUPTI/lib64` which holds the `libcupti.so.8.0` file.

therefore, add this path to the `LD_LIBRARY_PATH` environment variable.

$ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/extras/CUPTI/lib64

recommend adding this to `.bashrc`
