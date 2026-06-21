---
title: python list, list of list value test
date: '2019-04-09T00:00:00+00:00'
lastmod: '2019-04-09T00:00:00+00:00'
slug: python-list-list-of-list-value-test
categories:
- python
tags: []
draft: false
---
```python
def f1():

    return \[\[\]\]

def f2():
    return \[\]

result = f1()
result2 = f2()

print(result)
print(result2)

if result is None:
    print("result is None")
else:
    print("result is not None")

if result2 is None:
    print("result2 is none")
else:
    print("result2 is not none")

if result:
    print("result is regarded not False")
else:
    print("result is regarded as false")

if result2:
    print("result2 is regarded not False")
else:
    print("result2 is regarded as false")

```

the result:

```generic
\[\[\]\]
\[\]
result is not None
result2 is not none
result is regarded not False
result2 is regarded as false

```
