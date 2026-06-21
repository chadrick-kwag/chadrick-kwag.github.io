---


title: implementing seq2seq RNN model in tensorflow
date: '2019-03-17T00:00:00+00:00'
lastmod: '2019-03-17T00:00:00+00:00'
slug: implementing-seq2seq-rnn-model-in-tensorflow
categories:
- machine-learning
tags:
- "tensorflow"
- "many-to-many"
- "rnn"
- "timedistributed"
- "implementing"
draft: false
---
for tackling the many-to-many(with timedistributed) is easy to implement in keras code, it does not seem to be easy to do so in pure tensorflow.

Of course, one can implement it when the sequence length is fixed for all input size. However when the sequence length among batches vary, then it becomes a problem. Since the sequence length will vary, there is high possibility that the wrapping layer that will convert the RNN block’s output to desired output dimension is going to complicate building the model.

To elaborate, image a situation where we want to get all the outputs for input sequence for all time steps. And we have a label for each time step and want to train it. This requires the model to somehow apply the last wrapping layer to every RNN block output.

If there is assurance that the sequence length(which equals to the number of time steps, and will further denote as ‘N’) is fixed for all training data, then we can build the model to create N wrapping layers for each time step RNN output. Of course this approach may not be exactly what we had in mind since this does not use the same wrapping layer for all RNN output throughout all time steps. But still, I guess it should do the trick.

However, if the sequence length varies, then we have a serious problem when building the model. Since it is uncertain how many wrapping layers will be needed at model build time, it is simply impossible to build a model in the first place.

Keras code has a function that will deal with timedistributed situations. I’m not sure exactly how this is implemented but it does the trick.

Since this API is also supported in tf.keras, we could sort of say that tensorflow can now also account for timedistributed situations but still, that isn’t exactly using pure tensorflow code in my opinion. I should look under the hood and see what really is happening.

## Things to work on…

- <https://www.tensorflow.org/api_docs/python/tf/keras/layers/TimeDistributed> : track down source code and see how it is implemented
