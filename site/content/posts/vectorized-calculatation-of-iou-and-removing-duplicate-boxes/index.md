---
title: calculating IOU in a vectorized manner and fetching index pairs that are above
  threshold
date: '2019-01-25T00:00:00+00:00'
lastmod: '2019-01-25T00:00:00+00:00'
slug: vectorized-calculatation-of-iou-and-removing-duplicate-boxes
categories: []
tags:
- iou
- numpy
draft: false
---
when doing object detection, it would be very hard to avoid calculating IOU at some point. Although this could be done iteratively one by one in python with a for loop if there are only a few boxes, when the number of boxes become large the computation time increases significantly. One way to speed things up is to caluclate the IOU matrix in a vectorized manner: in other words, calculating in units of arrays.

Here is how calculate the IOU matrix using tensorflow. Also, the code will output the index pairs where the boxes have IOU value above a given threshold(in this case, 0.8). When getting this index pair, if we simply use `tf.where` with a condition the index pair would also include a pair of same indices, which is obvious because every box would have IOU values of 1.0 with itself. But we don’t want to count these cases. Therefore a bit more lines of code removes these cases.

BTW, the code below assumes that the coordinates of the boxes are values relative to the image width and height, thus we assume that it is in the range of 0~1.The code using tensorflow is as below:

```python
def get\_iou\_matrix\_tf(box\_arr1, box\_arr2):
    x11, y11, x12, y12 = tf.split(box\_arr1, 4, axis=1)
    x21, y21, x22, y22 = tf.split(box\_arr2, 4, axis=1)
    xA = tf.maximum(x11, tf.transpose(x21))
    yA = tf.maximum(y11, tf.transpose(y21))
    xB = tf.minimum(x12, tf.transpose(x22))
    yB = tf.minimum(y12, tf.transpose(y22))
    interArea = tf.maximum((xB - xA + 1e-9), 0) \* tf.maximum((yB - yA + 1e-9), 0)
    boxAArea = (x12 - x11 + 1e-9) \* (y12 - y11 + 1e-9)
    boxBArea = (x22 - x21 + 1e-9) \* (y22 - y21 + 1e-9)
    iou = interArea / (boxAArea + tf.transpose(boxBArea) - interArea)

    return iou

def calculate\_iou\_matrix\_tf(boxarr, threshold=0.8):

    # or can use gpu. e.g. "/device:GPU:0"
    device\_str = "/device:CPU:0"

    with tf.device(device\_str):
        box\_list\_ph = tf.placeholder(tf.float32, shape=(None, 4))
        iou\_matrix = get\_iou\_matrix\_tf(box\_list\_ph, box\_list\_ph)

        high\_iou\_coords = tf.where(iou\_matrix>threshold)

        print(high\_iou\_coords)

    with tf.device("/device:CPU:0"):
        first\_coords, second\_coords = tf.split(high\_iou\_coords, 2, axis=1)
        
        iscoord\_same = first\_coords - second\_coords

        tresult = tf.where(tf.not\_equal(iscoord\_same, 0))

        sel\_indices, \_ = tf.split(tresult,2, axis=1)

        sel\_indices = tf.squeeze(sel\_indices)

        valid\_high\_iou\_coords = tf.gather(high\_iou\_coords, sel\_indices)

    with tf.Session() as sess:

        \_iou\_matrix, \_valid\_high\_iou\_coords = sess.run(\[iou\_matrix, valid\_high\_iou\_coords\], feed\_dict={box\_list\_ph: boxarr})
```

One thing to note about the code above, is that there are two separate parts which uses `with tf.device` statements. The first part’s device argument can be replace with a GPU. However, the second part cannot. You can try and you will run into an error that GPU cannot work with int types. That is why the second part needs to be run in the CPU region.

The same can be done using numpy and this can be useful when user does not with to use tensorflow for getting the iou matrix.

```python
def calculate\_iou\_matrix(box\_arr1, box\_arr2):

    x11, y11, x12, y12 = np.split(box\_arr1, 4, axis=1)
    x21, y21, x22, y22 = np.split(box\_arr2, 4, axis=1)
    xA = np.maximum(x11, np.transpose(x21))
    yA = np.maximum(y11, np.transpose(y21))
    xB = np.minimum(x12, np.transpose(x22))
    yB = np.minimum(y12, np.transpose(y22))
    interArea = np.maximum((xB - xA + 1e-9), 0) \* np.maximum((yB - yA + 1e-9), 0)
    boxAArea = (x12 - x11 + 1e-9) \* (y12 - y11 + 1e-9)
    boxBArea = (x22 - x21 + 1e-9) \* (y22 - y21 + 1e-9)
    iou = interArea / (boxAArea + np.transpose(boxBArea) - interArea)

    return iou
```
