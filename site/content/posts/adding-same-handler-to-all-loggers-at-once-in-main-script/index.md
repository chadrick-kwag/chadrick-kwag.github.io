---


title: adding same handler to all loggers at once in main script
date: '2019-05-21T00:00:00+00:00'
lastmod: '2019-05-21T00:00:00+00:00'
slug: adding-same-handler-to-all-loggers-at-once-in-main-script
categories:
- python
tags:
- "handler"
- "logger"
- "logging"
- "same"
- "all"
draft: false
---
```python
import logging

# do all imports necessary

debuglogger\_fh = logging.FileHandler("debug.log",mode='w')
debuglogger\_fh.setLevel(logging.DEBUG)

FORMAT = '%(asctime)-15s %(funcName)-20s > %(message)s'
formatter = logging.Formatter(FORMAT)

debuglogger\_fh.setFormatter(formatter)

debuglogger\_sh = logging.StreamHandler(sys.stdout)
debuglogger\_sh.setLevel(logging.DEBUG)
debuglogger\_sh.setFormatter(formatter)

for name, item in logging.root.manager.loggerDict.items():
    if isinstance(item, logging.Logger):
        item.setLevel(logging.DEBUG)
        item.addHandler(debuglogger\_fh)
        item.addHandler(debuglogger\_sh)
```
