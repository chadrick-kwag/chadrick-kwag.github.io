---


title: convert cairo surface to cv2 imgmat
date: '2018-12-03T00:00:00+00:00'
lastmod: '2018-12-03T00:00:00+00:00'
slug: convert-cairo-surface-to-cv2-imgmat
categories:
- machine-learning
tags:
- "cairo"
- "opencv"
- "surface"
- "imgmat"
draft: false
---
```python
def convert\_to\_cvmat(surface, surface\_width, surface\_height):
    """
    works with FORMAT\_RGB24
    it should work with FORMAT\_ARGB32 too but the transparency will be ignored.
    """
    # print("surface format = {}".format(surface.get\_format()))
    # assert surface.get\_format() == cairo.FORMAT\_RGB24

    buf = surface.get\_data()
    # print("format={}, given\_surface\_width:{}, actual\_surface\_width:{}, buf size: {}".format( surface.get\_format(), surface\_width, surface.get\_width(), len(buf)))

    # if surface.get\_width() != surface\_width:
    #     surface.write\_to\_png("error.png")
        

    np\_converted = np.ndarray(shape=(surface\_width, surface\_height),
                              dtype=np.uint32,
                              buffer=buf)

    # for r bitwise AND with 0x00ff0000
    r\_filter = int("00ff0000", 16)
    g\_filter = int("0000ff00", 16)
    b\_filter = int("000000ff", 16)

    np\_r\_filtered = np.bitwise\_and(np\_converted, r\_filter)
    np\_r\_shifted = np.right\_shift(np\_r\_filtered, 16)
    np\_r = np.expand\_dims(np\_r\_shifted, axis=-1)

    np\_g\_filtered = np.bitwise\_and(np\_converted, g\_filter)
    np\_g = np.expand\_dims(np.right\_shift(np\_g\_filtered, 8), axis=-1)

    np\_b = np.expand\_dims(np.bitwise\_and(np\_converted, b\_filter), axis=-1)

    # cv2 uses BGR format so concatenated in this order

    combined\_32 = np.concatenate(\[np\_b, np\_g, np\_r\], axis=2)

    combined = combined\_32.astype(np.uint8)

    return combined
```
