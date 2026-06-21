---


title: reading yaml files in python
date: '2021-03-23T00:00:00+00:00'
lastmod: '2021-03-23T00:00:00+00:00'
slug: reading-yaml-files-in-python
categories:
- python
tags:
- "yaml"
- "reading"
- "files"
draft: false
---
instlal PyYAML

```generic
$ pip install PyYAML
```

in python file, load file like the following

```generic
import yaml

somefile = '/path/file'

data = yaml.full\_load(somefile)
```

the data in yaml file will be saved in `data` variable as a python dict.
