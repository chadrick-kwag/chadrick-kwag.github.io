---
title: minimal annotation xml file generation compatible with labelimg
date: '2021-04-22T00:00:00+00:00'
lastmod: '2021-04-22T00:00:00+00:00'
slug: minimal-annotation-xml-file-generation-compatible-with-labelimg
categories:
- machine-learning
tags:
- convert-to-xml
- labelimg
- xml
draft: false
---
[LabelImg](https://github.com/tzutalin/labelImg) is a great and simple tool which can be used with easy when doing bounding box annotations. One downside that I feel with this tool is that it only supports two annotation formats: PascalVOC(xml) and YOLO. I have been using PascalVOC xml format which looks like this.

```generic
<annotation>
	<folder>images</folder>
	<filename>someimage.png</filename>
	<path>D:\\data\\someimage.png</path>
	<source>
		<database>Unknown</database>
	</source>
	<size>
		<width>2306</width>
		<height>2662</height>
		<depth>1</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>cell</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>155</xmin>
			<ymin>94</ymin>
			<xmax>2168</xmax>
			<ymax>454</ymax>
		</bndbox>
	</object>
	<object>
		<name>cell</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>91</xmin>
			<ymin>578</ymin>
			...
```

However, I usually manage object class and coordinates in json file which is more easier to handle in python. In order to modify my json annotations, I need to convert them into PascalVOC xml format which can be read from LabelImg.

For my pupose, I only need to utilize class and coordinate info from LabelImg, and do not require to use features such as verification labeling, difficult lableing which is supported in LabelImg.

The following python function shows the minimal part of xml format file that is needed to be created from a list of object class and coordinates. As can be seen from the code, not every single xml element shown above needs to be populated for it to be compatible with LabelImg.

```generic
import os
from lxml import etree as et

def create\_xml(imgfilepath, object\_list, savedir):
    """

    params:
    - imgfilepath: path of corresponding img file. only the basename will be actually used.
    - object\_list: python list of objects. the format of each element is up to the user, but for this example, each element will be a tuple of (classname, \[x1,y1,x2,y2\])
    - savedir: output directory to save generated xml file

    """

    basename = os.path.basename(imgfilepath)
    filename, \_ = os.path.splitext(basename)

    
    root = et.Element('annotation')

    fn\_elem = et.SubElement(root, 'filename')

    bn = os.path.basename(imagefilepath)
    fn, \_ = os.path.splitext(bn)
    img\_bn = f"{fn}.png"
    fn\_elem.text = img\_bn

    for classname, (x1,y1,x2,y2) in object\_list:
        object\_elem = et.SubElement(root, 'object')
        name = et.SubElement(object\_elem, 'name')
        name.text = classname
        bndbox = et.SubElement(object\_elem, 'bndbox')

        xmin = et.SubElement(bndbox, 'xmin')
        xmin.text = str(x1)
        xmax = et.SubElement(bndbox, 'xmax')
        xmax.text = str(x2)

        ymin = et.SubElement(bndbox, 'ymin')
        ymin.text = str(y1)
        ymax = et.SubElement(bndbox, 'ymax')
        ymax.text = str(y2)

    out = et.tostring(root, pretty\_print=True, encoding='utf8') # if element attributes contains some non ascii characters, then need to specify encoding. if not the case, then encoding doesn't need to be set

    savepath = os.path.join(savedir, f'{fn}.xml')

    with open(savepath, 'wb') as fd:
        fd.write(out)
```

Few things to be careful is, the xml file requires the coresponding image file name. Not the full path, just the filename. Also, the generated xml file should have the same filename as the corresponding image filename except the extension. For example, say I have given the imagepath as ‘/some/path/testimage.png’. The generated xml file should be named ‘testimage.xml’.
