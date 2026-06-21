---
title: adding pip config file in virtualenv
date: '2021-04-20T00:00:00+00:00'
lastmod: '2021-04-20T00:00:00+00:00'
slug: adding-pip-config-file-in-virtualenv
categories: []
tags:
- pip-conf
- proxy
- virutalenv
draft: false
---
after creating a virtualenv, one can setup `pip.conf` file right inside the created virtualenv directory. Here’s an example

```generic
$ virtualenv -p python3 testenv
$ cd testenv
$ vi pip.conf
```

An example of `pip.conf` that I use commonly is shown below. The “index-url” may not be necessary since it is the default value, but in case it is overwritten by the system global default, then you may need it in some cases.

Adding “trusted-host” option allows to avoid SSL verification for the repository urls.

“proxy” option is optional, and use it when you have to go through a proxy to acquire internet connection.

```generic
\[global\]
index-url=https://pypi.python.org/simple/
trusted-host=files.pythonhosted.org pypi.org
proxy=http://localhost:8007
```
