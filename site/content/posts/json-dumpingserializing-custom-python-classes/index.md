---


title: json dumping(serializing) custom python classes
date: '2019-07-05T00:00:00+00:00'
lastmod: '2019-07-05T00:00:00+00:00'
slug: json-dumpingserializing-custom-python-classes
categories:
- python
tags:
- "class"
- "custom-class"
- "json"
- "serialization"
- "serialize"
draft: false
---
One of the greatest features of Python is that native types are naturally JSON serializable which makes it exporting/importing json files so easy and convenient without any hassle.

However, once the user starts to create their own classes and confronts the situation to dump them as a part of a JSON exportable type, then things start to get out of hand.

For example, when a project starts to get complicated and I create several classes of my own and as always, print some debugging outputs, I usually simply dump objects of interest into a json file for later inspection. This is when I face difficulties because the classes that I made are not naturally JSON serialized. Here’s an example

```python
import json

class ParentClass:

    def \_\_init\_\_(self, id, val):
        self.\_id = id
        self.\_val = val

    def tojson(self):
        return {
            "id": self.\_id,
            "val": self.\_val
        }

t = ParentClass(0, "something")

wrap = {
    "data": \[t\],
    "blah": 1
}

print(json.dumps(wrap, indent=4))

```

This results in an error:

```generic
File "/usr/lib/python3.6/json/encoder.py", line 437, in \_iterencode
    o = \_default(o)
  File "/usr/lib/python3.6/json/encoder.py", line 180, in default
    o.\_\_class\_\_.\_\_name\_\_)
TypeError: Object of type 'ParentClass' is not JSON serializable
```

AFAIK, there is no way to make my class be naturally JSON serializable. However, there is a hack for this.

The idea is to use a custom json encoder. This custom json encoder will json serialize as normal when encountering the native python object types. However, when it faces a custom class, instead of raising an error, it will check if it has `tojson` method and if it does, it will call this method and retrieve an object that consists of json serializable objects. Here is the code for this idea:

```python
import json

class ParentClass:

    def \_\_init\_\_(self, id, val):
        self.\_id = id
        self.\_val = val

    def tojson(self):
        return {
            "id": self.\_id,
            "val": self.\_val
        }

class SubClass:
    def \_\_init\_\_(self, data):
        self.\_data = data

    def tojson(self):

        return {
            "data": self.\_data
        }

class CustomEncoder(json.JSONEncoder):
    def default(self, o):

        if "tojson" in dir(o):
            return o.tojson()
        return json.JSONEncoder.default(self, o)

s= SubClass("blah")
t = ParentClass(0, s)

wrap = {
    "data": \[t\],
    "blah": 1
}

print(json.dumps(wrap, indent=4, cls=CustomEncoder))
```

And here is the result:

```json
{
    "data": \[
        {
            "id": 0,
            "val": {
                "data": "blah"
            }
        }
    \],
    "blah": 1
}
```

And it worked! Another important point to note here is how the `CustomEncoder` will also take care of subclasses that needs to be dealt in our own special way. The `SubClass` also has implemented `tojson` method which is called recursively when json serializing `ParentClass` object.

Although this approach does require the hassle of configuring the `cls` parameter whenever calling `json.dump` and ensuring that any custom classes that faces the situation of json serializing will be required to implement a `tojson` sort of method, I believe this is still the neatest way of doing it so far.
