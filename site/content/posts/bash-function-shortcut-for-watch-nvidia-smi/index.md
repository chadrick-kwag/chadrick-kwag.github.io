---


title: bash function shortcut for watch nvidia-smi
date: '2021-03-11T00:00:00+00:00'
lastmod: '2021-03-11T00:00:00+00:00'
slug: bash-function-shortcut-for-watch-nvidia-smi
categories:
- linux
tags:
- "bash"
- "nvidia-smi"
- "nvmon"
- "function"
- "shortcut"
draft: false
---
add the following to `.bashrc` or `.bash_aliases`

```generic
nvmon (){
	watch -n 0.1 nvidia-smi
}
```
