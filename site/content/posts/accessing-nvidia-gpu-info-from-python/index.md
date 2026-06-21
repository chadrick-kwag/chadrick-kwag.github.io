---


title: Accessing NVIDIA gpu info from python
date: '2019-05-18T00:00:00+00:00'
lastmod: '2019-05-18T00:00:00+00:00'
slug: accessing-nvidia-gpu-info-from-python
categories:
- machine-learning
tags:
- "nvidia"
- "nvml"
- "python-gpu-usage"
- "accessing"
- "gpu"
draft: false
---
Here is an example code and its output. I think it is easy to expand from here.

```python
import pynvml as nvml

nvml.nvmlInit()

print(f"driver version: {nvml.nvmlSystemGetDriverVersion().decode()}")

print(f"device count: {nvml.nvmlDeviceGetCount()}")

handle = nvml.nvmlDeviceGetHandleByIndex(0)
info = nvml.nvmlDeviceGetMemoryInfo(handle)

total\_mem = info.total
total\_mem = total\_mem / (1024\*1024)
print(f"total\_mem(MB): {total\_mem}")

free\_mem = info.free
free\_mem = free\_mem / (1024\*1024)
print(f"free\_mem(MB): {free\_mem}")

free\_percentage = free\_mem / total\_mem \* 100

print(f"free %: {free\_percentage}")
```

And the output:

```generic
driver version: 410.104
device count: 1
total\_mem(MB): 4046.0625
free\_mem(MB): 3634.1875
free %: 89.82035003166658
```

This was coded with python 3.6.6 and the packge used was the this one: <https://pypi.org/project/nvidia-ml-py3/>
