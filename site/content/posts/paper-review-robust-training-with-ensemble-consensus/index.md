---
title: 'paper review: Robust Training with Ensemble Consensus'
date: '2020-05-25T00:00:00+00:00'
lastmod: '2020-05-25T00:00:00+00:00'
slug: paper-review-robust-training-with-ensemble-consensus
categories: []
tags:
- paper-review
draft: false
---
pdf link: <https://arxiv.org/pdf/1910.09792.pdf>

# Key Idea

- deep neural networks learn to generalize but also memorize noisy cases, which is bad.
- if the DNN is generalized to clean samples, then adding some perturbation to these samples would not increase loss significantly.
- But for memorized noisy cases, adding some perturbation would increase loss significantly.
- Using this phenomenon, after training the DNN(warmup stage), cull out noisy samples in the training dataset and train with survived samples.
- Think of “noisy” samples mentioned in this paper as “not learned but overfitted” samples.
- The intention is that repeating this process will remove “noisy” samples that have been memorized by the network and in the next training phase, the network will have been removed of its bad habits since the culprit noisy samples have been removed.
- But by intuition, there is a dange of what if this learning procedure removes clean samples instead of noisy samples?
- The paper addresses this problem and says that they have experimented this and such bad scenario did not happen. Hmm… I’m not sure if I can blindly take their word for it. But then again, they start applying their proposed technique after a warmup phase which should guarantee some level of clean sample generalization.
