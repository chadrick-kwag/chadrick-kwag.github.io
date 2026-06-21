---


title: sitk sample code
date: '2018-12-12T00:00:00+00:00'
lastmod: '2018-12-12T00:00:00+00:00'
slug: sitk-sample-code
categories:
- machine-learning
tags:
- "sitk"
- "sample"
- "code"
draft: false
---
```python
def resample\_isocubic(img, new\_spacing):
    def calc\_new\_size():
        np\_size = np.array(img.GetSize())
        np\_cur\_spacing = np.array(img.GetSpacing())
        np\_new\_spacing = np.array(new\_spacing)
        
        np\_new\_size = np\_size \* np\_cur\_spacing / new\_spacing
        return np\_new\_size.astype(int).tolist()
        
    origin = img.GetOrigin()
    size = img.GetSize()
    cur\_spacing = img.GetSpacing()
    direction = img.GetDirection()
    
    new\_size = calc\_new\_size()
    print(new\_size)
    transform = sitk.Transform()                # default is 'IdentityTransform'
    interpolator = sitk.sitkNearestNeighbor
    
    return sitk.Resample(img, 
                         new\_size,
                         transform,
                         interpolator,
                         origin,
                         new\_spacing,
                         direction,
                         0.0,
                         img.GetPixelIDValue())
```

```python
def resampleMask\_isocubic(img, base\_spacing, ref\_img):
    img.SetSpacing(base\_spacing)                # change with the same spacing of reference
    transform = sitk.Transform()                # default is 'IdentityTransform'
    interpolator = sitk.sitkNearestNeighbor
    
    return sitk.Resample(img, 
                         ref\_img.GetSize(),
                         transform,
                         interpolator,
                         ref\_img.GetOrigin(),
                         ref\_img.GetSpacing(),
                         ref\_img.GetDirection(),
                         0.0,
                         img.GetPixelIDValue())
```

```python
def resampleMask\_isocubic(img, base\_spacing, ref\_img):
    img.SetSpacing(base\_spacing)                # change with the same spacing of reference
    transform = sitk.Transform()                # default is 'IdentityTransform'
    interpolator = sitk.sitkNearestNeighbor
    
    return sitk.Resample(img, 
                         ref\_img.GetSize(),
                         transform,
                         interpolator,
                         ref\_img.GetOrigin(),
                         ref\_img.GetSpacing(),
                         ref\_img.GetDirection(),
                         0.0,
                         img.GetPixelIDValue())
```

```python
input\_img = read\_cardiac\_image(task='CHD', is\_label=False, file='sample\_dia.mha')
show\_info(input\_img)
show.myshow(input\_img)
base\_spacing = input\_img.GetSpacing()
isocubic\_img = resample\_isocubic(input\_img, (0.5, 0.5, 0.5))
show\_info(isocubic\_img)
show.myshow(isocubic\_img)
```

here is a full sample code

```python
"""
isotropically reslicing example code
"""

import SimpleITK as sitk , cv2, numpy as np , matplotlib.pyplot as plt , os, shutil

def resample\_isocubic(img, new\_spacing):
    def calc\_new\_size():
        np\_size = np.array(img.GetSize())
        np\_cur\_spacing = np.array(img.GetSpacing())
        np\_new\_spacing = np.array(new\_spacing)
        
        np\_new\_size = np\_size \* np\_cur\_spacing / new\_spacing
        return np\_new\_size.astype(int).tolist()
        
    origin = img.GetOrigin()
    size = img.GetSize()
    cur\_spacing = img.GetSpacing()
    direction = img.GetDirection()
    
    new\_size = calc\_new\_size()
    print(new\_size)
    transform = sitk.Transform()                # default is 'IdentityTransform'
    interpolator = sitk.sitkNearestNeighbor
    
    return sitk.Resample(img, 
                         new\_size,
                         transform,
                         interpolator,
                         origin,
                         new\_spacing,
                         direction,
                         0.0,
                         img.GetPixelIDValue())

def resampleMask\_isocubic(img, base\_spacing, ref\_img):
    img.SetSpacing(base\_spacing)                # change with the same spacing of reference
    transform = sitk.Transform()                # default is 'IdentityTransform'
    interpolator = sitk.sitkNearestNeighbor
    
    return sitk.Resample(img, 
                         ref\_img.GetSize(),
                         transform,
                         interpolator,
                         ref\_img.GetOrigin(),
                         ref\_img.GetSpacing(),
                         ref\_img.GetDirection(),
                         0.0,
                         img.GetPixelIDValue())

# mha\_file = "../chd\_sample/001\_dia\_M.mha"
mha\_file = "../chd\_sample/001\_dia.mha"
mask\_mha\_file = "../chd\_sample/001\_dia\_M.mha"

image = sitk.ReadImage(mha\_file)
maskimage = sitk.ReadImage(mask\_mha\_file)

raw\_spacing = image.GetSpacing()
direction = image.GetDirection()
size = image.GetSize()

print("spacing={}  , direction={}, size={}".format(raw\_spacing, direction, size))

new\_spacing = (0.5, 0.5, 0.5)
resampled\_image = resample\_isocubic(image, new\_spacing)

spacing = resampled\_image.GetSpacing()
direction = resampled\_image.GetDirection()
size = resampled\_image.GetSize()

print("after resampling >> spacing={}  , direction={}, size={}".format(spacing, direction, size))

resampled\_mask\_image = resampleMask\_isocubic(maskimage, raw\_spacing, resampled\_image)

spacing = resampled\_mask\_image.GetSpacing()
direction = resampled\_mask\_image.GetDirection()
size = resampled\_mask\_image.GetSize()

print("after resampling mask image >> spacing={}  , direction={}, size={}".format(spacing, direction, size))

# array = sitk.GetArrayFromImage(image) # shape: 171 , 512,512
```
