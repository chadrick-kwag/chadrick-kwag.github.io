---
title: creating your own pytorch scheduler
date: '2022-05-12T00:00:00+00:00'
lastmod: '2022-05-12T00:00:00+00:00'
slug: creating-your-own-pytorch-scheduler
categories:
- machine-learning
tags: []
draft: false
---
here is an example of a scheduler that I subclassed in pytorch.

```python
class WarmUpAndCosineAnnealingLRScheduler(torch.optim.lr\_scheduler.\_LRScheduler):
    def \_\_init\_\_(
        self,
        optimizer: Optimizer,
        warmup\_steps: int,
        warmup\_lr,
        lr\_max,
        cosine\_t,
        last\_epoch: int = -1,
        verbose=False,
    ) -> None:

        assert warmup\_steps >= 0, "warmup\_steps >=0 required"
        self.warmup\_steps = warmup\_steps

        assert warmup\_lr > 0, "warmup lr >0 required"
        self.warmup\_lr = warmup\_lr

        assert lr\_max > warmup\_lr, "lr\_max > warmup\_lr required"
        self.lr\_max = lr\_max

        assert cosine\_t > 0, "cosine T >0 required"
        self.cosine\_t = cosine\_t

        super().\_\_init\_\_(optimizer, last\_epoch)

    def get\_lr(self) -> float:

        if self.\_step\_count < self.warmup\_steps:
            return \[self.warmup\_lr for \_ in self.base\_lrs\]

        else:

            x = self.\_step\_count - self.warmup\_steps
            amplitude = self.lr\_max - self.warmup\_lr

            new\_lr = self.warmup\_lr + amplitude / 2 \* (
                1 + math.cos(math.pi + x \* 2 \* math.pi / self.cosine\_t)
            )

            return \[new\_lr for \_ in self.base\_lrs\]

```
