---
title: check ubuntu version through command line
date: '2020-08-06T00:00:00+00:00'
lastmod: '2020-08-06T00:00:00+00:00'
slug: check-ubuntu-version-through-command-line
categories:
- linux
tags: []
draft: false
---
The most popular command

```generic
$ lsb\_release -a
```

However, in some cases when `lsb_release` is not available, then use the following

```generic
$ cat /etc/issue
```
