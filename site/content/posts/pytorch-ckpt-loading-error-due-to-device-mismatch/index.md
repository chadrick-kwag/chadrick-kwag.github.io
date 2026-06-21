---


title: pytorch ckpt loading error due to device mismatch
date: '2020-04-17T00:00:00+00:00'
lastmod: '2020-04-17T00:00:00+00:00'
slug: pytorch-ckpt-loading-error-due-to-device-mismatch
categories:
- machine-learning
tags:
- "pytorch"
- "pytorch-load-error"
- "torch-load-error"
- "ckpt"
- "due"
draft: false
---
# Problem

I have trained and saved model checkpoint which was train in GPU 1. However, when I try to load the checkpoint in GPU 0, it fails.

The following is my ckpt loading code:

```generic
net = Net()
net.load\_state\_dict(torch.load(ckpt\_path))

net.cuda(device) # device = GPU0
```

this gives me the following error:

```generic
Traceback (most recent call last):
  File "train.py", line 127, in <module>
    net.load\_state\_dict(torch.load(ckpt\_path))
  File "/data/chadrick/venv/tf113/lib/python3.7/site-packages/torch/serialization.py", line 529, in load
    return \_legacy\_load(opened\_file, map\_location, pickle\_module, \*\*pickle\_load\_args)
  File "/data/chadrick/venv/tf113/lib/python3.7/site-packages/torch/serialization.py", line 702, in \_legacy\_load
    result = unpickler.load()
  File "/data/chadrick/venv/tf113/lib/python3.7/site-packages/torch/serialization.py", line 665, in persistent\_load
    deserialized\_objects\[root\_key\] = restore\_location(obj, location)
  File "/data/chadrick/venv/tf113/lib/python3.7/site-packages/torch/serialization.py", line 156, in default\_restore\_location
    result = fn(storage, location)
  File "/data/chadrick/venv/tf113/lib/python3.7/site-packages/torch/serialization.py", line 136, in \_cuda\_deserialize
    return storage\_type(obj.size())
  File "/data/chadrick/venv/tf113/lib/python3.7/site-packages/torch/cuda/\_\_init\_\_.py", line 480, in \_lazy\_new
    return super(\_CudaBase, cls).\_\_new\_\_(cls, \*args, \*\*kwargs)
RuntimeError: CUDA error: out of memory
```

# Solution

when loading ckpt data, ensure that device is mapped from some GPU to CPU. The fixed loading code is like this:

```generic
net = Net()
load\_data = torch.load(ckpt\_path, map\_location='cpu')
net.load\_state\_dict(load\_data)

net.cuda(device)
```

the problematic behavior described above is also explained in the [official docs.](https://pytorch.org/docs/stable/torch.html#torch.load)
