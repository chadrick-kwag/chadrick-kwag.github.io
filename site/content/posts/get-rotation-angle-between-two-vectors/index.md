---
title: get rotation angle between two vectors
date: '2021-04-30T00:00:00+00:00'
lastmod: '2021-04-30T00:00:00+00:00'
slug: get-rotation-angle-between-two-vectors
categories:
- python
tags:
- angle
- vector
draft: false
---
Getting the angle between two vectors is well known. But finding the ‘rotation angle’ from one vector to another needs a bit more consideration. The following functions can handle this.

```generic
import numpy as np

def calculate\_rotation\_angle\_from\_vector\_to\_vector(a,b):
    """ return rotation angle from vector a to vector b, in degrees.

    Args:
        a : np.array vector. format (x,y)
        b : np.array vector. format (x,y)

    Returns:
        angle \[float\]: degrees. 0~360
    """

    unit\_vector\_1 = a / np.linalg.norm(a)
    unit\_vector\_2 = b / np.linalg.norm(b)
    dot\_product = np.dot(unit\_vector\_1, unit\_vector\_2)
    angle = np.arccos(dot\_product)

    angle = angle/ np.pi \* 180

    c = np.cross(b,a)

    if c>0:
        angle +=180
    

    return angle
```

This function will use cross product between two vectors to identify if the rotation direction is CW or CCW. This function will return rotation angle in CCW direction in degrees.
