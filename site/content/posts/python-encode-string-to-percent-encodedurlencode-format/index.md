---
title: python encode string to percent encoded(urlencode) format
date: '2021-03-15T00:00:00+00:00'
lastmod: '2021-03-15T00:00:00+00:00'
slug: python-encode-string-to-percent-encodedurlencode-format
categories: []
tags:
- percent-encode
- python
- urlencode
draft: false
---
reference: <https://www.urlencoder.io/python/>

```generic
\>>> import urllib.parse
>>> query = 'Hellö Wörld@Python'
>>> urllib.parse.quote(query)
'Hell%C3%B6%20W%C3%B6rld%40Python'
```
