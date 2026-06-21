---
title: add tokens to huggingface tokenizer
date: '2022-06-02T00:00:00+00:00'
lastmod: '2022-06-02T00:00:00+00:00'
slug: add-tokens-to-huggingface-tokenizer
categories:
- machine-learning
tags:
- huggingface
- tokenizer
- tokens
draft: false
---
Here’s a sample code of how to load huggingface tokenizer, add some custom tokens and save it.

```python
from transformers import XLMRobertaTokenizer
import os, shutil

t\_dir = "/some/path/xlm-roberta-base"

tokenizer = XLMRobertaTokenizer.from\_pretrained(t\_dir)

original\_length = len(tokenizer)

print(f"before mod length: {original\_length}")

special\_tokens\_to\_add = \["\[custom1\]", "\[custom2\]"\]

tokenizer.add\_tokens(special\_tokens\_to\_add, special\_tokens=True)

print(f"after modification length: {len(tokenizer)}")

# create outputdir
outputdir = "testoutput/pretrain\_tokenizer"

if os.path.exists(outputdir):
    shutil.rmtree(outputdir)

os.makedirs(outputdir)

tokenizer.save\_pretrained(outputdir)

# reload and check

tokenizer = XLMRobertaTokenizer.from\_pretrained(outputdir)

print(f"> reload tokenizer length: {len(tokenizer)}")

print("done")

```
