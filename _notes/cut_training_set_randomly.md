---
date: 2020-06-15
title: making training datasets
---

One technique I adopted in my Aviation project, as an example in the [notebook here](https://github.com/namoopsoo/aviation-pilot-physiology-hmm/blob/master/notes/2019-12-14--annotated.md), was shuffling my training datasets to impact the distribution of examples in mini batches used during training.

And a fine point here is that instead of shuffling  training sets in place, in the below snipped, we are just shuffling the indices, which is less time consuming.

```python
indices = np.random.choice(range(size), size=size, replace=False)
```

```python
# shuffle...
size = X_train.shape[0]
print(size)
indices = np.random.choice(range(size), size=size, replace=False)
X_train_shfl = X_train[indices]
Ylabels_train_shfl = Ylabels_train[indices].astype('int64')
```
