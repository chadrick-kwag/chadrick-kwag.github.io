---
title: get git short hash in python
date: '2021-12-10T00:00:00+00:00'
lastmod: '2021-12-10T00:00:00+00:00'
slug: get-git-short-hash-in-python
categories:
- python
tags:
- git
- hash
- python
draft: false
---
```python
def git\_short\_hash():

    cmd = "git rev-parse --short HEAD"

    result = subprocess.run(cmd.split(" "), capture\_output=True)

    if result.returncode == 0:
        hash = result.stdout.decode()
        if hash\[-1\] == "\\n":
            hash = hash\[:-1\]
        return hash
    else:
        None
```
