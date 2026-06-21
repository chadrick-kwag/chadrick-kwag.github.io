---
title: allowing utf8 characters in python csv writer
date: '2020-11-05T00:00:00+00:00'
lastmod: '2020-11-05T00:00:00+00:00'
slug: allowing-utf8-characters-in-python-csv-writer
categories:
- python
tags:
- csv
- python
- utf8
draft: false
---
reference: <https://stackoverflow.com/questions/46551955/python-3-csv-utf-8-encoding>

```generic
with open('sample.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvfile.write('\\ufeff')
```

do this at the start of csv writer to ad BOM
