---


title: combine error message and tracestack into one string in python Exception
date: '2019-07-25T00:00:00+00:00'
lastmod: '2019-07-25T00:00:00+00:00'
slug: combine-error-message-and-tracestack-into-one-string-in-python-exception
categories:
- python
tags:
- "error-string"
- "exception-string"
- "exception-traceback"
- "exception-traceback-and-message"
- "message"
draft: false
---
```generic
import traceback

def get\_full\_string\_of\_exception(e):
    tb = e.\_\_traceback\_\_
    tb\_lines = traceback.format\_tb(tb)
    tb\_str=""
    for line in tb\_lines:
        tb\_str += line + "\\n"

    full\_string = "{}\\n{}".format(str(e), tb\_str)

    return full\_string
```
