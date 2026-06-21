---
title: 'paper review: Explaining and Harnessing Adversarial Examples (FGSM adversarial
  attack)'
date: '2019-12-11T00:00:00+00:00'
lastmod: '2019-12-11T00:00:00+00:00'
slug: paper-review-explaining-and-harnessing-adversarial-examples-fgsm-adversarial-attack
categories: []
tags:
- adversarial-example
- adversarial-fgsm
- adversarial-sample
- fgsm
draft: false
---
paper link: <https://arxiv.org/abs/1412.6572>

This paper introduces Fast Gradient Signed Method(FGSM) adversarial attack along with some useful insights on why linearity of deep learning networks would allow such attacks.

The FGSM method is regarded as the method introduced after using L-BGFS method to generate adversarial samples. These two share similar ideas on how to generate adversarial samples but their methods do differ. This paper mentions that the L-BGFS method has disadvantages in terms of optimization time/computation cost.

So instead, this paper proposes FGSM which is much easier and faster to implement. The idea is simple. Obtaining gradients using back propagation against pretty much any variable against the loss functions is a basic part of deep learning training process. So why not just find the gradients of the input against the loss function and add perturbation along that gradient’s direction? Though this simple approach we can effectively disrupt the correct classification logits.

The idea is simple and easy to implement. Here is a tensorflow tutorial: [https://www.tensorflow.org/tutorials/generative/adversarial_fgsm](https://www.google.com/url?q=https://www.tensorflow.org/tutorials/generative/adversarial_fgsm&sa=D&source=hangouts&ust=1576156386205000&usg=AFQjCNHvWOhUPAvB6DyJ3DM3xNg00bZV7w)

The authors note than when training with adversarial samples, it was important to increase the capacity of the network. In other words, increase the number of node in each layer to accommodate for the extra calculations to cope with adversarial samples.

Another section of the paper describes on why such small perturbations generated either by FGSM or L-BGFS method could cause such catastrophic results. The authors suggest that the too much linearity of the deep learning models when using linear activations result in such behavior. If the activation functions were nonlinear, then such adversarial attacks would have been less effective. Through experimenting through different network structures with the same training dataset, the authors also explain the discovery that they all seem to show similar behavior to adversarial samples generated from one of the models. This discovery suggest that the linearity of these network structure is the cause of the common vulnerability to the same adversarial samples.

Here is the list of conclusions from the paper which is a superb summary of the paper:

- Adversarial examples can be explained as a property of high-dimensional dot products.
- They are a result of models being too linear, rather than too nonlinear.
- The generalization of adversarial examples across different models can be explained as a result of adversarial perturbations being highly aligned with the weight vectors of a model, and different models learning similar functions when trained to perform the same task.
- The direction of perturbation, rather than the specific point in space, matters most. Space is not full of pockets of adversarial examples that finely tile the reals like the rational numbers.
- Because it is the direction that matters most, adversarial perturbations generalize across different clean examples.
- We have introduced a family of fast methods for generating adversarial examples.
- We have demonstrated that adversarial training can result in regularization; even further regularization than dropout.
- We have run control experiments that failed to reproduce this effect with simpler but less efficient regularizers including L1 weight decay and adding noise.
- Models that are easy to optimize are easy to perturb.
- Linear models lack the capacity to resist adversarial perturbation; only structures with a hidden layer (where the universal approximator theorem applies) should be trained to resist adversarial perturbation.
- RBF networks are resistant to adversarial examples.
- Models trained to model the input distribution are not resistant to adversarial examples.
- Ensembles are not resistant to adversarial examples.
- Rubbish class examples are ubiquitous and easily generated.
- Shallow linear models are not resistant to rubbish class examples
- RBF networks are resistant to rubbish class examples.

Personally, after trying out both L-BGFS and FGSM method, FGSM is much more easier and merrier to work with. It’s much easier to implement and personally, I think it generates adversarial examples faster with less iterations on changing epsilon value.
