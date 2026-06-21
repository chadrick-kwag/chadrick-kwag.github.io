---
title: supress any output from subprocess
date: '2019-11-13T00:00:00+00:00'
lastmod: '2019-11-13T00:00:00+00:00'
slug: supress-any-output-from-subprocess
categories: []
tags:
- python
- subprocess
draft: false
---
```generic
subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

this is how to suppress any output when executing a subprocess in python.
