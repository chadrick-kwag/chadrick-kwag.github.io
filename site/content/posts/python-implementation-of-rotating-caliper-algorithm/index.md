---
title: python implementation of rotating caliper algorithm
date: '2020-08-12T00:00:00+00:00'
lastmod: '2020-08-12T00:00:00+00:00'
slug: python-implementation-of-rotating-caliper-algorithm
categories:
- python
tags:
- python-implementation
- rotating-caliper
draft: false
---
Rotating caliper algorithm is used to find a rectangle that fits a convex hull. Below is a python implementation that finds all rotated rectangles for a given convex hull points. It is up to the user to select which rectangle to use since it returns all possible rotating caliper rectangles.

```generic
import numpy as np

def get\_rotating\_caliper\_bbox\_list(hull\_points\_2d):
    """

    hull\_points\_2d: array of hull points. each element should have \[x,y\] format
    """

    # Compute edges (x2-x1,y2-y1)
    edges = np.zeros( (len(hull\_points\_2d)-1,2) ) # empty 2 column array
    for i in range( len(edges) ):
        edge\_x = hull\_points\_2d\[i+1,0\] - hull\_points\_2d\[i,0\]
        edge\_y = hull\_points\_2d\[i+1,1\] - hull\_points\_2d\[i,1\]
        edges\[i\] = \[edge\_x,edge\_y\]

    # Calculate edge angles   atan2(y/x)
    edge\_angles = np.zeros( (len(edges)) ) # empty 1 column array
    for i in range( len(edge\_angles) ):
        edge\_angles\[i\] = np.arctan2( edges\[i,1\], edges\[i,0\] )

    # Check for angles in 1st quadrant
    for i in range( len(edge\_angles) ):
        edge\_angles\[i\] = np.abs( edge\_angles\[i\] % (np.pi/2) ) # want strictly positive answers
    #print "Edge angles in 1st Quadrant: \\n", edge\_angles

    # Remove duplicate angles
    edge\_angles = np.unique(edge\_angles)
    #print "Unique edge angles: \\n", edge\_angles

    bbox\_list=\[\]
    for i in range( len(edge\_angles) ):

        # Create rotation matrix to shift points to baseline
        # R = \[ cos(theta)      , cos(theta-PI/2)
        #       cos(theta+PI/2) , cos(theta)     \]
        R = np.array(\[ \[ np.cos(edge\_angles\[i\]), np.cos(edge\_angles\[i\]-(np.pi/2)) \], \[ np.cos(edge\_angles\[i\]+(np.pi/2)), np.cos(edge\_angles\[i\]) \] \])

        # Apply this rotation to convex hull points
        rot\_points = np.dot(R, np.transpose(hull\_points\_2d) ) # 2x2 \* 2xn

        # Find min/max x,y points
        min\_x = np.nanmin(rot\_points\[0\], axis=0)
        max\_x = np.nanmax(rot\_points\[0\], axis=0)
        min\_y = np.nanmin(rot\_points\[1\], axis=0)
        max\_y = np.nanmax(rot\_points\[1\], axis=0)

        # Calculate height/width/area of this bounding rectangle
        width = max\_x - min\_x
        height = max\_y - min\_y
        area = width\*height

        # Calculate center point and restore to original coordinate system
        center\_x = (min\_x + max\_x)/2
        center\_y = (min\_y + max\_y)/2
        center\_point = np.dot( \[ center\_x, center\_y \], R )

        # Calculate corner points and restore to original coordinate system
        corner\_points = np.zeros( (4,2) ) # empty 2 column array
        corner\_points\[0\] = np.dot( \[ max\_x, min\_y \], R )
        corner\_points\[1\] = np.dot( \[ min\_x, min\_y \], R )
        corner\_points\[2\] = np.dot( \[ min\_x, max\_y \], R )
        corner\_points\[3\] = np.dot( \[ max\_x, max\_y \], R )

        bbox\_info = \[edge\_angles\[i\], area, width, height, min\_x, max\_x, min\_y, max\_y, corner\_points, center\_point\]
        bbox\_list.append(bbox\_info)

    return bbox\_list
```

this code was based on code from [here](https://github.com/dbworth/minimum-area-bounding-rectangle/blob/master/python/min_bounding_rect.py). I only updated the code to return all possible rectangles instead of the one with minimum area since the user may be interested in other rectangles depending on their needs. Also I’ve updated it to use explicit functions from numpy.
