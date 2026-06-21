---


title: None index in python list?
date: '2020-12-12T00:00:00+00:00'
lastmod: '2020-12-12T00:00:00+00:00'
slug: none-index-in-python-list
categories:
- python
tags:
- "indexing-none"
- "none-index"
- "none"
- "index"
- "list"
draft: false
---
while looking through some deep learning implementation code, I found some strange list indexing in python code. Here is an example.

```python
        if reference\_points.shape\[-1\] == 2:
            offset\_normalizer = torch.stack(\[input\_spatial\_shapes\[..., 1\], input\_spatial\_shapes\[..., 0\]\], -1)
            sampling\_locations = reference\_points\[:, :, None, :, None, :\] \\
                                 + sampling\_offsets / offset\_normalizer\[None, None, None, :,
```

It was using `None` as an index when indexing a python object. First I thought is this indexing `None` on a python list and tested it. But it gave me an error.

It turns out that None indexing does work under numpy arrays and also tensor objects. Here is an example showing how none indexing with a numy array works.

```python
import numpy as np

a = np.random.rand(3,2)

print(a\[None,:\].shape) # output: (1, 3, 2)
print(a\[:,None\].shape) # output: (3, 1, 2)
print(a\[:,None,:,None\].shape) # output: (3, 1, 2, 1)
print(a\[:,None,None, :\].shape) # output: (3, 1, 1, 2)

print(a\[:,None,:,:\]) # IndexError: too many indices for array: array is 2-dimensional, but 3 were indexed
```

As you can see, it practically acts as `np.expand_dims` function to add a dummy axis where I want, but in a more inline coding fashion.
