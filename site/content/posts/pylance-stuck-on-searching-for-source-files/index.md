---
title: pylance stuck on "Searching for source files"
date: '2022-07-31T00:00:00+00:00'
lastmod: '2022-07-31T00:00:00+00:00'
slug: pylance-stuck-on-searching-for-source-files
categories:
- python
tags:
- pylance
- stuck
- visual-code
- vscode
draft: false
---
while using vscode, I noticed that pylance wasn’t running even after forcing pylance server restart. I checked the output logs and it was stuck at this line:

```
(10968) Searching for source files
```

# solution

add `pyrightconfig.json` on project root dir.

Here is a [link](https://github.com/microsoft/pyright/blob/main/docs/configuration.md) to github explaning about what this file is.

populate `exclude` field with directories that contain large, non source, etc files that you don’t want pylance to look into.

in my case, I had a directory that had no python files but a large dataset file. Adding these dirs to `exclude` immediately solve my issue.
