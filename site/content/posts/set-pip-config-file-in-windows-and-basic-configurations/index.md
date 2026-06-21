---
title: set pip config file in windows and basic configurations
date: '2020-03-26T00:00:00+00:00'
lastmod: '2020-03-26T00:00:00+00:00'
slug: set-pip-config-file-in-windows-and-basic-configurations
categories: []
tags:
- pip-config
- pip-ini
- windows
draft: false
---
# Setup

create `pip.ini` file in `C:\Users\Username\pip` directory.

This directory may not exist, if so, then create one manually.

here are some common configurations that I add to the config file.

```generic
\[global\]
trusted-host = 5.6.7.8 pypi.org files.pythonhosted.org
proxy = 8.7.8.7:8080
```

if multiple values should be set for one key, add a space between items like I did with `trusted-host`.

# check if config is read

in terminal, run command like below to check if configuration from `pip.ini` has been loaded.

```generic
$ pip config list
global.proxy='8.7.8.7:8080'
global.trusted-host='5.6.7.8 pypi.org files.pythonhosted.org'
```
