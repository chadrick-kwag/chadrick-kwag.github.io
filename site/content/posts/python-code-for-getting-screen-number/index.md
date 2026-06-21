---
title: python code for getting screen number
date: '2019-12-26T00:00:00+00:00'
lastmod: '2019-12-26T00:00:00+00:00'
slug: python-code-for-getting-screen-number
categories: []
tags:
- number
- python
- screen
draft: false
---
```generic
import os

def get\_screen\_info():

    screen\_id = os.environ.get("STY", None)
    if screen\_id:

        screen\_num = os.environ.get("WINDOW", None)

        return screen\_id, screen\_num

    return None, None
```
