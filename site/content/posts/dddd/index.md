---
title: dddd
date: '2019-06-17T00:00:00+00:00'
lastmod: '2019-06-17T00:00:00+00:00'
slug: dddd
categories: []
tags: []
draft: false
---
```python
p1\_t = np.transpose(p1\_array)

print(f"p1\_t:{p1\_t}\\nT:{T}")
p3 = np.matmul(T, p1\_t)

print(f"p3: {p3}")

p3\_t = np.transpose(p3)

print(f"p3\_t: {p3\_t}")

#----

center\_point = (150,150)

# move origin to center point by subtracting cp for all point coords

print(">>>> test3")

p1\_arr = p1\_array.copy()

print(f"p1\_arr: {p1\_arr}")
p1\_sub = p1\_arr - np.array(center\_point)

print(f"p1\_sub: {p1\_sub}")

p1\_sub\_t = np.transpose(p1\_sub)

p1\_rot\_invt = np.matmul(T, p1\_sub\_t)

p1\_rot = np.transpose(p1\_rot\_invt)

print(f"p1\_rot: {p1\_rot}")

# restore to original coord

p2 = p1\_rot + np.array(center\_point)

print(f"p2: {p2}")

img = blank\_canvas.copy()
p2 = p2.tolist()
img = draw\_point\_list(img, p2)

savepath = os.path.join(outputdir, "test3\_output.png")
cv2.imwrite(savepath, img)


```
