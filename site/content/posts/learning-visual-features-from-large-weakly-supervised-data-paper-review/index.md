---


title: '"Learning Visual Features from Large Weakly Supervised Data" paper review'
date: '2020-08-31T00:00:00+00:00'
lastmod: '2020-08-31T00:00:00+00:00'
slug: learning-visual-features-from-large-weakly-supervised-data-paper-review
categories:
- paper-review
tags:
- "weak-supervised"
- "weakly-supervised"
- "learning"
- "visual"
- "features"
draft: false
---
[arxiv link](https://arxiv.org/pdf/1511.02251.pdf)

key points

- attempts to train classifier with weakly annotated data from flicker. Thus, this this paper is about “weakly supervised” training.
- the data used is scraped from flicker where the scrapped data includes hash keywords and descriptions. The authors strip out keywords from these data
- They used GoogLeNet and AlexNet model architecture for comparison with weakly supervised trained model and existing pre-trained model.
- Results are that models trained with weakly supervised data are in par with existing pre-trained models.

Comments

- this work is trying to train a classifier 1000, 10000, 100000 classes. If one is also trying to train a classifier with that many output classes, details on loss and training methods introduced in this paper should be worth looking into. This work sampled uniformly per class. When doing back propagation, due to the large class size, the back propagation operation itself takes a long time. To bypass this problem, this work suggests only back propagating for a few significant output class losses. They say it worked.
- “one verses all loss”, “multi-class logistic loss” ?? what are they talking about?
