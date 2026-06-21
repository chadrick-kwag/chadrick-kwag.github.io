---
title: Using curve fitting to fit an equation to designated data points
date: '2020-02-18T00:00:00+00:00'
lastmod: '2020-02-18T00:00:00+00:00'
slug: using-curve-fitting-to-fit-an-equation-to-designated-data-points
categories: []
tags:
- curve-fitting
- curve_fit
- scipy
draft: false
---
Assume a situation where you have the frame of an equation at ready but are struggling to fit that equation to some data points. In other words, if you are stuck in a situation where you need to fit the and equation or function to a set of data points, using `curve_fit` in scipy is very helpful.

Here is an example where I have created an equation(check out `func` in the below sample code) with undecided parameters(a,b,c) which has the shape that I want. But I want this shape to pass three points, (0,0) (1,1) (5, 0.2).

Of course, there is no guarantee that by adjusting the three parameters would pass these three points precisely. But I at least want to get the values of the parameters which will be as close to passing these three points as possible.

```generic
import numpy as np
from scipy.optimize import curve\_fit

def func(x, a,b,c):

    return a - np.exp(b-x) - c \* 1/(1+ np.exp(-x))

points = \[
    (0,0),
    (1,1),
    (5, 0.2)
\]

points = np.array(points)
xdata = points\[:,0\]
ydata = points\[:,1\]

out = curve\_fit(func, xdata, ydata)

param\_matrix = out\[0\]

a = param\_matrix\[0\]
b = param\_matrix\[1\]
c = param\_matrix\[2\]
```

if we visualize this function it looks like this:
