---
title: tensorflow manual cross entropy loss calculation
date: '2020-06-12T00:00:00+00:00'
lastmod: '2020-06-12T00:00:00+00:00'
slug: tensorflow-manual-cross-entropy-loss-calculation
categories: []
tags:
- cross-entropy-loss
draft: false
---
In case you need a raw cross entropy loss calculation done not with logits but with the final value, and no reductions on the output whatsoever, here’s a code snippet for it.

```python
def ce\_loss(y\_true, y\_pred):
    ce\_loss = -((1-y\_true) \* tf.log(1-y\_pred) + y\_true \* tf.log(y\_pred))
    return ce\_loss
```
