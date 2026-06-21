---
title: How to implement ctc loss using tensorflow keras (feat. CRNN example)
date: '2019-08-27T00:00:00+00:00'
lastmod: '2019-08-27T00:00:00+00:00'
slug: tf-keras-rnn-ctc-example
categories: []
tags:
- ctc-decoding
- ctc-loss
- tensorflow
- tf-keras
draft: false
---
## Code:

using tensorflow 1.14

```generic
\# train.py

model, label\_length\_ts, pred\_length\_ts, y\_true\_input\_ts= build\_model\_v1(config\["model\_input\_w"\], config\["model\_input\_h"\], config\["model\_input\_ch"\], class\_size, max\_str\_len)

ctc\_loss\_prepare\_fn = functools.partial(ctc\_loss, input\_length=pred\_length\_ts, label\_length=label\_length\_ts, real\_y\_true\_ts=y\_true\_input\_ts)

model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.0001), loss=ctc\_loss\_prepare\_fn)
```

```generic
\# build\_model.py

def build\_model\_v1(input\_width, input\_height, input\_channels, class\_size, max\_str\_len):
    """

    :param input\_width:
    :param input\_height:
    :param input\_channels:
    :param class\_size: including pseudo blank
    :return:
    """

    input = tf.keras.layers.Input((input\_height, input\_width, input\_channels),name="img\_input")

    label\_length\_input = tf.keras.layers.Input((1,),name="label\_length\_input")

    pred\_length\_input = tf.keras.layers.Input((1,),name="pred\_length\_input")

    y\_true\_input = tf.keras.layers.Input((max\_str\_len,), name="y\_true\_input")

    output = conv\_bn\_actv(input, 8, (5,5), 1, name="down\_0")

    output = tf.keras.layers.MaxPooling2D(name="pool\_0")(output)

    output = conv\_bn\_actv(output, 16, (5,5), 1, name="down\_1")

    output = tf.keras.layers.MaxPooling2D(name="pool\_1")(output)

    output = conv\_bn\_actv(output, 32, (3,3), 1, name="down\_2")

    output = conv\_bn\_actv(output, 64, (3,1), 1, name="down\_3")

    print(output.shape)

    conv\_out\_flatten = tf.keras.layers.Reshape((output.shape\[2\], output.shape\[3\]))(output)

    output = conv\_out\_flatten

    # create rnn

    output = tf.keras.layers.CuDNNLSTM(100, return\_sequences=True, name="lstm\_0")(output)

    output = tf.keras.layers.CuDNNLSTM(100, return\_sequences=True, name="lstm\_1")(output)

    output = tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(class\_size, activation="linear"), input\_shape=output.shape, name="timedist\_dense")(output)

    y\_pred = tf.keras.layers.Softmax()(output)

    model = tf.keras.Model(inputs=\[input, pred\_length\_input, label\_length\_input, y\_true\_input\],outputs=y\_pred)

    return model, label\_length\_input, pred\_length\_input, y\_true\_input
```

```generic
\# ctc\_loss.py
import tensorflow as tf

def ctc\_loss(y\_true, y\_pred, input\_length, label\_length, real\_y\_true\_ts):

    return tf.keras.backend.ctc\_batch\_cost(real\_y\_true\_ts, y\_pred, input\_length, label\_length)
```

The `tk.keras.backend.ctc_batch_cost` uses `tensorflow.python.ops.ctc_ops.ctc_loss` functions which has `preprocess_collapse_repeated` parameter. In some threads, it comments that this parameters should be set to `True` when the `tf.keras.backend.ctc_batch_cost` function does not seem to work, such as inconverging loss. However, my experience is that although setting this parameter to True may give the user the illusion that the loss is reducing, it is not actually training the model as the user intends. Please check out the docs on this parameter. For most cases, using the vanilla `tf.keras.backend.ctc_batch_cost` function is good enough.

## Input Sequence / Label Sequence

These two terms that keep appearing documents of ctc related functions and in papers are very confusing. Even once you get the general idea of why those two need to be seperated, there were several confusing moments when determining the shape and type of tensor when coding it. I think what most people, including myself a few days ago, want to know in the end is “exactly what shape/type of tensor do I need to pass on to `tf.keras.backend.ctc_batch_cost`”?

