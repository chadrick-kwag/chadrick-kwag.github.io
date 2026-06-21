---
title: 'headless chrome driver: puppeteer'
date: '2020-03-04T00:00:00+00:00'
lastmod: '2020-03-04T00:00:00+00:00'
slug: headless-chrome-driver-puppeteer
categories: []
tags:
- chromium
- headless-chrome
- puppeteer
draft: false
---
this is a npm package which allows to launch a chromium process headlessly and allowing powerful control over it. It is reallly useful for taking screenshots since this can capture the entire page(not just the visible portion). And it can do more than just take screenshots because the package is actually launching a fullsize chromium process which is just like a normal browser.

The potential of this package is endless…

<https://github.com/puppeteer/puppeteer>

# having trouble auto-downloading chromium with npm install?

In some cases, such as working behind a corporate environment, you may find `npm install puppeteer` fail due to unable to download chromium directly. In this case, there is a workaround which I underwent myself and can confirm that it does work.

<https://github.com/puppeteer/puppeteer/issues/2173#issuecomment-372727628>

this is the comment that explains the details. One difficulty might be finding the release code of chrominum that will fit with puppeteer version that you are trying to install. In the error message output from `npm install puppeteer`, it will show the release version that it attempted to download. In my case, it was `r722234`. The chromium download link in the comment is outdated. The following is the link that I used so please adjust the relase version code appropriately.

<https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/722234/>

or you could just goto `https://commondatastorage.googleapis.com/chromium-browser-snapshots` and dig around.

Another tip is instead of modifying the environment variables to avoid downloading chromium when calling `npm install puppeteer`, you can just call `npm install puppeteer-core` which does exactly that. But if you did this, then when you are importing the package in your javascript file, you will have to use the following `require` line.

```generic
// const pup = require('puppeteer') <-- instead of this, use:
const pup = require('puppeteer-core')
```
