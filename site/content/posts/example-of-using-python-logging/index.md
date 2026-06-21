---
title: example of using python logging logger
date: '2018-11-14T00:00:00+00:00'
lastmod: '2018-11-14T00:00:00+00:00'
slug: example-of-using-python-logging
categories: []
tags:
- logger
- logging
- python
draft: false
---
at the main script, insert the code below to setup a logger named `debug`.

```
# inside `main.py`. and example main script file

debuglogger = logging.getLogger("debug")
debuglogger.setLevel(logging.DEBUG)

debuglogger_fh = logging.FileHandler("debug.log",mode='w')
debuglogger_fh.setLevel(logging.DEBUG)

FORMAT = '%(asctime)-15s %(funcName)-20s > %(message)s'
formatter = logging.Formatter()

debuglogger_fh.setFormatter(formatter)

debuglogger_sh = logging.StreamHandler(sys.stdout)
debuglogger_sh.setLevel(logging.DEBUG)

debuglogger.addHandler(debuglogger_fh)
debuglogger.addHandler(debuglogger_sh)

...

# do some main stuff
```

In the above code, I have set the `debug` logger to print its text to both sys.stdout(providing the same effect as a normal `print`) and to a file `debug.log`. Note that when writing to this external file, I have set the writing mode to `w` indicating that whenever this logger is setup, it will overwrite if a file named `debug.log` already exists. If I used the `a` option as the mode, then it will append to the already existing file with the same name.

Once our `debug` logger is setup in the main script, then you can fetch this logger from anywhere in your python files(not only the main script file) and push a log message to it.

For example, lets say that in the main script file I have imported a python module(which is identical to a python file) named `some_external`. If I wanted to print some debug messages in this module, instead of using `print`, I can do the following:

```
# this is `some_external.py`
import logging

debuglogger = logging.getLogger("debug")

def some_func1():
    # do something
    # and I want to print some debug messages

    debuglogger.debug("yikes")

```

Notice that in this `some_external.py`, the code only fetches a logger named `debug` and doesn’t configure this logger. That is because the configuration(adding handlers, adding formatters, etc.) is meant and will be done in the main sript file. And this totally make sense because `some_external.py` file isn’t meant to play a role as a main execution script but rather just a side-module that stores numerous functions. That is why `some_external.py` should only utilize a reference to some logger and do not need to care anything about the specific configurations of the logger.
