---
title: best path(greedy) vs. beam width search ctc decoding
date: '2019-09-26T00:00:00+00:00'
lastmod: '2019-09-26T00:00:00+00:00'
slug: best-pathgreedy-vs-beam-width-search-ctc-decoding
categories: []
tags:
- ctc-decoding
draft: false
---
While training CRNN for text prediction, I found that best path decoding predicts more properly and clearly compared to beam width.  
Beam width decoding results tended to be excessively messy.
