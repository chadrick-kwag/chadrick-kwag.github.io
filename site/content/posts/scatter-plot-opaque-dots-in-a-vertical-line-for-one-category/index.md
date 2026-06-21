---
title: scatter plot opaque dots in a vertical line for one category
date: '2018-11-28T00:00:00+00:00'
lastmod: '2018-11-28T00:00:00+00:00'
slug: scatter-plot-opaque-dots-in-a-vertical-line-for-one-category
categories: []
tags:
- matplotlib
draft: false
---
```python
import matplotlib.pyplot as plt 

y=\[0.1, 0.2, 0.13, 0.1, 0.7, 1.0, 0.8, 0.9, 0.6, 0.64, 0.66, 0.84\]

x = \["test"\] \* len(y)

fig = plt.figure()

ax1 = fig.add\_subplot(111)

ax1.scatter(x, y, c="red", alpha=0.3)

plt.show()
```