If we looks at the [docs](https://www.tensorflow.org/api_docs/python/tf/keras/backend/ctc_batch_cost):

- **`y_true`**: tensor `(samples, max_string_length)` containing the truth labels.
- **`y_pred`**: tensor `(samples, time_steps, num_categories)` containing the prediction, or output of the softmax.
- **`input_length`**: tensor `(samples, 1)` containing the sequence length for each batch item in `y_pred`.
- **`label_length`**: tensor `(samples, 1)` containing the sequence length for each batch item in `y_true`.

Here I will explain with an example.

Assume I’m training an CRNN which is what the code presented above is doing. I have a dataset of 6 with images containing texts:

[ “hat”, “cat”, “mouse”, “deer”, “tensorflow”, “good” ]

Assume using batch size of 2, and the output of convolutional layers give 25 sequences, iow 25 time slices that will be feed to the RNN.

Assume the first batch picked [“hat”, “good”].

In this case, the shape of `y_true` depends on how the user designs the data provision. Since the current batch has max_str_len of 4 (because “good” as four characters), the user can provide `y_true` to have shape of (2,4). Or since the longest str_len in the whole dataset is 10 (because “tensorflow” has ten characters), the user can provide `y_true` to have shape of (2,10). As long as the `max_string_length` used in `y_true` is same/bigger than the number of chars in the longest word(or label) in the batch, no harm done. So this raises the question: “what should be filled in the ignorable slots in `y_true`?”. Anything. It doesn’t matter. Put in zeros or -1s or 73839593 if you like. If you take a closer look in the `tf.keras.backend.ctc_batch_cost` function source code, the `y_true` and `label_length` will combine and a sparse tensor will emerge. This process will render the ignorable slots in `y_true` useless.

`y_pred` should have shape of (2, 25, class_size). BTW the class_size is “actual class size + 1” where +1 is for pseudo blank.

`input_length` will have shape of (2,1). But what should its values be? This question was the question that really gave me a hard time. Should it be equal to `label_length`? or should it be containing the values of the numbers of time slices? If so then isn’t this too obvious since the number of time slices is already available in `y_pred`? Why is this function requiring me to specify this? …. These are the questions that haunted me.

The answer was the latter. Although it does seem weird, the values of `input_length` would be [ [25], [25] ] in this example. It is a repetition of the number of time slices(or “sequence”) coming out from RNN.

`label_length` will have shape of (2,1) and as you might have guessed it, it contains the str_len for each label in the batch. For this example batch, the value will be [ [3], [4] ].

However, the documentation does not mention one of the most important rule when using ctc loss. This is mentioned in the CTC paper.

The RNN sequence length(or “number of time slices” which is **25** in this example) should be larger than `( 2 * max_str_len ) + 1`. Here **max_str_len** if the max_str_len across the entire dataset. Since the max_str_len across the entire dataset in this example is 10(“tensorflow”), and 25 > (2*10+1) is true the ctc loss design is good to go.

If this rule compromised, I’m not sure what side effects will happen but my guess is that the model will only learn to get part of the long label(or word) correct and it will not be able to predict the rest of the long label(or word). Or… perhaps something worse might happen. Haven’t tested it.

## CTC Decoding

When predicting, ctc decoding is required. Although this isn’t the most neat way of doing it, here is how it could be roughly done.

```generic
\# predict.py

pred = model.predict(input\_data)

print("pred shape: {}".format(pred.shape))
sequence\_length\_nparr = np.ones((pred.shape\[0\],),dtype="int32")
sequence\_length\_nparr \*= 27

print("sequence\_length\_nparr shape: {}".format(sequence\_length\_nparr.shape))

# create graph for ctc decoding
batch\_size = pred.shape\[0\]
y\_pred\_ph = tf.placeholder(tf.float32, shape=pred.shape)
sequence\_length\_ph = tf.placeholder(tf.int32, shape=(batch\_size,))

transposed\_pred = tf.transpose(y\_pred\_ph, perm=\[1,0,2\])
decoded, log\_prob = tf.nn.ctc\_beam\_search\_decoder(transposed\_pred, sequence\_length\_ph,merge\_repeated=True)

# print(decoded)

decoded\_dense = tf.sparse\_tensor\_to\_dense(decoded\[0\], default\_value=-1)

with tf.Session() as sess:

    decode\_output = sess.run(decoded\_dense, feed\_dict={
        y\_pred\_ph: pred,
        sequence\_length\_ph: sequence\_length\_nparr
    })
```

I’m not yet sure if I am doing this right, but the code works. This will need to be tested and studies further.
