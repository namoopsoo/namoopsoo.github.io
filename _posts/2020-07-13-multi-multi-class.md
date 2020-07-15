
### Summary
Here is an early draft of a post, trying to extract some of the insights from the project [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/).
There is a lot to write about and I want to just start getting it out.

### Quick outline
- The logloss upper bound
- Does the "k area" metric help?
- training balancing
- Is it possible to calculate the Bayesian error rate here?
- And logloss seems to be very sensitive.   (can look at correlations , not super high)

#### The logloss upper bound
Training set accuracy and test set accuracy have intuitive boundaries, between `0` and `1`, but logloss does not feel intuitive.

What are some theoretical bad logloss outcomes? How do I know model candidates are doing anything useful at all?

In an earlier notebook I calculated logloss w/ random data and got `4.29` , discussing  `random_logloss`  and `uniform_logloss` [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-04-aws.md) . In general, logloss maybe it has a theoretical worst case basically . Filling equal likelihoods for all output probabilities gave a logloss of `3.98`.



#### The k area metric
In the notebook [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-11-local.md) I have been evaluating some of the results of a multi day hyper parameter tuning session that has been running in [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-10-aws.md). ( First mini tuning session also [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-09-aws.md) ).

I started discussing this [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-11-local.md#karea).

Also, first started calculating some of this data in [this notebook](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-04-aws.md)


The idea is if we want to compare two models predicting multi-class probabilities, in an ideal world, the accuracy will be good enough. But when the number of classes is really high (in this case `54`), we will be looking at very low accuracies. And accuracy only looks at the top class. You can also look at the "Top k=5 accuracy", or the "Top k=10 accuracy", meaning whether the target class is in the top `k=5` or top `k=10` ranked probabilities.

Instead you can create a single number between `0` and `1` by accumulating the ranked probabilities


If you plot, for all of the examples in a test set, what is the `k` required to get the correct answer you get this distribution,


<img src="https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-04-aws_files/2020-07-04-aws_34_0.png?raw=true" >

This looks good in the sense the numbers are higher for lower k.

And the cumulative distribution looks like this

<img src="https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-04-aws_files/2020-07-04-aws_36_0.png?raw=true" />



#### Effect of balancing training data
.

In previous projects, training set balancing has been an important aspect of good dev/test set performance. Without balancing, highly imbalanced training sets end up producing classifiers that do disproportionately better with the majority or plurality classes.

In the note book "2020-06-29.md" notebook, I worked on a balancing/shrinking concept . Hopefully I can take these concepts and use them in the future as well. I tried to write this balancing code in a somewhat re-usable way.

In the "2020-07-03-aws.md" notebook, I also added some "shrinkage" because of my Jupyter kernel crashing. The other useful concept is how much data do we really need? Obviously if there is too much data and it crashes the notebook (as [here]("2020-06-28-take2.ipynb") for example ) , but I think this "balanced shrinkage" concept is interesting to explore just to be more efficient in for example use of hyper parameter tuning time. If you can perhaps "boil down" your data reducing its size by `50%` and if the dev/test set error does not change much then in principle that can save a lot of hyper parameter tuning time, where you may be training/predicting hundreds of models.

And here "2020-07-08-aws.md" I have another version of balancing that is less aggressive. The first iteration of balancing I was using sort of flipped the proportions. It dramatically (proportionally) weighed down the majority class (too much). This second iteration tries to just bring the plurality classes down closer to the "equal share" each class should get .


But surprisingly, in "2020-07-08-aws.md" the "balanced test accuracy" did not improve much.


Also in past projects I had balanced out a "groomed" test set myself but this time I just tried using `balanced_accuracy_score` from sklearn.

I think visualizing the confusion is pretty interesting too in multiclass problems like this one from "2020-07-03-aws.md", where I had noted the last class (bright yellow!) is sort of taking over the color spectrum of this data, because it is in the `1000` range but all the other data appears to be below `200`.

<img src="https://github.com/namoopsoo/learn-citibike/raw/2020-revisit/notes/2020-07-03-aws_files/2020-07-03-aws_32_0.png?raw=true" >


And as a proof of concept my confusion visualization from [2020-07-05-aws-two](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-05-aws-two.md) ,

is showing the evidence of no balancing at all !

<img src="https://github.com/namoopsoo/learn-citibike/raw/2020-revisit/notes/2020-07-05-aws-two_files/2020-07-05-aws-two_11_0.png?raw=true">
