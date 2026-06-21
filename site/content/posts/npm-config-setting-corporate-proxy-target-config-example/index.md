---
title: npm config setting (corporate proxy target config example)
date: '2020-03-04T00:00:00+00:00'
lastmod: '2020-03-04T00:00:00+00:00'
slug: npm-config-setting-corporate-proxy-target-config-example
categories: []
tags:
- npm
- npm-config
- npm-config-corporate
- npm-proxy
draft: false
---
if you are in a corporate environment, then there is a high chance that you will have to bypass through a specific proxy with a cert file or worse, public internet access is completely shutoff and you can only access a repository setup by the corporate.

Under these circumstances, here are key npm config options that you might want to fiddle around with. At the same time, this guide will show you how to set npm options.

there are various ways to set npm config but I will be useing the terminal method. The following is the template for the command.

```generic
$ npm config set <key> <value>
```

The config options that may be useful for a corporate environment are

```generic
$ npm config set proxy 3.4.5.6:8899
$ npm config set https-proxy 3.4.5.6:8899
$ npm config set cafile c:\\\\somewhere\\\\some.crt
$ npm config set strict-ssl false
$ npm config registry http://somewhere/repo
```

not all of them may not be necessary. choose the ones that fits your needs.
