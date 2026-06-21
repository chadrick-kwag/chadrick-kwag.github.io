---
title: 'error fix: onnxruntime "Type Error: Type ''tensor(int64)'' of input parameter
  of operator(Min) in node is invalid'''
date: '2021-11-17T00:00:00+00:00'
lastmod: '2021-11-17T00:00:00+00:00'
slug: error-fix-onnxruntime-type-error-type-tensorint64-of-input-parameter-of-operatormin-in-node-is-invalid
categories:
- machine-learning
tags:
- graph-invalid
- onnx
- opset
- type-error
- type-invalid
draft: false
---
# Background

I was trying to convert pytorch bert-like model from torch to onnx and see if I can run it in onnxruntime. Here’s the environment I used

- python: 3.9
- torch: 1.9.0
- onnx: 1.10.2
- onnxruntime-gpu: 1.9.0

I converted by pytorch model to onnx with the following line

```
# convert pytorch model to onnx
model = load_model(some_ckpt)
torch.onnx.export(model, model_input_args, output_filepath)
```

then I tried to load the onnx file and run it with onnxruntime like this:

```
import onnxruntime as ort, numpy as np

sess = ort.InferenceSession(onnx_file) # << where error occurs

test_input = .... # prepare dummy input using numpy arrays

output = sess.run(None, test_input)  
 
```

and then the exception with the following description appears.

```
[ONNXRuntimeError] : 10 : INVALID_GRAPH : Load model from test.onnx failed:This is an invalid model. Type Error: Type 'tensor(int64)' of input parameter (262) of operator (Min) in node (Min_84) is invalid.
  File "/run_onnx.py", line 17, in <module>
    sess = ort.InferenceSession(onnx_file)
```

# Cause & Solution

The error was hard to comprehend because it seems so unlikely that a simple ‘Min’ operation would not work just because the two inputs have ‘int64’ type.

I checked if the two inputs had different types, but it was the same after inspecting it with Netron, a model graph visualization tool.

The cause was due to low onnx opset version used when exporting from pytorch. By default, the `torch.onnx.export` function will used onnx opset 9. But according to the [docs](https://github.com/onnx/onnx/blob/master/docs/Operators.md#Min), while the latest `Min` operation introduced since onnx opset version 13 supports pretty much all types including “int64” type, the version range 8-11 only supports type “float16”, “float”, and “double”. My exported onnx used used version 9 so this was causing the problem.

The solution is then to export pytorch model to onnx using a higher onnx opset version. I decided to use 13 since this seems to be the [highest onnx opset version number supported by pytorch 1.9.0](https://github.com/pytorch/pytorch/tree/release/1.9/torch/onnx).

The exporting code was changed like this:

```
# convert pytorch model to onnx
model = load_model(some_ckpt)
torch.onnx.export(model, model_input_args, output_filepath, opset_version=13)
```

and rerunning the onnx load and run code, it works this time.
