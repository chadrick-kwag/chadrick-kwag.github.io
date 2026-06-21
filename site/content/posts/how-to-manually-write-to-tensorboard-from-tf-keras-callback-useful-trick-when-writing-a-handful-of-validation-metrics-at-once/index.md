---
title: how to manually write to tensorboard from tf.keras callback (useful trick when
  writing a handful of validation metrics at once)
date: '2019-07-25T00:00:00+00:00'
lastmod: '2019-07-25T00:00:00+00:00'
slug: how-to-manually-write-to-tensorboard-from-tf-keras-callback-useful-trick-when-writing-a-handful-of-validation-metrics-at-once
categories:
- machine-learning
tags: []
draft: false
---
`tf.keras` does support `Metric` classes which can evaludate metrics at each batch. However, it does have a limitation that it can only calculat on training data and it can only output only one value.

This becomes a problem especially in cases such as when the user does validation evaluation and needs to record more than one metrics at once. A `callback` is more suitable for periodic validation set evaluation since it would be slow and computationally expensive to execute this at every training step. However, a native `callback` does not solve the problem of saving any calculated values into tfsummary so that the user can track down these values from tensorboard. However this part can be hacked.

First, a vanilla `TensorBoard` callback needs to be instantiated and passed on to our custom callback.

```python
import tensorflow as tf
from .test\_callback import TestCallback

model = tf.keras.Model()

tb\_callback = tf.keras.callbacks.TensorBoard("somedir")
test\_callback = TestCallback(tb\_callback)

callbacks = \[
    tb\_callback,
    test\_callback
\]

model.fit(x\_data, y\_data, batch\_size=8, epochs=10, callbacks=callbacks)
```

The `TestCallback` looks like this:

```python
import tensorflow as tf

class TestCallback(tf.keras.callbacks.Callback):

    def \_\_init\_\_(self, tb\_callback):

        self.tb\_callback = tb\_callback
        self.step\_number =0

    def on\_epoch\_end(self, epoch, logs=None):

        test\_input = "something"
        test\_gt = "some ground truth data"

        test\_output = self.model.predict(test\_input)

        metric1, metric2 = get\_metrics(test\_gt, test\_output)

        items\_to\_write={
            "metric1\_name": metric1,
            "metric2\_name": metric2
        }

        writer = self.tb\_callback.writer

        for name, value in items\_to\_write.items():

            summary = tf.summary.Summary()
            summary\_value = summary.value.add()
            summary\_value.simple\_value = value
            summary\_value.tag = name
            writer.add\_summary(summary, self.step\_number)
            writer.flush()

        self.step\_number += 1

```
