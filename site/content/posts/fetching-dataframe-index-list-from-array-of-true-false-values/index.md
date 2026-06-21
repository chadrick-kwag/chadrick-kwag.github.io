---


title: fetching dataframe index list from array of True/False values
date: '2019-05-04T00:00:00+00:00'
lastmod: '2019-05-04T00:00:00+00:00'
slug: fetching-dataframe-index-list-from-array-of-true-false-values
categories:
- python
tags:
- "pandas"
- "dataframe"
- "index"
- "list"
- "array"
draft: false
---
While working with Pandas dataframes, I encountered a situation where I needed to locate the row indexes that satisfy a certain condition so that I could later drop them from the dataframe.

Getting a True/False series for the entire index of a dataframe can be done various based on the user’s needs, but for this example a True/False series of wether a row contains a NaN value or not will be used.

Here’s the trick to do it.

```python
isna\_bool\_list = data.isna().any(axis=1)

pop\_row\_index\_list = data.index\[isna\_bool\_list\]
pop\_row\_index\_list.tolist()
```

Later on, if I wanted to drop the rows with these indices, then I could do something like this:

```generic
data4 = data.drop(data.index\[pop\_row\_index\_list\])
print(data4.shape)
print(data.shape)

>> output
(682, 9)
(768, 9)
```

There is another way which is using numpy functions but its messy so I recommend using this approach.
