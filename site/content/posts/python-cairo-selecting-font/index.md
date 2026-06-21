---
title: python cairo selecting font
date: '2019-03-12T00:00:00+00:00'
lastmod: '2019-03-12T00:00:00+00:00'
slug: python-cairo-selecting-font
categories: []
tags:
- cairo
- font
draft: false
---
Here is how to select the font in cairo in python.

```generic
import cairocffi as cairo

# define context somewhere..

ft="Times New Roman"
context.select\_font\_face(ft, cairo.FONT\_SLANT\_NORMAL, cairo.FONT\_WEIGHT\_NORMAL)
```
