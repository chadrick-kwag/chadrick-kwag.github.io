---
title: 'webpack dev server run error "Error: spawn chrome ENOENT"'
date: '2020-03-08T00:00:00+00:00'
lastmod: '2020-03-08T00:00:00+00:00'
slug: webpack-dev-server-run-error-error-spawn-chrome-enoent
categories:
- web
tags:
- webpack-dev-server-chrome-enoent
- webpack-dev-server-error
draft: false
---
# Problem

I had a react project that was originally worked in windows environment. I migrated to ubuntu environment and attempted to start project with webpack-dev-server. After installing all npm packages, I encoured the following error

```generic
$ npx webpack-dev-server
ℹ ｢wds｣: Project is running at http://localhost:8080/
ℹ ｢wds｣: webpack output is served from /
ℹ ｢wds｣: Content not from webpack is served from /home/chadrick/prj/web/timeline2
events.js:167
      throw er; // Unhandled 'error' event
      ^

Error: spawn chrome ENOENT
    at Process.ChildProcess.\_handle.onexit (internal/child\_process.js:232:19)
    at onErrorNT (internal/child\_process.js:407:16)
    at process.\_tickCallback (internal/process/next\_tick.js:63:19)
Emitted 'error' event at:
    at Process.ChildProcess.\_handle.onexit (internal/child\_process.js:238:12)
    at onErrorNT (internal/child\_process.js:407:16)
    at process.\_tickCallback (internal/process/next\_tick.js:63:19)
```

# Solution

This was caused because of my webpack-dev-server `open` config. Here is the devserver config in `webpack.config.js`

```generic
devServer: {
        open: 'chrome',
        index: "template.html"
    }
```

The problem was that I have set `open` to `"chrome"` which was the binary filename for opening chrome in **windows**. In ubuntu, the binary command for opening chrome is `google-chrome`.

After I changed the value of `open` to `google-chrome`, the webpack-dev-server start worked.

```generic
devServer: {
        open: 'google-chrome',
        index: "template.html"
    }
```
