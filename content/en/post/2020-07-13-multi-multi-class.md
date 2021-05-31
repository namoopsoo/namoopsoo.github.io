---
date: 2020-07-13
title: Notes on multi-multi-class classifiers
---

### Summary
Here is an early draft of a post, trying to extract some of the insights from the project [here](/project/2020-10-20-bike-share-learn-reboot/).
There is a lot to write about and I want to just start getting it out.

### Quick outline
- The logloss upper bound
- Does the "k area" metric help?
- training balancing
- Is it possible to calculate the Bayesian error rate here?
- And logloss seems to be very sensitive.   (can look at correlations , not super high)
- So what metric should be used ?
- And re-calc that train error so I can compare against test error to understand level of bias/variance

#### The logloss upper bound
Training set accuracy and test set accuracy have intuitive boundaries, between `0` and `1`, but logloss does not feel intuitive.

What are some theoretical bad logloss outcomes? How do I know model candidates are doing anything useful at all?

In an earlier notebook I calculated logloss w/ random data and got `4.29` , discussing  `random_logloss`  and `uniform_logloss` [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-04-aws.md) . In general, logloss maybe it has a theoretical worst case basically . Filling equal likelihoods for all output probabilities gave a logloss of `3.98`.

Making contrived probability vectors off by 1 class from the correct answers [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-04-aws.md#best-and-worst-possible-logloss) yielded logloss of `34.538` regardless of which the wrong class was. So indeed logloss does not care about the order. 

Also, in a different approach for a baseline logloss, in one of the earlier notebooks [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-04-pure-prior-probability-model.md#train-this-super-dumb-baseline-model) , I created a model which just returned the softmax output of the destination tallies for all of the source neighborhoods. With a `5 fold` cross validation, this produced validation logloss values of `array([29.03426394, 25.61716199, 29.19083979, 28.312853  , 22.04601817])` which is somehow way worse than random! I think this shows that in general perhaps the usefulness of logloss is not great as an evaluation metric for a super large number of classes (in this case `54`). This finding feels erratic.

#### The k area metric
In the notebook [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md) I have been evaluating some of the results of a multi day hyper parameter tuning session that has been running in [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-10-aws.md). ( First mini tuning session also [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-09-aws.md) ).

I started discussing this [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#karea).

Also, first started calculating some of this data in [this notebook](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-04-aws.md)


The idea is if we want to compare two models predicting multi-class probabilities, in an ideal world, the accuracy will be good enough. But when the number of classes is really high (in this case `54`), we will be looking at very low accuracies. And accuracy only looks at the top class. You can also look at the "Top k=5 accuracy", or the "Top k=10 accuracy", meaning whether the target class is in the top `k=5` or top `k=10` ranked probabilities.

Instead you can create a single number between `0` and `1` by accumulating the ranked probabilities


If you plot, for all of the examples in a test set, what is the `k` required to get the correct answer you get this distribution,


<img src="https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-04-aws_files/2020-07-04-aws_34_0.png?raw=true" >

This looks good in the sense the numbers are higher for lower k.

And the cumulative distribution looks like this

<img src="https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-04-aws_files/2020-07-04-aws_36_0.png?raw=true" />

So the `k area` metric is the area under this second curve. The fewer `k` we need to find the correct answer, the larger the area under this figure. This feels a bit more intuitive of a metric for evaluating classifiers with many many classes, at least compared to logloss!



#### Extending notes on k-area
* Earlier notes on this metric are [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-04-aws.md#beginnings-of-a-more-granular-metric-for-multi-class-models)
* The genesis was basically that logloss doesn't care about the rank a model gives to each class probability.
* This metric is an idea of how to capture roughly how early in the output probabilities does a multi-class model capture the correct answer.
* The *k-area* metric is a number from 0 to (num_classes-1)/num_classes , which is the area under the curve of the "cumulative rank accuracy" , based on the rank of the correct predictions in a model's multi-class probabilities.
* Here are some examples

```python
import pylab
import matplotlib.pyplot as plt
import numpy as np
import fresh.metrics as fm
import fresh.utils as fu

def _plot(vec):
    plt.plot(vec)
    plt.title(f'cumulative accuracy (karea={vec.sum()})')
    out_dir = 'notes/2020-10-20-karea-worst__files'
    out_loc = f'{out_dir}/{fu.utc_ts()}_cumulative_accuracy.png'
    pylab.savefig(out_loc)
    pylab.close()
    return out_loc

y_test = np.array([1,
                   2,
                   1,
                   0,
                   3])
# Worst possible, always splitting the predictions in the other classes
y_prob = np.array([[.6, 0, .3, .1],
                  [.5, .4, 0, 1],
                  [.5, 0, .4, .1],
                  [0, .5, .4, .1],
                  [.5, .4, .1, 0],])
#
correct_kth, topk, karea = fm.kth_area(y_test, y_prob, num_classes=4)                  
_plot(topk)

```

<img src="https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-20-karea-worst__files/2020-10-21T165705Z_cumulative_accuracy.png?raw=true" width="50%">

```python
# Slightly better than worst...
y_prob = np.array([[.6, .3, .1, 0],
                  [.5, .5, 0, 0],
                  [.5, 0, .5, 0],
                  [0, .5, .5, 0],
                  [.5, .5, 0, 0],])
#
correct_kth, topk, karea = fm.kth_area(y_test, y_prob, num_classes=4)
_plot(topk)
# ([1, 3, 3, 3, 2], 0.15000000000000002)                  

```
<img src="https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-20-karea-worst__files/2020-10-21T173626Z_cumulative_accuracy.png?raw=true" width="50%">

* in the middle...

```python
y_prob = np.array([[.4, .2, .1, .3],
                  [.5, .4, .1, 0],
                  [.5, 0, .5, 0],
                  [.5, .1, .4, 0],
                  [.4, .5, 0, .1],])
#
correct_kth, topk, karea = fm.kth_area(y_test, y_prob, num_classes=4)
_plot(topk)
# ([2, 2, 3, 0, 2], 0.30000000000000004)
```
<img src="https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-20-karea-worst__files/2020-10-21T173730Z_cumulative_accuracy.png?raw=true" width="50%">

* near perfect
```python
y_prob = np.array([[.2, .4, .1, .3],
                  [.1, .4, .5, 0],
                  [0, .6, .4, 0],
                  [.5, .1, .4, 0],
                  [.1, .5, 0, .4],])
#
correct_kth, topk, karea = fm.kth_area(y_test, y_prob, num_classes=4)
_plot(topk)

# ([0, 0, 0, 0, 1], 0.7)
```
<img src="https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-20-karea-worst__files/2020-10-21T173805Z_cumulative_accuracy.png?raw=true" width="50%">

* perfect
```python
y_prob = np.array([[.2, .4, .1, .3],
                  [.1, .4, .5, 0],
                  [0, .6, .4, 0],
                  [.5, .1, .4, 0],
                  [.1, .4, 0, .5],])
#
correct_kth, topk, karea = fm.kth_area(y_test, y_prob, num_classes=4)
_plot(topk)
# ([0, 0, 0, 0, 0], 0.75)
```

<img src="https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-20-karea-worst__files/2020-10-21T173826Z_cumulative_accuracy.png?raw=true" width="50%">

#### Effect of balancing training data
.

In previous projects, training set balancing has been an important aspect of good dev/test set performance. Without balancing, highly imbalanced training sets end up producing classifiers that do disproportionately better with the majority or plurality classes.

In the note book "2020-06-29.md" notebook, I worked on a balancing/shrinking concept . Hopefully I can take these concepts and use them in the future as well. I tried to write this balancing code in a somewhat re-usable way.

In the ["2020-07-03-aws.md"](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-03-aws.md) notebook, I also added some "shrinkage" because of my Jupyter kernel crashing. The other useful concept is how much data do we really need? Obviously if there is too much data and it crashes the notebook (as [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-28-take2.md) for example ) , but I think this "balanced shrinkage" concept is interesting to explore just to be more efficient in for example use of hyper parameter tuning time. If you can perhaps "boil down" your data reducing its size by `50%` and if the dev/test set error does not change much then in principle that can save a lot of hyper parameter tuning time, where you may be training/predicting hundreds of models.

And here ["2020-07-08-aws.md"](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-08-aws.md) I have another version of balancing that is less aggressive. The first iteration of balancing I was using sort of flipped the proportions. It dramatically (proportionally) weighed down the majority class (too much). This second iteration tries to just bring the plurality classes down closer to the "equal share" each class should get .


But surprisingly, in ["2020-07-08-aws.md"](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-08-aws.md) the "balanced test accuracy" did not improve much.
```
test acc 0.12198962315156459
test balanced acc 0.1044572104146026
logloss 3.4794945441534866
```


Also in past projects I had balanced out a "groomed" test set myself but this time I just tried using `balanced_accuracy_score` from sklearn.

I think visualizing the confusion is pretty interesting too in multiclass problems like this one from ["2020-07-03-aws.md"](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-03-aws.md), where I had noted the last class (bright yellow!) is sort of taking over the color spectrum of this data, because it is in the `1000` range but all the other data appears to be below `200`.

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-03-aws_files/2020-07-03-aws_32_0.png?raw=true" >


And as a proof of concept my confusion visualization from [2020-07-05-aws-two](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-05-aws-two.md) ,

is showing the evidence of no balancing at all, because we see the classifier is focused on predicting basically one class, what looks like class `8` or `9`.

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-05-aws-two_files/2020-07-05-aws-two_11_0.png?raw=true">


And the corresponding metrics for that classifier are
```
logloss 3.282076793024198
acc 0.15964601098390355
balanced acc 0.08281646671786597
```
which helps to show that when `acc` and `balanced acc` are far from each other, then the `acc` probably cannot be trusted.

#### Ultimately what is a good metric


Because balanced acc and acc correlate so highly, the choice between those does not matter so much, as long as the input training data is somewhat balanced, since as we see in the above result, if `acc` is considerably higher than `balanced acc` then we probably even cannot trust the `logloss`. So perhaps checking that `acc` and `balanced acc` are close is a good _"meta metric"_ at first.

Logloss vs acc, that is an interesting choice.

With hyper parameter tuning, we can look at a lot of results and see how these all compare.

I write about some hyper parameter tuning result [here](/post/2020-07-24-understanding-tuning-results/)

But ultimately I think `k area` is a more granular measure than simple accuracy.
