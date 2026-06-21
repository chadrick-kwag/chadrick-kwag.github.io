---
title: visual code python debugging configuration
date: '2021-04-30T00:00:00+00:00'
lastmod: '2021-04-30T00:00:00+00:00'
slug: visual-code-python-debugging-configuration
categories:
- python
tags:
- debugging
- launch-json
- python
- python-debug
- visual-code
- vscode
draft: false
---
creating the most basic `launch.json` file is explained well in official docs.

# changing execution path

However what I really wanted to know was how to configure it to make it run debugging on a file from a specific directory path.

For example, I have a workspace structure like this.

```generic
workspace\_root/
  - main.py
  - utils.py
  - subdir1/
    - t1.py
```

And `t1.py` file imports `utils.py` like this

```generic
import os, sys
sys.path.append(os.path.abspath('..'))

from utils import some\_func1

### blahblah
```

In this case, `t1.py` is configured to run from `workspace_root/subdir` and not from `workspace_root/`, and this is not the way the default `launch.json` will work.

Adding `cwd` option fixed this problem. In this example, the following `cwd` option will set the debugging to run from the directory where the running file exists.

```generic
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": \[
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${fileDirname}"
        }
    \]
}
```

## passing arguments

If I have a python script that takes in command line arguments in order to execute them, I would also want to pass arguments when debugging such a python file. For example, if I created a python file that normally executes like this

```
$ python test.py /path/to/config/file
```

In this case, we can setup the vscode `launch.json` file like this by adding the `args` option

```generic
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": \[
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${fileDirname}",
            "args": \["/some/path/testconfig.yaml"\]
        }
    \]
}
```
