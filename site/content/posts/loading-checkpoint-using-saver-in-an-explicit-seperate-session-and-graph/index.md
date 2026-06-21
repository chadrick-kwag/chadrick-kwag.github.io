---


title: loading checkpoint using Saver in an explicit seperate session and graph
date: '2020-02-03T00:00:00+00:00'
lastmod: '2020-02-03T00:00:00+00:00'
slug: loading-checkpoint-using-saver-in-an-explicit-seperate-session-and-graph
categories:
- machine-learning
tags:
- "checkpoint"
- "saver"
- "explicit"
- "seperate"
- "session"
draft: false
---
```generic
graph = tf.Graph()
with graph.as\_default():
	saver = tf.train.import\_meta\_graph(metapath)

session = tf.Session(graph=graph)

self.sess = session

saver.restore(session, os.path.splitext(metapath)\[0\])
```
