---
title: setting gpu fraction in tensorflow keras
date: '2019-09-17T00:00:00+00:00'
lastmod: '2019-09-17T00:00:00+00:00'
slug: setting-gpu-fraction-in-tensorflow-keras
categories: []
tags:
- gpu-fraction
draft: false
---
```generic
\# set gpu fraction
gpu\_fraction = 0.3

if gpu\_fraction is not None:

    assert gpu\_fraction >0 and gpu\_fraction < 1, "invalid gpu\_fraction={}".format(gpu\_fraction)
    sessconfig = tf.ConfigProto()
    sessconfig.gpu\_options.per\_process\_gpu\_memory\_fraction = gpu\_fraction
    session = tf.Session(config=sessconfig)

    tf.keras.backend.set\_session(session)
```

put this code at the beginning before building/loading the model.
