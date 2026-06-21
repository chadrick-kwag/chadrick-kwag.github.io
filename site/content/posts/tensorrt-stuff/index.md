---


title: tensorRT stuff
date: '2019-03-18T00:00:00+00:00'
lastmod: '2019-03-18T00:00:00+00:00'
slug: tensorrt-stuff
categories:
- machine-learning
tags:
- "tensorrt"
- "stuff"
draft: false
---
tensorRT support matrix: <https://docs.nvidia.com/deeplearning/dgx/integrate-tf-trt/index.html#matrix>

to apply the tensorRT optimizations, it needs to call `create_inference_graph` function. Check [here](https://docs.nvidia.com/deeplearning/dgx/integrate-tf-trt/index.html) for more details on this function.

the graph that is fed to `create_inference_graph` should be freezed. To know more on what exactly means by “freezing”, check [here](https://www.tensorflow.org/guide/extend/model_files#freezing).

for using bare tensorRT python module, check out [here](https://docs.nvidia.com/deeplearning/sdk/tensorrt-archived/tensorrt_401/tensorrt-api/python_api/workflows/tf_to_tensorrt.html).
