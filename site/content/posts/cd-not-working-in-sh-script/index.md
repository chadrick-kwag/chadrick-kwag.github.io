---
title: cd not working in sh script
date: '2020-07-31T00:00:00+00:00'
lastmod: '2020-07-31T00:00:00+00:00'
slug: cd-not-working-in-sh-script
categories: []
tags: []
draft: false
---
## problem

I had a shell script like the following

```generic
#!/bin/sh
cd /to/somewhere
python runsomething.py
```

and I was trying to run it with `$ sh somescript.sh`

but it kept failing with the error something liek “cd: no directory”.

## Solution

After resaving the script file with LF instead of CRLF, the script worked. I was using intellij to edit the script file and by default it was CRLF.
