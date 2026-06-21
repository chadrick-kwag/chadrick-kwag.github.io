---
title: various properties of cairo `text_extent`
date: '2020-11-23T00:00:00+00:00'
lastmod: '2020-11-23T00:00:00+00:00'
slug: various-properties-of-cairo-text_extent
categories:
- machine-learning
tags:
- cairo
- context
- rotation
- text-extent
draft: false
---
when using cairo with python, the `text_extent` function call is powerful because it returns coordinate information of the text the user wants to print. However, the information depends on the `Context` which will be used when calling this function and this context may have different properties.

## Effected by order of `select_font_face` and `set_font_size`?

```python
import cairocffi as cairo

surface = cairo.ImageSurface(cairo.FORMAT\_RGB24, 100, 100)

context = cairo.Context(surface)

context.set\_font\_size(30)
context.select\_font\_face('times new roman')

xb,yb,w,h,xa,ya = context.text\_extents("hello")
print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

context = cairo.Context(surface)
context.select\_font\_face('times new roman')
context.set\_font\_size(30)

xb,yb,w,h,xa,ya = context.text\_extents("hello")
print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

"""
output:
xb=0.0, yb=-21.0, w=58.0, h=21.0, xa=59.0, ya=0.0
xb=0.0, yb=-21.0, w=58.0, h=21.0, xa=59.0, ya=0.0

"""
```

conclusion: is not affected by order

## Effected by rotation?

```python
import cairocffi as cairo, numpy as np

surface = cairo.ImageSurface(cairo.FORMAT\_RGB24, 100, 100)

context = cairo.Context(surface)

xb,yb,w,h,xa,ya = context.text\_extents("hello")

print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

context.rotate(5/180 \* np.pi) # rotate slightly

xb,yb,w,h,xa,ya = context.text\_extents("hello")

print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

### output:
### xb=0.0, yb=-7.000000000000001, w=21.0, h=7.000000000000001, xa=21.0, ya=0.0
### xb=0.0, yb=-8.0, w=21.0, h=8.0, xa=21.0, ya=0.0
```

conclusion: it is affected by rotation

## does it return valid results for blank space?

```python
import cairocffi as cairo

surface = cairo.ImageSurface(cairo.FORMAT\_RGB24, 100, 100)

context = cairo.Context(surface)

xb,yb,w,h,xa,ya = context.text\_extents(" ")
print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

xb,yb,w,h,xa,ya = context.text\_extents("ab")
print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

xb,yb,w,h,xa,ya = context.text\_extents("a b")
print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

xb,yb,w,h,xa,ya = context.text\_extents("ab ")
print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

xb,yb,w,h,xa,ya = context.text\_extents(" ab")
print(f"xb={xb}, yb={yb}, w={w}, h={h}, xa={xa}, ya={ya}")

"""
output:
xb=0.0, yb=0.0, w=0.0, h=0.0, xa=3.0000000000000004, ya=0.0  # " "
xb=0.0, yb=-7.000000000000001, w=11.0, h=7.000000000000001, xa=11.0, ya=0.0   # "ab"
xb=0.0, yb=-7.000000000000001, w=14.0, h=7.000000000000001, xa=14.0, ya=0.0   # "a b"
xb=0.0, yb=-7.000000000000001, w=11.0, h=7.000000000000001, xa=14.0, ya=0.0   # "ab "
xb=3.0000000000000004, yb=-7.000000000000001, w=11.0, h=7.000000000000001, xa=14.0, ya=0.0   # " ab"
"""


```

conclusion: blank spaces are automatically ignored for bounding box related outputs(‘w’, ‘h’) but it does affect bearings and advancements which are related to cursor positioning.
