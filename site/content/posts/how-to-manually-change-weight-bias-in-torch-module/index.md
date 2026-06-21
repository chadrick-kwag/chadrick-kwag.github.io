---


title: how to manually change weight/bias in torch module
date: '2020-04-03T00:00:00+00:00'
lastmod: '2020-04-03T00:00:00+00:00'
slug: how-to-manually-change-weight-bias-in-torch-module
categories:
- machine-learning
tags:
- "change-bias"
- "change-weight"
- "lstm-bias"
- "pytorch"
- "manually"
draft: false
---
## Problem

an LSTM module will be used as an example. Assume a simple net that includes an LSTM module.

```generic
import torch 

class Net(torch.nn.Module):

    def \_\_init\_\_(self):
        super().\_\_init\_\_()

        self.lstm = torch.nn.LSTM(1,1,1) # input element size:1, hidden state size: 1, num\_layers = 1

        ...
```

According to the [docs](https://pytorch.org/docs/stable/nn.html#lstm), the weight and bias can be accessed by `weight_ih_l[k]`, `weight_hh_l[k]`, `bias_ih_l[k]`, `bias_hh_l[k]`. For this example, I want to set the b_if to one. So, I could do something like this.

```generic
class Net(torch.nn.Module):

    def \_\_init\_\_(self):
        super().\_\_init\_\_()

        self.lstm = torch.nn.LSTM(1,1,1) # input element size:1, hidden state size: 1, num\_layers = 1

        print(self.lstm.bias\_ih\_l0) # printing for demonstration. output: tensor(\[-0.4163, -0.0641, -0.3475,  0.5244\], requires\_grad=True)

        hidden\_size = 1
        b\_if\_start\_index = int(4\*hidden\_size \* 0.25)
        b\_if\_end\_index = int(4\*hidden\_size \* 0.5)
        self.lstm.bias\_ih\_l0\[b\_if\_start\_index:b\_if\_end\_index\] = 1

        print(self.lstm.bias\_ih\_l0)  # ouput: tensor(\[-0.4163,  1.0000, -0.3475,  0.5244\], grad\_fn=<CopySlices>)

        ...
```

we can verify that the b_if value has been manually set to 1 as intended.

However, when this net is trained with optimizer, it raises an error.

```generic
ValueError: can't optimize a non-leaf Tensor
```

as it turns out, the approached used above turns `self.lstm.bias_ih_l0` to a non-leaf tensor. This can be confirmed like this:

```python
class Net(torch.nn.Module):

    def \_\_init\_\_(self):
        super().\_\_init\_\_()

        self.lstm = torch.nn.LSTM(1,1,1) # input element size:1, hidden state size: 1, num\_layers = 1

        print(self.lstm.bias\_ih\_l0) # printing for demonstration. output: tensor(\[-0.4163, -0.0641, -0.3475,  0.5244\], requires\_grad=True)
        print(self.lstm.bias\_ih\_l0.is\_leaf) # output: True

        hidden\_size = 1
        b\_if\_start\_index = int(4\*hidden\_size \* 0.25)
        b\_if\_end\_index = int(4\*hidden\_size \* 0.5)
        self.lstm.bias\_ih\_l0\[b\_if\_start\_index:b\_if\_end\_index\] = 1

        print(self.lstm.bias\_ih\_l0)  # ouput: tensor(\[-0.4163,  1.0000, -0.3475,  0.5244\], grad\_fn=<CopySlices>)
        print(self.lstm.bias\_ih\_l0.is\_leaf) # output: False
```

as you can see, before manually changing the b_if value, the `self.lstm.bias_ih_l0` tensor is a leaf tensor but after the operation, it no longer is.

# Solution

To avoid the error, the manualy bias value change should be done like this.

```python
class Net(torch.nn.Module):

    def \_\_init\_\_(self):
        super().\_\_init\_\_()

        self.lstm = torch.nn.LSTM(1,1,1) # input element size:1, hidden state size: 1, num\_layers = 1

        print(self.lstm.bias\_ih\_l0) # printing for demonstration. output: tensor(\[-0.4163, -0.0641, -0.3475,  0.5244\], requires\_grad=True)
        print(self.lstm.bias\_ih\_l0.is\_leaf) # output: True

        hidden\_size = 1
        b\_if\_start\_index = int(4\*hidden\_size \* 0.25)
        b\_if\_end\_index = int(4\*hidden\_size \* 0.5)

        bias\_nparr = self.lstm.bias\_ih\_l0.detach().numpy()

        bias\_nparr\[b\_if\_start\_index:b\_if\_end\_index\] = 1

        print(self.lstm.bias\_ih\_l0)  # ouput: tensor(\[-0.4163,  1.0000, -0.3475,  0.5244\], requires\_grad=True)
        print(self.lstm.bias\_ih\_l0.is\_leaf) # output: True
```

the difference is that the bias tensor is first **detached** and then by applying `numpy()`, the code gains access to the tensor **values** only. After that, we change only the b_if section to 1. This way, the error does not show up even at optimization procedure.

Detaching is required since we want a copy of the bias tensor but without the `require_grad` set to True. Tensors with `require_grad=True` will not allow `numpy()` function to work and raise an error. Here is a [link](https://pytorch.org/docs/stable/autograd.html#torch.Tensor.detach) to the doc on `detach`.

`detach` will copy the tensor but it will point to the same data storage, which is why changes made to `bias_nparr` variable is reflected automatically to `self.lstm.bias_ih_l0`.
