---


title: tf.where examples and its behavior
date: '2019-07-22T00:00:00+00:00'
lastmod: '2019-07-22T00:00:00+00:00'
slug: tf-where-examples-and-its-behavior
categories:
- machine-learning
tags:
- "tensorflow-equal"
- "tf-equal"
- "tf-where"
- "tensorflow"
- "behavior"
draft: false
---
Before going into `tf.where` example, a proper way to implement equal comparison in tensorflow will be demonstrated since equal comparison will be used as the condition of the `tf.where`.

## Equal Comparison in Tensorflow

```python
import tensorflow as tf, os

a = tf.constant(\[\[1,1\],\[3,6\]\])
b= a==3

with tf.Session() as sess:
    output = sess.run(b)

    print(output)
```

output:

```
TypeError: Fetch argument False has invalid type <class 'bool'>, must be a string or Tensor. (Can not convert a bool into a Tensor or Operation.)

Process finished with exit code 1
```

to fix this, do not use python native operands such as `==` in the above. instead use comparing operations provided by tensorflow.

```python
import tensorflow as tf, os

a = tf.constant(\[\[1,1\],\[3,6\]\])
b = tf.equal(a,3)

with tf.Session() as sess:
    output = sess.run(b)

    print(output)
```

output:

```
[[False False]
 [ True False]]
```

Now that we have verified how to properly use equal comparison in tensorflow, lets move on to `tf.where`

## Examples of `tf.where`

```python
import tensorflow as tf, os

a = tf.constant(\[\[1,1\],\[3,6\]\])
b = tf.where(tf.equal(a,3))

with tf.Session() as sess:
    output = sess.run(b)

    print(output)
```

output:

```
[[1 0]]
```

The coordinate of `3` in the sample tensor has been correctly identified. Then let’s try increasing the dimension of the target array.

```python
import tensorflow as tf, os

a = tf.constant(\[\[\[1,1\],\[3,6\]\],\[\[7,8\],\[9,9\]\]\])
b = tf.where(tf.equal(a,3))

with tf.Session() as sess:
    output = sess.run(b)

    print(output)
```

output:

```
[[0 1 0]]
```

We can identify that the output of `tf.where` will be dependant on the dimension of the input tensor.

Then how would the output look like when there are multiple condition matches in the input tensor?

```python
import tensorflow as tf, os

a = tf.constant(\[\[\[1,1\],\[3,6\]\],\[\[7,8\],\[3,3\]\]\])
b = tf.where(tf.equal(a,3))

with tf.Session() as sess:
    output = sess.run(b)

    print(output)
```

output:

```
[[0 1 0]
 [1 1 0]
 [1 1 1]]
```

We can identify that the coordinates of each of the multiple finding are returned in a list.
