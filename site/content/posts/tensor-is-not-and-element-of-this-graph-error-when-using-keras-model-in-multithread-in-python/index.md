---
title: '`Tensor is not and element of this graph` error when using Keras model in
  multithread in python'
date: '2019-01-21T00:00:00+00:00'
lastmod: '2019-01-21T00:00:00+00:00'
slug: tensor-is-not-and-element-of-this-graph-error-when-using-keras-model-in-multithread-in-python
categories:
- machine-learning
tags: []
draft: false
---
When a python script containing a keras model, it will work fine when the script is executed without any multithreading/multiprocessing. However, once multithreading is used and a keras model needs to execute in a new thread, it will cause problems. Here is an error message that I encountered.

```python
  File "/home/ubuntu/venv/lib/python3.6/site-packages/keras/engine/training.py", line 1797, in predict
    self.\_make\_predict\_function()
  File "/home/ubuntu/venv/lib/python3.6/site-packages/keras/engine/training.py", line 1009, in \_make\_predict\_function
    \*\*kwargs)
  File "/home/ubuntu/venv/lib/python3.6/site-packages/keras/backend/tensorflow\_backend.py", line 2499, in function
    return Function(inputs, outputs, updates=updates, \*\*kwargs)
  File "/home/ubuntu/venv/lib/python3.6/site-packages/keras/backend/tensorflow\_backend.py", line 2442, in \_\_init\_\_
    with tf.control\_dependencies(self.outputs):
  File "/home/ubuntu/venv/lib/python3.6/site-packages/tensorflow/python/framework/ops.py", line 4304, in control\_dependencies
    return get\_default\_graph().control\_dependencies(control\_inputs)
  File "/home/ubuntu/venv/lib/python3.6/site-packages/tensorflow/python/framework/ops.py", line 4017, in control\_dependencies
    c = self.as\_graph\_element(c)
  File "/home/ubuntu/venv/lib/python3.6/site-packages/tensorflow/python/framework/ops.py", line 3035, in as\_graph\_element
    return self.\_as\_graph\_element\_locked(obj, allow\_tensor, allow\_operation)
  File "/home/ubuntu/venv/lib/python3.6/site-packages/tensorflow/python/framework/ops.py", line 3114, in \_as\_graph\_element\_locked
    raise ValueError("Tensor %s is not an element of this graph." % obj)
ValueError: Tensor Tensor("predictions/concat:0", shape=(?, 100, 16), dtype=float32) is not an element of this graph.

```

## Solution

after loading the weights, call `_make_predict_function` method for the model returned. Here is an example

```python
self.model.load\_weights(weight\_path)
self.model.\_make\_predict\_function()
```

after doing this, the keras model will be properly initialized even in a new thread environment and the error will disappear.
