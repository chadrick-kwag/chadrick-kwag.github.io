---
title: convert subquery columns into array of json objects
date: '2021-02-13T00:00:00+00:00'
lastmod: '2021-02-13T00:00:00+00:00'
slug: convert-subquery-columns-into-array-of-json-objects
categories:
- database
tags: []
draft: false
---
```generic
SELECT json\_agg(t) FROM t
for a JSON array of objects, and

SELECT
    json\_build\_object(
        'a', json\_agg(t.a),
        'b', json\_agg(t.b)
    )
FROM t
```
