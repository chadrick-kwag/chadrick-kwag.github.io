---


title: positioning footprints in wanted places and updateing it in gui of pcbnew
date: '2019-11-24T00:00:00+00:00'
lastmod: '2019-11-24T00:00:00+00:00'
slug: positioning-footprints-in-wanted-places-and-updateing-it-in-gui-of-pcbnew
categories:
- python
tags:
- "pcbnew"
- "positioning"
- "footprints"
- "wanted"
- "places"
draft: false
---
here is a sample code

```generic
import pcbnew, re
board = pcbnew.GetBoard()
modules = board.GetModules()

interested\_modules=\[\]

for mod in modules:
    print(mod.GetReference())

diode\_r = re.compile(r".\*D\\d+")

for mod in modules:
    if diode\_r.match(mod.GetReference()):
        interested\_modules.append(mod)

pklfile = "D:\\projects\\circleproblem\\\\triangular\_points.txt"

with open(pklfile, 'r') as fd:
    lines = fd.readlines()

points=\[\]

for line in lines:
    if line\[-1\]=='\\n':
        line=line\[:-1\]
    splitted = line.split(' ')
    x = float(splitted\[0\])
    y = float(splitted\[1\])
    points.append(\[x,y\])

# SetPosition

scale= 1000000

for i, point in enumerate(points):
    selmod = interested\_modules\[i\]
    # x,y = point
    x,y = point
    x \*= scale
    y \*= scale
    wxp = pcbnew.wxPoint(x,y)
    
    selmod.SetPosition(wxp)

# update the gui to show updated positions
pcbnew.Refresh()
```

The last line does the trick of updating the changes made to be fully applied on to the pcbnew workscreen.
