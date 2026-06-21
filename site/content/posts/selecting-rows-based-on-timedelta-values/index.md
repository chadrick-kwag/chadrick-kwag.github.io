---


title: selecting rows based on timedelta values
date: '2019-05-05T00:00:00+00:00'
lastmod: '2019-05-05T00:00:00+00:00'
slug: selecting-rows-based-on-timedelta-values
categories:
- python
tags:
- "pandas"
- "timedelta"
- "selecting"
- "rows"
- "values"
draft: false
---
Assume we have a series that contains time difference values.

```generic
na\_removed\_order\_time\_diff.head()

0   00:46:33
1   00:12:07
2   00:14:59
3   00:09:43
4   00:12:22
dtype: timedelta64\[ns\]
```

Let’s find rows which have time difference more than an hour. According to the pandas documentation, the pandas timedelta is actually using the python’s `datetime` module’s timedelta.

For first make a datetime.timedelta object that contains a value of one hour and use this as a comparison against our pandas series to extract the rows that satisfy the condition.

```generic
td = datetime.timedelta(hours=1)

over\_threshold = order\_time\_diff > td

0    False
1    False
2    False
3    False
4    False
dtype: bool
```

Now we can select the rows with this array of booleans.
