---
title: python script to convert dir or file of image to png
date: '2020-04-01T00:00:00+00:00'
lastmod: '2020-04-01T00:00:00+00:00'
slug: python-script-to-convert-dir-or-file-of-image-to-png
categories:
- python
tags:
- convert-to-png
- imagemagick
draft: false
---
here is a simple code to convert dir/file of images to png in batch.

```python
import os, glob, argparse, datetime, subprocess

parser = argparse.ArgumentParser()

parser.add\_argument('inputs', type=str, help='path to input')

args = parser.parse\_args()

input\_path = args.inputs

assert os.path.exists(input\_path)

if os.path.isdir(input\_path):
    input\_files = glob.glob(os.path.join(input\_path, '\*'))
else:
    input\_files = \[input\_path\]
    

timestamp=datetime.datetime.now().strftime("%y%m%d\_%H%M%S")

outputdir = 'testoutput/{}'.format(timestamp)
os.makedirs(outputdir)
print("outputdir: {}".format(outputdir))

for f in input\_files:
    basename = os.path.basename(f)
    filename, \_ = os.path.splitext(basename)
    
    savepath = os.path.join(outputdir, '{}.png'.format(filename))
    
    cmd = 'convert {} {}'.format(f, savepath)
    subprocess.run(cmd, shell=True)
   

```

for installing imagemagick, use this command:

```generic
$ sudo apt install imagemagick
```
