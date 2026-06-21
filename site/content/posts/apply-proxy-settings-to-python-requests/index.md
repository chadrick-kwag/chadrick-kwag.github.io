---
title: apply proxy settings to python requests
date: '2021-03-24T00:00:00+00:00'
lastmod: '2021-03-24T00:00:00+00:00'
slug: apply-proxy-settings-to-python-requests
categories:
- python
tags:
- proxy
- requests
draft: false
---
you can apply proxy settings to python requests like this:

```generic
import requests

proxy\_dict={
    "http": "http://1.1.1.1:8080",
    "https": "https://1.1.1.1:8080"
}

resp = requests.get(some\_url, proxies=proxy\_dict)
```
