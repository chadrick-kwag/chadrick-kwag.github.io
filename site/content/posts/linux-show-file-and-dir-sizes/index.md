---


title: linux show file and dir sizes
date: '2023-08-23T00:00:00+00:00'
lastmod: '2023-08-23T00:00:00+00:00'
slug: linux-show-file-and-dir-sizes
categories:
- linux
tags:
- "file"
- "dir"
- "sizes"
draft: false
---
For current dir

```
$ du -sh .
```

for file and dirs in current path, with max depth 1

```
$ du -h -d 1
```

or just simply(h, d, 1 args merged as one)

```
$ du -hd1
```
