---
title: solving TF-TRT graph conversion errors
date: '2019-03-19T00:00:00+00:00'
lastmod: '2019-03-19T00:00:00+00:00'
slug: solving-tf-trt-graph-conversion-errors
categories: []
tags:
- tensorrt
draft: false
---
I’ve tried converting a graph in various setups which produced different error messages

Original environment

- ubuntu 16.04
- CUDA 9.0.176
- cudnn 7.0.x
- TITAN XP: compute capability 6.1
- nvidia driver version 384.130
- tensorRT 4.0

original environment + tensorflow-gpu==1.11.0

```generic
2019-03-19 15:03:06.618682: E tensorflow/stream\_executor/cuda/cuda\_dnn.cc:343\] Loaded runtime CuDNN library: 7.1.3 but source was compiled with: 7.2.1. CuDNN library major and minor version needs to match or have higher minor version in case of CuDNN 7.0 or later version. If using a binary install, upgrade your CuDNN library.  If building from sources, make sure the library loaded at runtime is compatible with the version specified during compile configuration.
Segmentation fault (core dumped)
```

original environment + tensorflow-gpu==1.12.0

```generic
UnknownError (see above for traceback): Failed to get convolution algorithm. This is probably because cuDNN failed to initialize, so try looking to see if a warning log message was printed above.
         \[\[node conv2d\_1/convolution (defined at t3.py:53)  = Conv2D\[T=DT\_FLOAT, data\_format="NCHW", dilations=\[1, 1, 1, 1\], padding="SAME", strides=\[1, 1, 1, 1\], use\_cudnn\_on\_gpu=true, \_device="/job:localhost/replica:0/task:0/device:GPU:0"\](conv2d\_1/convolution-0-TransposeNHWCToNCHW-LayoutOptimizer, conv2d\_1/kernel/read)\]\]
         \[\[{{node predictions/concat/\_2335}} = \_Recv\[client\_terminated=false, recv\_device="/job:localhost/replica:0/task:0/device:CPU:0", send\_device="/job:localhost/replica:0/task:0/device:GPU:0", send\_device\_incarnation=1, tensor\_name="edge\_5676\_predictions/concat", tensor\_type=DT\_FLOAT, \_device="/job:localhost/replica:0/task:0/device:CPU:0"\]()\]\]
```

anaconda environment(may not match with original environment)

```generic
2019-03-19 15:29:11.917619: I tensorflow/core/grappler/devices.cc:51\] Number of eligible GPUs (core count >= 8): 1
2019-03-19 15:29:12.885814: I tensorflow/contrib/tensorrt/convert/convert\_graph.cc:383\] MULTIPLE tensorrt candidate conversion: 167
2019-03-19 15:29:12.890672: E tensorflow/contrib/tensorrt/log/trt\_logger.cc:38\] DefaultLogger (Unnamed Layer\* 7) \[Concatenation\]: all concat input tensors must have the same dimensions except on the concatenation axis
2019-03-19 15:29:12.890688: E tensorflow/contrib/tensorrt/convert/convert\_nodes.cc:534\] Dimension does not match, fail gracefully
2019-03-19 15:29:12.890699: I tensorflow/contrib/tensorrt/convert/convert\_nodes.cc:2624\] Max batch size= 1 max workspace size= 13953
2019-03-19 15:29:12.890703: I tensorflow/contrib/tensorrt/convert/convert\_nodes.cc:2630\] starting build engine
python3: ../builder/tacticOptimizer.cpp:1768: bool nvinfer1::builder::{anonymous}::hasSolution(const nvinfer1::query::TensorRequirements&, const nvinfer1::builder::Region&): Assertion \`req.pitches\[i\].empty() == (i > r.dims.nbDims)' failed.
Aborted (core dumped)
```

## Solution

install cudnn 7.5.0

and used tensorflow==1.12.0

these two factors allowed the script to run without errors and it produced results correctly.
