---
title: cross entropy loss / focal loss implmentation in pytorch
date: '2020-08-21T00:00:00+00:00'
lastmod: '2020-08-21T00:00:00+00:00'
slug: cross-entropy-loss-focal-loss-implmentation-in-pytorch
categories:
- machine-learning
tags:
- cross-entropy-loss
- focal-loss
- focal-loss-implementation
- pytorch
- torch
draft: false
---
at the moment, the code is written for torch 1.4

## binary cross entropy loss

```generic
\## using pytorch 1.4

def logit\_sanitation(val, min\_val):

    unsqueezed\_a = torch.unsqueeze(val, -1)
    limit = torch.ones\_like(unsqueezed\_a) \* min\_val
    a = torch.cat((unsqueezed\_a, limit),-1)
    values, \_= torch.max(a,-1)

    return values
	
	
def manual\_bce\_loss(pred\_tensor, gt\_tensor, epsilon = 1e-8):

    a = logit\_sanitation(1-pred\_tensor, epsilon)
    b = logit\_sanitation(pred\_tensor, epsilon)

    loss = - ( (1- gt\_tensor) \* torch.log(a) + gt\_tensor \* torch.log(b))

    return loss
```

currently, torch 1.6 is out there and according to the pytorch docs, the `torch.max` function can receive two tensors and return element-wise max values. However, in 1.4 this feature is not yet supported and that is why I had to unsqueeze, concatenate and then apply `torch.max` in the above snippet. If you are using torch 1.6, you can change refactor the `logit_sanitation` function with the updated `torch.max` function.

The above binary cross entropy calculation will try to avoid any NaN occurrences due to excessively small logits when calculating `torch.log` which should return a very large negative number which may be too big to process resulting in NaN. The epsilon value will be limiting the original logit value’s minimum value.

## focal loss

using the functions defined above,

```generic
def manual\_focal\_loss(pred\_tensor, gt\_tensor, gamma, epsilon = 1e-8):

    a = logit\_sanitation(1-pred\_tensor, epsilon)
    b = logit\_sanitation(pred\_tensor, epsilon)

    logit = (1-gt\_tensor) \* a + gt\_tensor \* b
    focal\_loss = - (1-logit) \*\* gamma \* torch.log(logit)

    return focal\_loss
```

focal loss is also used quite frequently so here it is.
