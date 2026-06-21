---
title: gathering non-identical indices that match a condition in a matrix using tensorflow
date: '2019-01-28T00:00:00+00:00'
lastmod: '2019-01-28T00:00:00+00:00'
slug: gathering-indices-that-matches-condition
categories:
- machine-learning
tags: []
draft: false
---
here is an example. There is a square shaped 2-dimensional matrix(ss_matrix) and I want to get the index pairs which satisfy where the value of the matrix is above 0.8. But, I do not wish to select the index pairs where the first and second index are the same. This operation can be achieved in tensorflow with the combination of `tf.where` and `tf.gather`

```python
sm\_sel\_indices = tf.where(some\_matrix > 0.8, None, None)
index\_list\_1 , index\_list\_2 = tf.split(sm\_sel\_indices, 2, axis=1)
index\_diff = index\_list\_1 - index\_list\_2
index\_diff = tf.squeeze(index\_diff)

index\_of\_index\_list\_where\_not\_same = tf.where(tf.not\_equal(index\_diff, 0), None, None)

index\_of\_index\_list\_where\_not\_same = tf.squeeze(index\_of\_index\_list\_where\_not\_same)

sm\_over\_thresh\_no\_same\_indices = tf.gather(sm\_sel\_indices, index\_of\_index\_list\_where\_not\_same)
```
