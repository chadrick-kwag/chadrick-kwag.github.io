---


title: python interrupt, sigterm, sigkill, exception handling experiments
date: '2022-07-08T00:00:00+00:00'
lastmod: '2022-07-08T00:00:00+00:00'
slug: python-interrupt-sigterm-sigkill-exception-handling-experiments
categories:
- python
tags:
- "exception"
- "keyboardinterrupt"
- "kill"
- "sigint"
- "sigkill"
draft: false
---
When thinking both Exceptions and interrupts at the same time, things can get confusing so here I write down some simple experiments that I did to clear some confusing concepts.

## sigkill can’t be catched

signal handling can be done with `signal` package that is included in python by default. Last time I read the docs, there was `SIGKILL` so I blatantly thought KILL signal can also be caught. But even in the docs, [it says that it cannot catch it](https://docs.python.org/3/library/signal.html#signal.SIGKILL).

I ran this under Ubuntu environment, python3.8.10

```python
import signal

def kill\_handler(signum, frame):
    print("kill hanlder")

signal.signal(signal.SIGKILL, kill\_handler)

print("hello")
```

and the script even fails to run.

```
Traceback (most recent call last):
  File "t2.py", line 7, in <module>
    signal.signal(signal.SIGKILL, kill_handler)
  File "/usr/lib/python3.8/signal.py", line 47, in signal
    handler = _signal.signal(_enum_to_int(signalnum), _enum_to_int(handler))
OSError: [Errno 22] Invalid argument
```

## KeyBoardInterrupt cannot be catched by `try..except Exception`

I just thought Ctrl+C keyboard interrupt was just another Exception subclass, so I expected the following `catch` statement to be able to catch it but I was surprised to see that it didn’t.

```python
import signal

try:
    print("entering loop")
    while True:
        pass
except Exception as e:
    print("exception catched")
```

output:

```
entering loop
^CTraceback (most recent call last):
  File "t2.py", line 6, in <module>
    pass
KeyboardInterrupt
```

As you can see the KeyboardInterrupt was not catched by `except Exception ...` statement.

From the python [docs](https://docs.python.org/3/library/exceptions.html#KeyboardInterrupt):

> *exception* `KeyboardInterrupt`  
> Raised when the user hits the interrupt key (normally Control-C or Delete). During execution, a check for interrupts is made regularly. The exception inherits from [`BaseException`](https://docs.python.org/3/library/exceptions.html#BaseException) so as to not be accidentally caught by code that catches [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception) and thus prevent the interpreter from exiting.

So I have mistaken `KeyboardInterrupt` as a subclass of `Exception` when it wasn’t. The proper way to handle this exception would be:

```python
try:
    print("entering loop")
    while True:
        pass
except KeyboardInterrupt:
    print("keyboardinterrupt detected")
except Exception as e:
    print("exception catched")
```

output:

```
entering loop
^Ckeyboardinterrupt detected
```

## SIGINT signal handler comes first than `except KeyboardInterrupt`

However, `signal` package also allows to handle keyboard interrupts through `SIGINT`. In this case which one would be prioritized? The following code puts this to the test:

```python
import signal, sys

def int\_handler(signum, frame):
    print("sigint handler")
    sys.exit(0)

signal.signal(signal.SIGINT, int\_handler)

try:
    print("entering loop")
    while True:
        pass
except KeyboardInterrupt:
    print("keyboardinterrupt detected")
except Exception as e:
    print("exception catched")

```

output:

```
entering loop
^Csigint handler
```

The SIGINT handler comes first.

## SIGTERM handler works when terminated from outside

say we run the following script:

```python
import signal, sys, os

def term\_handler(signum, frame):
    print("sig term handler")
    sys.exit(0)

signal.signal(signal.SIGTERM, term\_handler)

print(f"pid: {os.getpid()}")
print("entering loop")
try:
    while True:
        pass
except Exception as e:
    print("exception detected")
except BaseException:
    print("base exception detected")

# output:
# pid: 18927
# entering loop

```

and from another shell, we terminate (not kill) it with cmd:

```
$ sudo kill 18927
```

then we get the following output from the python script running terminal:

```
pid: 18927
entering loop
sig term handler
base exception detected
```

we can confirm that SIGTERM is handled well as expected and is not somehow filtered by `except Exception`. But surprisingly even after sigint handler, it is caught by `except BaseException` statement. As it turns out, the BaseException was raised by `sys.exit(0)` in the sigint handler. I guess the calling of sigint handler was still inside the context of `try...except` and thus the call of `sys.exit(0)` triggered `except BaseException`.

## SIGTERM handler is not triggered by killing the process from outside

With the same code above, I tested `$ sudo kill -9 <pid>` which sends a KILL signal instead of TERMINATE signal. The result terminal output was something like this:

```
pid: 19738
entering loop
Killed
```

As expected, it failed to even call sigint handler.
