---


title: adding custom tf.keras metric
date: '2019-04-30T00:00:00+00:00'
lastmod: '2019-04-30T00:00:00+00:00'
slug: adding-custom-tf-keras-metric
categories:
- machine-learning
tags:
- "custom"
- "tensorflow"
- "metric"
- "keras"
draft: false
---
starting from tf 1.13 it looks like a native tf.keras precision metric exists. However for tf 1.10, it does not exist. So here is a custom created precision metric function that can be used for tf 1.10. I suppose this approach of creating custom metrics should work in other tf versions that do not have officially supported metrics.

```generic
def precision\_metric(y\_true, y\_pred):

    
    # mod\_y\_pred = tf.where(y\_pred>0.8, 1, 0)
    # mod\_y\_pred = tf.to\_float(y\_pred > 0.8)
    mod\_y\_pred = tf.cast(y\_pred > 0.8 , dtype=tf.float32)

    dl.debug("mod\_y\_pred: {}".format(mod\_y\_pred))

    # compare\_matrix = tf.where(y\_true == mod\_y\_pred, 1, 0)
    compare\_matrix = mod\_y\_pred \* y\_true

    dl.debug("compare\_matrix: {}".format(compare\_matrix))

    match\_count\_matrix = tf.reduce\_sum(compare\_matrix, axis=1)

    predicted\_count\_matrix = tf.reduce\_sum(mod\_y\_pred, axis=1)

    eps = 1e-8

    predicted\_count\_matrix += eps

    precision\_matrix = match\_count\_matrix / predicted\_count\_matrix

    precision = tf.reduce\_mean(precision\_matrix)

    dl.debug("precision mean : {}".format(precision))

    return precision
```

As you can see, the function is a graph builder and not an eagerly function.
