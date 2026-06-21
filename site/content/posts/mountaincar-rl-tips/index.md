---
title: mountaincar RL tips
date: '2020-01-03T00:00:00+00:00'
lastmod: '2020-01-03T00:00:00+00:00'
slug: mountaincar-rl-tips
categories: []
tags:
- mountaincar
- reinforcement-learning
draft: false
---
when adding samples, I modified the reference code to exclude  
terminating status samples in hope that this would less complicate the batch creation process.

the original code:

```generic
self.samplestorage.add\_sample(state, action, reward, next\_state)
```

the modified code:

```python
if done:
    pass
else:
    self.samplestorage.add\_sample(state, action, reward, next\_state)
```

However, this small change made a huge difference in training convergence.

The modification failed to ever get the total reward for each episode to increase.

The original code was able to learn something and increase its total reward per episode after a few episode runs.

So the tip here is to always include the terminating sample even though the termination does not mean accomplishing the ultimate objective.

reference code: <https://github.com/adventuresinML/adventures-in-ml-code/blob/master/r_learning_tensorflow.py>
