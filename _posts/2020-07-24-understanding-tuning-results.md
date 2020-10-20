

To explore some of the hyperparameter boundaries with this model, I ran some tests in these notebooks, [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-09-aws.md) and [here](https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-10-aws.md).

And to get a better understanding of the overfitting-ness / underfitting-ness of models , [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-16-local.md#2020-07-18) , I took the model artifacts and recalculated metrics on the training set, to generate some stats comparing training and testing performance.


### Hyperparameter testing
(Going to describe this later)

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-09-aws_files/2020-07-09-aws_10_1.png">

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-09-aws_files/2020-07-09-aws_13_0.png">

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-09-aws_files/2020-07-09-aws_14_0.png">

The tuning took several days to complete, but I started plotting early results in [this notebook](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md)

Learning rate had some drastic effects for sure!

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_17_0.png">

Maybe this one below did not have enough data points yet, but slightly surprising perhaps. I had expected the smaller learning rate to take longer. 

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_33_0.png">



### Train / Test Comparisons

For instance, keeping a few parameters fixed, I started looking at accuracy across the number of rounds used during training,

```python
import fresh.plot as fp
keep_fixed = {
 'max_depth': 3,
 'learning_rate': 0.01,
 'colsample_bylevel': 0.1,
 'colsample_bynode': 1,
 'colsample_bytree': 0.1,
 'subsample': 0.1,
 #'num_round': 10,
        }
# alldf is the combined train+test metrics on model artifacts
fp.compare_train_test(alldf, feature_col='num_round',
                      metric_cols=['acc', 'train_acc'],
                      keep_fixed=keep_fixed)
```

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-16-local_files/2020-07-16-local_28_0.png" >

And sorting the metrics dataframe by test accuracy, I also plotted that,

```python
best_params = dict(alldf.sort_values(by='acc').iloc[-1])
best_params
{'train_acc': 0.12693459297270465,
 'train_balanced_acc': 0.11012147901980039,
 'i': 755,
 'train_logloss': 3.4301962566050057,
 'train_karea': 0.76345208497788,
 'max_depth': 4,
 'learning_rate': 0.1,
 'objective': 'multi:softprob',
 'num_class': 54,
 'base_score': 0.5,
 'booster': 'gbtree',
 'colsample_bylevel': 1.0,
 'colsample_bynode': 1,
 'colsample_bytree': 1.0,
 'gamma': 0,
 'max_delta_step': 0,
 'min_child_weight': 1,
 'random_state': 0,
 'reg_alpha': 0,
 'reg_lambda': 1,
 'scale_pos_weight': 1,
 'seed': 42,
 'subsample': 0.4,
 'verbosity': 0,
 'acc': 0.12304248437307332,
 'balanced_acc': 0.10551953202851949,
 'logloss': 3.4480742986458592,
 'walltime': 1918.593945,
 'karea': 0.75845582462009,
 'num_round': 100}
# Taking the best params ^^ here is what the "learning curve" seems to look like
keep_fixed = {
 'max_depth': 4,
 'learning_rate': 0.1,

 'colsample_bylevel': 1.0,
 'colsample_bynode': 1,
 'colsample_bytree': 1.0,

 'subsample': 0.4,
 #'num_round': 10,
        }

fp.compare_train_test(alldf, feature_col='num_round',
                      metric_cols=['acc', 'train_acc', 'balanced_acc',
                                  'train_balanced_acc'],
                      keep_fixed=keep_fixed)
```


<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-16-local_files/2020-07-16-local_31_0.png">

The difference between train accuracy and test accuracy does not look crazy so I think it is safe to say this model is not overfitting .
