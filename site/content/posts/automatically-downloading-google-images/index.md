---
title: automatically downloading google images
date: '2018-11-29T00:00:00+00:00'
lastmod: '2018-11-29T00:00:00+00:00'
slug: automatically-downloading-google-images
categories:
- python
tags:
- image-download
draft: false
---
use `googleimagedownload` python library.

[pypi link](https://pypi.org/project/google-images-download/1.0.1/)

here’s an example to run by importing

```python
from google\_images\_download import google\_images\_download

response = google\_images\_download.googleimagesdownload()

response.download({
    "keywords": "flower, car",
    "format": "png"
    })

```

if you want a lot of keywords, try this code

```python
from google\_images\_download import google\_images\_download

response = google\_images\_download.googleimagesdownload()

keyword\_list=\[
    "flower",
    "car",
    "seoul",
    "nature",
    "forest",
    "city",
    "machine",
    "graphic art",
    "computer",
    "people",
    "microscopic images",
    "colorful",
    "tiny stuff",
    "dense",
    "xray",
    "population",
    "crowded",
    "person",
    "scene",
    "coat",
    "rain",
    "cartoon",
    "dark nature",
    "sky",
    "night vision",
    "semiconductor",
    "grid",
    "pixel art"
\]

keyword\_str=""
for index, k in enumerate(keyword\_list):
    if index == len(keyword\_list)-1:
        keyword\_str+=k
    else:
        keyword\_str+=k
        keyword\_str+=','
    

response.download({
    "keywords":keyword\_str,
    "format": "png"
    })
```
