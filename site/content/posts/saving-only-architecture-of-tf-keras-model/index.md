---


title: saving and loading only architecture of tf.keras model
date: '2019-05-25T00:00:00+00:00'
lastmod: '2019-05-25T00:00:00+00:00'
slug: saving-only-architecture-of-tf-keras-model
categories:
- machine-learning
tags:
- "architecture"
- "model"
- "saving"
- "only"
- "tensorflow"
draft: false
---
One can export only the model’s architecture information as JSON file like the following.

```python
modeljson = model.to\_json()

model\_save\_path = "somewhere/model\_arch.json

with open(model\_save\_path,'w') as fd:
    fd.write(modeljson)
```

To load this back to model, here is a sample code

```python
with open(model\_json\_path,'r') as fd:
    modeljson = fd.read()

model = tf.keras.models.model\_from\_json(modeljson)
```
