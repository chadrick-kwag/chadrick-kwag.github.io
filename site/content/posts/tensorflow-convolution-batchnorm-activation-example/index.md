---
title: tensorflow convolution + batchnorm + activation example
date: '2019-08-19T00:00:00+00:00'
lastmod: '2019-08-19T00:00:00+00:00'
slug: tensorflow-convolution-batchnorm-activation-example
categories:
- machine-learning
tags:
- batchnorm
- convolution
- tensorflow
draft: false
---
The “convolution + batchnorm + activation” layer combination is an extremely powerful set which stabilizes training a lot. Since it appears in many model architectures, here I keep a tensorflow implementation for future reference.

```python
def conv\_bn\_actv(input, filter\_size, kernel, strides, activation="relu", padding="valid", name=None):

    assert isinstance(activation, str)

    if name:
        conv\_name = "{}\_conv".format(name)
    else:
        conv\_name = None
    conv1 = tf.keras.layers.Conv2D(filter\_size, kernel, strides=strides, padding=padding, name = conv\_name)(input)

    if name:
        bn\_name = "{}\_bn".format(name)
    else:
        bn\_name = None

    bn = tf.keras.layers.BatchNormalization(name=bn\_name)(conv1)

    if name:
        actv\_name = "{}\_actv\_{}".format(name, activation)
    else:
        actv\_name = None

    actv = tf.keras.layers.Activation(activation, name = actv\_name)(bn)

    return actv
```
