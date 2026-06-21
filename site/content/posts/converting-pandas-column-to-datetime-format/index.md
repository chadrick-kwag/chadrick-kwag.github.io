---
title: converting pandas column to datetime format
date: '2019-05-05T00:00:00+00:00'
lastmod: '2019-05-05T00:00:00+00:00'
slug: converting-pandas-column-to-datetime-format
categories: []
tags:
- datetime
- pandas
draft: false
---
here is a column which has timestamp in string format.

```generic
order\_purchase\_col.head()

0    2017-09-13 08:59:02
1    2017-04-26 10:53:06
2    2018-01-14 14:33:31
3    2018-08-08 10:00:35
4    2017-02-04 13:57:51
Name: order\_purchase\_timestamp, dtype: object
```

convert it to datetime format with `to_datetime` method

```generic
order\_purchase\_col = pd.to\_datetime(order\_purchase\_col)
order\_purchase\_col.head()

0   2017-09-13 08:59:02
1   2017-04-26 10:53:06
2   2018-01-14 14:33:31
3   2018-08-08 10:00:35
4   2017-02-04 13:57:51
Name: order\_purchase\_timestamp, dtype: datetime64\[ns\]
```
