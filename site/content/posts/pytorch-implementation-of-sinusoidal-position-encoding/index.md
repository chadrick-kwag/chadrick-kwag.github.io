---
title: pytorch implementation of sinusoidal position encoding
date: '2022-05-26T00:00:00+00:00'
lastmod: '2022-05-26T00:00:00+00:00'
slug: pytorch-implementation-of-sinusoidal-position-encoding
categories:
- machine-learning
tags:
- implementation
- position-encoding
- pytorch
- sinusoidal-position-encoding
draft: false
---
There are existing sinusoidal position encoding modules out there, but the ones that I confronted were mostly assuming the position to be incrementing from 0 to the size of sequence. For example, when a token embedding sequence with shape of (B, L, D_token) is given then the sinusoidal position encoding module will take this tensor as input and manually create a tensor (B,L) where the values for each row is (0,1,2,3, …., L-1) and then apply sinusoidal encoding on this.

But I wanted a sinusoidal position encoding module that can handle when position values are not incremental. For example, when I have a token embedding tensor (B,L,D_token), I also have a position array shape (B,L) where the position values are not incremental (e.g. (0,1,2,3,0,1,2,0,1,0,1,2,3,4,5,…) ).

To handle such cases, I coded my own sinusoidal position encoding module in pytorch where the input will be a tensor containing position integer values.

```python
class SinusoidalPositionEncoding(torch.nn.Module):
    def \_\_init\_\_(self, dim, max\_period=5000):

        assert dim % 2 == 0
        self.dim = dim

        self.max\_period = max\_period

        super().\_\_init\_\_()

        w\_arr = torch.arange(0, self.dim // 2)
        w\_arr = 1 / (max\_period) \*\* (w\_arr \* 2 / dim)

        self.register\_buffer("w\_arr", w\_arr)

    def forward(self, x):
        """
        assume x has shape (B,T) where B=batch size, T=token size(or sequence length)
        and values of x are integers >=0.
        """

        \_x = torch.unsqueeze(x, -1)  # (B,T,1)

        v = \_x \* self.w\_arr  # (B,T,dim//2)

        sin = torch.sin(v)
        sin = torch.unsqueeze(sin, -1)  # (B,T,m,1)

        cos = torch.cos(v)
        cos = torch.unsqueeze(cos, -1)  # (B,T,m,1)

        m = torch.cat(\[sin, cos\], -1)  # (B,T,m,2)

        b, t, \_, \_ = m.shape

        y = m.reshape(b, t, -1)  # (B,T,dim) where 2m=\`dim\`

        return y

```

If you are just using implicit incremental positions, then you don’t have to use this and just use one from any framework that goes with that approach.
