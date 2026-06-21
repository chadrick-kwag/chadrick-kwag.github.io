---
title: get attribute/inner html of html element in python selenium
date: '2020-03-29T00:00:00+00:00'
lastmod: '2020-03-29T00:00:00+00:00'
slug: get-attribute-inner-html-of-html-element-in-python-selenium
categories:
- python
tags:
- getattribute
- selenium
draft: false
---
If we had the following html,

```html
<html>
...
<div value='1000'>what?</div>
</html>
```

we can extract ‘value’ attribute and innerhtml with the following sample python code.

```python
element = driver.find\_element\_by\_id('cityCode')

# get attribute named 'value'
value = element.get\_attribute('value')  # 1000

# get inner html
innerhtml = element.get\_attribute('innerHTML')  # 'what?'
```
