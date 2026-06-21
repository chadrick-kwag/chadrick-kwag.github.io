---
title: loading multiple tensorflow 1.x models at once
date: '2021-04-19T00:00:00+00:00'
lastmod: '2021-04-19T00:00:00+00:00'
slug: loading-multiple-tensorflow-1-x-models-at-once
categories:
- machine-learning
tags:
- load-multiple-model
- tensorflow
draft: false
---
Loading multiple tensorflow models at once in tf1.x causes problems because the operations in each model may have same name, and thus cause collision. While this can be avoided by manually giving unique names to tensors when developing a model, this is a cumbersome strategy.

Another approach would be to save each model in a separate graph, and assign separate session to each of these graphs. By assigning a graph for each model, there is no need to worry about name collision.

I wondered if assigning multiple graphs to a single session would be possible. But I have only ran into errors and it looks like this is not possible.

These findings can be used in code like this.

```python
import tensorflow as tf, numpy as np, os

class Model1:
    def \_\_init\_\_(self, model\_arch, model\_weight):
        self.graph = tf.Graph()

        with self.graph.as\_default():
            self.sess = tf.Session(graph=self.graph)

            with self.sess.as\_default():
                with open(model\_arch, 'r') as fd:
                    self.model = tf.keras.models.model\_from\_json(fd.read())
                self.model.load\_weights(model\_weight)
    
    def predict(self, x):
        with self.graph.as\_default():
            with self.sess.as\_default():
                out = self.model.predict(x)
        
        return out

model\_arch = '/model\_arch\_json\_path'
model\_weight = '/model\_weight\_path'

os.environ\["CUDA\_DEVICE\_ORDER"\] = "PCI\_BUS\_ID"
os.environ\["CUDA\_VISIBLE\_DEVICES"\] = "1"

m1 = Model1(model\_arch, model\_weight)
m2 = Model1(model\_arch, model\_weight)

testinput = np.random.rand(1, 224,224,3).astype('float32')

out = m1.predict(testinput)

print(out.shape)

out = m2.predict(testinput)

print(out.shape)
```

the above code works well.

One thing I found out is that first I though the `with tf.graph` and `with self.sess.as_default()` context block would cause a problem since normally at the end of context block, the context is closed automatically. But according to the tensorflow [docs](https://www.tensorflow.org/api_docs/python/tf/compat/v1/Session#attributes), this is not the case for tf.Session.
