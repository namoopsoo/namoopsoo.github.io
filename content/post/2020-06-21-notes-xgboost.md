---
date: 2020-06-21
title: Some xgboost notes so far
---

#### Let's summarize
I want to just summarize some learnings [from](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-07-quick-mvp-xgboost--snapshot-2020-06-10T0239Z.md) [some](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-10-again.md) [of](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-12--snapshot-2020-06-14T2258Z.md) [my](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-14.md) [recent](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-16.md) [notebooks](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-19.md) [yea](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-20.md).

I have picked up my bike share data learning project from earlier, to try to redo it after having gathered more experience. I want to just jot down some ad hoc thoughts here.

This is mainly around navigating XGBoost.

#### There are two XGBoost APIs
With the sklearn API you can

```python
import xgboost as xgb
from xgboost import XGBClassifier
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss

X, y = np.random.random(size=(1000, 3)), np.random.choice([1, 0], size=(1000,), replace=True)
X_train, X_test, y_train, y_test = train_test_split(X, y)
model = XGBClassifier().fit(X_train, y_train)
y_pred_prob = model.predict_proba(X_test)
y_pred = np.argmax(y_pred_prob, axis=1)
acc = accuracy_score(y_test, y_pred)
print(acc)
```

And you can also just

```python
params = {'max_depth': 2, 'eta': 1, 'objective': 'binary:logistic'}
dtrain = xgb.DMatrix(X_train, labels=y_train)
dtest = xgb.DMatrix(X_test)
bst = xgb.train(params, dtrain, num_round=2)
y_pred = bst.predict(dtest)

```

The sklearn API I believe uses `100` rounds/iterations/epochs (I have seen these used interchangeably) by default, and the `xg.train` method let's you specify that. I am not sure how to override that w/ the sklearn wrapper.

The sklearn API starts you off with a bunch of default parameters that appear to be different than the raw parameters.

#### Learning continuation is not a good method for batch learning
I tried to split up my data into chunks and use this approach to batch learn..

```python
def batch_train(X, y)
    parts = [range(1000), range(1000, 2000), range(2000, 3000)]
    prev_model_loc = None
    model = XGBClassifier()
    for i, part in enumerate(parts):
        model.fit(X[part], y[part], xgb_model=prev_model_loc)

        prev_model_loc = f'model.xg'
        model.save_model(prev_model_loc)

    return model
```

With about half a million rows, training was doable in one go and it took maybe `7 minutes`. But when I tried to "batch" this into  `10k` sections, this lasted for `8 hours` . Luckily I was sleeping and kept my laptop on with Amphetamine, but indeed that was crazy.

[This answer](https://stackoverflow.com/a/44922590)  around pickling/unpickling seems to even say incremental learning with the sklearn API is not possible. So indeed I feel like I want to try it with the functional API.

I am thinking the lesson is the data caching approach mentioned [here](https://stackoverflow.com/questions/43972009/how-to-load-a-big-train-csv-for-xgboost) for example, is the way to go, but I have not been able to find how to use it with the sklearn api.

I tried that in my [notebook here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-12.md#i-ended-up-trying-out-the-external-memory-approach) but my results were very different. I think this was something to do with a very different set of default parameters.

Or something tells me using  `num_rounds=2` could have been the culprit. I would like to retry this with more rounds! (In next [section](#using-the-functional-xgboost-api-with-caching-seems-to-be-hit-or-miss)   I did try `num_rounds=100` but that did not help )

Somehow the caching feature is not mentioned in [this blogpost](https://towardsdatascience.com/build-xgboost-lightgbm-models-on-large-datasets-what-are-the-possible-solutions-bf882da2c27d) .


##### Using the functional Xgboost api with caching seems to be hit or miss
I did try the functional xgboost api w/ `num_rounds=100` in [this notebook](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-21.md) , although it feels like something's wrong. The verbose xgboost output looks like no learning is happening. Going to have to try to pick that apart. According to the [parameters documentation](https://xgboost.readthedocs.io/en/latest/parameter.html)  , as far as the _"tree construction algorithm"_ goes, _"Experimental support for external memory is available for approx and gpu_hist."_ for the `tree_method` parameters.

Later on [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-03-aws.md) I can see learning does happen as long as that "cache" feature is not used. Indeed very odd.


#### Parallelism
One anecdote around parallelism. In these two notebooks, [2020-07-03-aws](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-03-aws.md) and [2020-07-04-aws](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-04-aws.md), I used the same data and same xgboost parameters except in the first go I used the functional API and in the second go I used the sklearn API.

Amazingly, the accuracy and logloss on the test set was exactly the same to several decimal places in the two cases (I passed `seed=42` in both cases as a parameter but I didn't expect such a high level of determinism!).

The walltime difference was `4min 18s` vs `49min 6s` ! (What a difference multithreading makes!)

The first case used `2 threads`. I didn't actually set the `nthread` parameter, but I read in [the docs](https://xgboost.readthedocs.io/en/latest/parameter.html) it defaults to the max. The [sklearn doc](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBClassifier) seems to show `n_jobs` is the equivalent parameter here, but it does not appear to describe the default.

Nicely, the magic func `%%time` shows the parallelization as

```
CPU times: user 8min 24s, sys: 1.24 s, total: 8min 26s
Wall time: 4min 18s
```

vs

```
CPU times: user 49min 10s, sys: 1.15 s, total: 49min 11s
Wall time: 49min 6s
```

#### Side note
* In the multiclass problem I have here, this is really making me think of the difference between [winner take all political elections](https://ballotpedia.org/Winner-take-all) vs [proportional representation](https://ballotpedia.org/Proportional_representation) elections, as binary vs multi-label problems.
