

### quick outline
- Does the "k area" metric help?
- In an earlier notebook I calculated logloss w/ random data and got `4.29` , discussing  `random_logloss`  and `uniform_logloss` [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-04-aws.md) . In general, logloss maybe it has a theoretical worst case basically . Filling equal likelihoods for all output probabilities gave a logloss of `3.98`.
- training balancing
- Is it possible to calculate the Bayesian error rate here?
- And logloss seems to be very sensitive.   (can look at correlations , not super high)


#### the k area metric
In the notebook [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-11-local.md) I have been evaluating some of the results of a multi day hyper parameter tuning session that has been running in [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-10-aws.md). ( First mini tuning session also [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-09-aws.md) ).

I started discussing this [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-11-local.md#karea).

Also, first started calculating some of this data in [this notebook](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-04-aws.md)


The idea is if we want to compare two models predicting multi-class probabilities, in an ideal world, the accuracy will be good enough. But when the number of classes is really high (in this case `54`), we will be looking at very low accuracies. And accuracy only looks at the top class. You can also look at the "Top k=5 accuracy", or the "Top k=10 accuracy", meaning whether the target class is in the top `k=5` or top `k=10` ranked probabilities.

Instead you can create a single number between `0` and `1` by accumulating the ranked probabilities


If you plot, for all of the examples in a test set, what is the `k` required to get the correct answer you get this distribution,
<img src="https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-04-aws_files/2020-07-04-aws_34_0.png">

This looks good in the sense the numbers are higher for lower k.

And the cumulative distribution looks like this

<img src="https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-04-aws_files/2020-07-04-aws_36_0.png">



#### Effect of balancing training data
