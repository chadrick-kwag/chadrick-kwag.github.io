---


title: release cached dataframe in pyspark
date: '2023-08-11T00:00:00+00:00'
lastmod: '2023-08-11T00:00:00+00:00'
slug: release-cached-dataframe-in-pyspark
categories:
- database
tags:
- "caching"
- "release"
- "cached"
- "dataframe"
- "pyspark"
draft: false
---
to release all cached dataframes use the following

```python
spark.catalog.clearCache()
```

reference: <https://sparkbyexamples.com/spark/spark-drop-dataframe-from-cache/>
