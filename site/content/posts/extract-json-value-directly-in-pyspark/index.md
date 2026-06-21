---
title: extract json value directly in pyspark
date: '2023-08-11T00:00:00+00:00'
lastmod: '2023-08-11T00:00:00+00:00'
slug: extract-json-value-directly-in-pyspark
categories: []
tags: []
draft: false
---
Say a spark dataframe has a column named `json_str_col` which contains json format strings, and the json format string have the format {“key1” : “some value”}

we can directly extract `key1` ’s values as a new column with the following.

```python
df.withColumn('value1', F.get\_json\_object(F.col('json\_str\_col'), '$.key1'))
```
