---
title: '`keras.load_weight` and `keras.load_model` gives different results'
date: '2019-10-29T00:00:00+00:00'
lastmod: '2019-10-29T00:00:00+00:00'
slug: keras-load_weight-and-keras-load_model-gives-different-results
categories:
- machine-learning
tags:
- load_model
- tensorflow
draft: false
---
There can be several ways to load a model from ckpt file and run inference.

#### Method1

Build model instance from source, just like in preparing for training from scratch.

```generic
model = build\_model\_function()
model.load\_weights(ckpt\_path)

model.predict(X)
```

#### Method2

When the ckpt file is a bundle of model architecture and weights, then simply use `load_model` function.

```generic
model = tf.keras.model.load\_model(ckpt\_path)

model.predict(X)
```

#### Method3

In case the model architecture and weights are saved in separate files, use `model_from_json` / `model_from_config` and `load_weights`

```generic
with open("model\_arch.json", 'r') as fd:
  archjson = fd.read()

model = tf.keras.model.model\_from\_json(archjson)
model.load\_weights(ckpt\_path)

```

## Symptom

Usually, any of these methods should work but I have ran into some cases where only Method#1 works and others failed. Method#2 and #3 seemed to have no problem when constructing a model and loading the weights, but its predictions were incorrect compared to the results from Method#1.

## Solution

The cause of this problem was infact due to the use of `Lambda` layers in the model architecture. This function is a custom function that the user defines and when the model architecture is saved in the ckpt file(or json file), the function of Lambda is not saved. Rather, it is saved in a weird string which is unreadable. This is why in `Lambda` used model reconstruction, using the original model building function from source works while reconstructing from an external save file fails.

To solve this problem the user will be forced to use Method#1 or find an alternative method to avoid using `Lambda` layers.
