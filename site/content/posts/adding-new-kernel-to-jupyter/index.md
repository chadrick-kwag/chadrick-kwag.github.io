---


title: adding new kernel to jupyter
date: '2023-10-20T00:00:00+00:00'
lastmod: '2023-10-20T00:00:00+00:00'
slug: adding-new-kernel-to-jupyter
categories:
- python
tags:
- "jupyter"
- "kernel"
draft: false
---
create a virutalenv and activate it.

then install `ipykernel`

once installed then run the following command

```
python -m ipykernel install --user --name <some_unique_name_for_kernel>
```

related doc: <https://ipython.readthedocs.io/en/stable/install/kernel_install.html#kernels-for-different-environments>

once this is done, then you can see that this kernel is available in jupyter. It may take a few seconds for this to take into effect.

remember, run the above command when the virtualenv that you wish to add is activated.

## What happens under the hood

jupyter is just a client and ipykernel is what receives workload from jupyter client and runs them.

then where are the multiple kernels of ipykernel stored?

by default it is stored in `~/.local/share/jupyter`

The `python -m ipykernel install xxx` command does is simply add a `kernel.json` file under `~/.local/share/jupyter/kernels/<created kernel name>` dir.

The `kernel.json` file content is simple and its purpose is designating the python env that the kernel uses.

```
{

 "argv": [
  "/home/chadrick/miniconda3/envs/new_kernel/bin/python",
  "-m",
  "ipykernel_launcher",
  "-f",
  "{connection_file}"
 ],
 "display_name": "new_kernel",
 "language": "python",
 "metadata": {
  "debugger": true
 }
}
```

related docs: <https://jupyter-client.readthedocs.io/en/latest/kernels.html#kernel-specs>
