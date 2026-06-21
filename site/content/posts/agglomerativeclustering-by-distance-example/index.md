---


title: AgglomerativeClustering by distance example
date: '2018-12-05T00:00:00+00:00'
lastmod: '2018-12-05T00:00:00+00:00'
slug: agglomerativeclustering-by-distance-example
categories:
- machine-learning
tags:
- "agglomerative-clustering"
- "clustering"
- "agglomerativeclustering"
- "distance"
draft: false
---
```python
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
import matplotlib.pyplot as plt

test\_values = \[20, 14, 19, 19, 19, 18, 17, 19, 19, 103, 105, 84, 83, 108, 75, 80, 92, 78\]

x = \[\[i\] for i in test\_values\]

Z = linkage(x, method='ward')

plt.figure()
dendrogram(Z)
plt.show()

clusters = fcluster(Z, 10, criterion='distance')

cluster\_result={}

for index, cluster\_id in enumerate(clusters):
    val = test\_values\[index\]
    fetch\_list = cluster\_result.get(cluster\_id,None)

    if fetch\_list is None:
        fetch\_list=\[val\]
        cluster\_result\[cluster\_id\] = fetch\_list
    else:
        fetch\_list.append(val)

print(cluster\_result)

```
