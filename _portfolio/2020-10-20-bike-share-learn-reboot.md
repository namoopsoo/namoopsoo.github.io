---
layout: post
title:  "Bike Share Learn Reboot"
date:   2020-10-20 10:00:05 -0400
---

<img src="https://s3.amazonaws.com/my-blog-content/2020/2020-10-20-bike-share-learn-reboot/IMG_8499.jpg" width="40%">


### What
This project is a reboot of [my earlier project](/portfolio/citibike-project-readme.html) of predicting bicycle ride share riders destinations.
https://bike-hop-predict.s3.amazonaws.com/index.html

This time around I used XGBoost, newer features, hyper parameter tuning and I have a <a href="https://bike-hop-predict.s3.amazonaws.com/index.html" target="_blank"> demo site </a> as well.   
<!-- http://bike.michal.piekarczyk.xyz/index.html -->

Again, the data looks like this

```
"tripduration","starttime","stoptime","start station id","start station name","start station latitude","start station longitude","end station id","end station name","end station latitude","end station longitude","bikeid","usertype","birth year","gender"
"171","10/1/2015 00:00:02","10/1/2015 00:02:54","388","W 26 St & 10 Ave","40.749717753","-74.002950346","494","W 26 St & 8 Ave","40.74734825","-73.99723551","24302","Subscriber","1973","1"
"593","10/1/2015 00:00:02","10/1/2015 00:09:55","518","E 39 St & 2 Ave","40.74780373","-73.9734419","438","St Marks Pl & 1 Ave","40.72779126","-73.98564945","19904","Subscriber","1990","1"
"233","10/1/2015 00:00:11","10/1/2015 00:04:05","447","8 Ave & W 52 St","40.76370739","-73.9851615","447","8 Ave & W 52 St","40.76370739","-73.9851615","17797","Subscriber","1984","1"
"250","10/1/2015 00:00:15","10/1/2015 00:04:25","336","Sullivan St & Washington Sq","40.73047747","-73.99906065","223","W 13 St & 7 Ave","40.73781509","-73.99994661","23966","Subscriber","1984","1"
"528","10/1/2015 00:00:17","10/1/2015 00:09:05","3107","Bedford Ave & Nassau Ave","40.72311651","-73.95212324","539","Metropolitan Ave & Bedford Ave","40.71534825","-73.96024116","16246","Customer","","0"
"440","10/1/2015 00:00:17","10/1/2015 00:07:37","3107","Bedford Ave & Nassau Ave","40.72311651","-73.95212324","539","Metropolitan Ave & Bedford Ave","40.71534825","-73.96024116","23698","Customer","","0"
```

### TOC
* [Prior probability baseline](#prior-probability-baseline)
* [Xgboost detour](#xgboost-detour)
* [Multi class classification notes](#multi-class-classification-notes)
* []()
* [Previously](#previously-vs-this-time)
* [model highlights](#model-highlights)
* data used
* [Glue notes](#glue-notes)
* [Looking at hyperparameter tuning results](#looking-at-hyperparameter-tuning-results)
* [Follow on](#follow-on)

### Prior probability baseline
[Here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-04-pure-prior-probability-model.md), I first wanted to get a metric baseline using a simple model which only uses the highest prior probability destination as the prediction for a source bike share station. Anything even slightly more sophisticated should perform better. I also used this opportunity to apply multi class logloss as an evaluation metric for this problem, which I had not tried last time. So for an output probability vector of `54` possible destination stations, log loss can more granularly assess the prediction probabilities against a vector of the correct station, `[0, 1, 0, 0, 0,...]` compared to just `accuracy`.

For example

```python
from sklearn.metrics import log_loss
# and some noisy predictions
noisy_pred = np.array([[.05, .05, .9],
                   [.95, 0.05, 0],
                   [.9, 0.1, 0],
                   [0.05, .05, .9],
                   [0, 1, 0]])
log_loss([3, 1, 1, 3, 2],
         noisy_pred)
```

the output here is `0.07347496827220674`, which is just slightly worse than the perfect `0.`, showing that log loss can be handy for comparing models.

The detail is in the [notes](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-04-pure-prior-probability-model.md), but basically the cross validation log loss using this method ended up being

```
array([29.03426394, 25.61716199, 29.19083979, 28.312853  , 22.04601817])
```

#### Dockerization
Next, for repeatability and portability, [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-07-local-docker-notes.md) I re-adapted some earlier Dockerization I had setup before to wrap xgboost, along with jupyter notebook for experimentation.

### Xgboost detour
To start, I wanted to better understand how to use Xgboost abilities with respect to training a model, putting it down, saving it to disk, loading it again and continuing to train on new data. I had used this capability in Tensorflow land earlier and I read it might be possible with Xgboost, but even after trial and error with both the main Xgboost API and its scikit learn API, I could not get this to work properly.
My notes on this are  [here in an earlier post](https://michal.piekarczyk.xyz/2020/06/21/notes-xgboost.html ).

One cool thing I did [learn](https://michal.piekarczyk.xyz/2020/06/21/notes-xgboost.html#parallelism) however was that when repeating a model train and evaluation experiment with both the functional API and the scikit learn API, the functional API took advantage of multithreading, and produced a particular result in `4min 18s` vs `49min 6s`, with both models using the same `seed=42` and ending up with the same accuracy and log loss on some held out data.

As I mentioned [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-12--snapshot-2020-06-14T2258Z.md#2020-06-13)  , I experienced some early problems running out of memory and crashing, for instance computing log los son `843416 rows`. And that is why I was seeking out approaches of online learning. But because of the limitations, my workout ended up being the use of at least carefully deleting objects in memory with `del` to free up space for, between preprocessing, training and validation. And I also played around with the approach of initializing a `xgb.DMatrix` using the `xgb.DMatrix('/my/blah/path#dtrain.cache')` syntax where you specify `#` a cache file to allow for file access to reduce the in-memory burden, also requiring to dump your pre-processed training data to file first. (And doing that is good anyway because it allows you to free up that precious memory).

Compared to the initial baseline logloss from earlier of around `29`, here I [noted](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-12--snapshot-2020-06-14T2258Z.md#averaging-log-losses) a result of `3.9934347` with the initial xgboost approach.

On [2020-06-14](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-14.md), I tried using the xgboost caching with the scikitlearn api approach. In the meantime I also ran into a fun issue where an xgboost model was trained on data without a particular output class , with only `53` classes in fact and would produce predict probability vectors of length `53` instead of `54`, so I ended up having to make sure to better shuffle the data to make sure when trying to use less data (when using cross validation for instance) that all of the output classes are accounted for, without having a more direct way of telling Xgboost what the output classes should be.

Also another fun Tensorflow comparison was I got `XGBoostError: need to call fit or load_model beforehand` when trying to call predict on a bare model that had not undergone training. Whereas with Tensorflow, I experienced in a previous project that this is absolutely fine, because you simply have a fully formed neural network with some randomly (or otherwise) initialized weights. But with xgboost, or at least the particular implementation I was using, this is not possible, because there is no notion of a base model.




### Multi class classification notes

* [Notes on multi class classification](https://michal.piekarczyk.xyz/2020/07/13/multi-multi-class.html)

### Understanding tuning results
 [hyper parameter tuning and train/test acc](https://michal.piekarczyk.xyz/2020/07/24/understanding-tuning-results.html)


### Previously vs This time
* Last time around, I segmented the starting data into `24` hour-long segments. This time, I segmented time into only `5` bins to make the model slightly more generalizable.

```python
# time_of_day
0: 6-9,
1: 10-13,
2: 14-16,
3: 17-21,
4: 22-0, 0-5
```

* Actually after picking these bins arbitrarily, I ended up also looking at the time of day histograms [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-22-features-v3.md) and the peaks look close to what I had as a mental model in my mind. It might be interesting try some other bins at some point later.

* One other new feature this time is the binary `weekday` feature, specifying weekday vs weekend.
* The starting neighborhood one hot encoded was kept as an input.
* Also last time around, the main model was a Random Forest classifier, but using XGBoost this time.

### Model Highlights

The top model has these stats...
```
(pandars3) $ docker run -p 8889:8889 -p 8080:8080 -i -t -v $(pwd):/opt/program \
             -v ${MY_LOCAL_DATA_DIRECTORY}:/opt/data \
             -v   ~/Downloads:/opt/downloads \
             -v  $(pwd)/artifacts/2020-08-19T144654Z:/opt/ml \
             citibike-learn:latest \
```
```python
import fresh.predict_utils as fpu
bundle = fpu.load_bundle_in_docker()

In [7]: bundle['model_bundle']['bundle']['validation_metrics']                                                                 
Out[7]:
{'accuracy': 0.12171455130090014,
 'balanced_accuracy': 0.10451301995291779,
 'confusion': array([[415,  64,   4, ...,   0, 103,  69],
        [ 56, 541,   4, ...,   0, 130,  27],
        [ 23,  10, 136, ...,   0,  16, 130],
        ...,
        [  2,   0,   2, ...,   1,   3,  36],
        [151, 222,   3, ...,   0, 260,  35],
        [ 84,  25,  46, ...,   0,  29, 861]]),
 'logloss': 3.4335361255637977,
 'test': '/home/ec2-user/SageMaker/learn-citibike/artifacts/2020-07-08T143732Z/test.libsvm',
 'karea': 0.760827309330065}


```
* More on the "k-area" metric is [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-20-karea-worst.md)


#### Top Model's Top Fscore features

Extracting from [this notebook](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-21-look-at-model-plot.md) ,

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>f</th>
      <th>fscore</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>9</th>
      <td>weekday</td>
      <td>f84</td>
      <td>12812</td>
    </tr>
    <tr>
      <th>10</th>
      <td>gender=1</td>
      <td>f76</td>
      <td>8973</td>
    </tr>
    <tr>
      <th>2</th>
      <td>time_of_day=3</td>
      <td>f81</td>
      <td>8377</td>
    </tr>
    <tr>
      <th>8</th>
      <td>gender=0</td>
      <td>f75</td>
      <td>7969</td>
    </tr>
    <tr>
      <th>11</th>
      <td>time_of_day=1</td>
      <td>f79</td>
      <td>7064</td>
    </tr>
    <tr>
      <th>26</th>
      <td>time_of_day=2</td>
      <td>f80</td>
      <td>6594</td>
    </tr>
    <tr>
      <th>7</th>
      <td>time_of_day=0</td>
      <td>f78</td>
      <td>6302</td>
    </tr>
    <tr>
      <th>17</th>
      <td>gender=2</td>
      <td>f77</td>
      <td>5509</td>
    </tr>
    <tr>
      <th>3</th>
      <td>time_of_day=4</td>
      <td>f82</td>
      <td>4854</td>
    </tr>
    <tr>
      <th>40</th>
      <td>start_neighborhood=Chelsea</td>
      <td>f12</td>
      <td>1199</td>
    </tr>
    <tr>
      <th>37</th>
      <td>start_neighborhood=Midtown East</td>
      <td>f46</td>
      <td>1058</td>
    </tr>
    <tr>
      <th>36</th>
      <td>start_neighborhood=Midtown West</td>
      <td>f47</td>
      <td>947</td>
    </tr>
    <tr>
      <th>30</th>
      <td>start_neighborhood=Downtown Brooklyn</td>
      <td>f18</td>
      <td>910</td>
    </tr>
    <tr>
      <th>41</th>
      <td>start_neighborhood=Hell's Kitchen</td>
      <td>f33</td>
      <td>877</td>
    </tr>
    <tr>
      <th>21</th>
      <td>start_neighborhood=Fort Greene</td>
      <td>f25</td>
      <td>865</td>
    </tr>
    <tr>
      <th>14</th>
      <td>start_neighborhood=Financial District</td>
      <td>f23</td>
      <td>860</td>
    </tr>
    <tr>
      <th>23</th>
      <td>start_neighborhood=Brooklyn Heights</td>
      <td>f7</td>
      <td>834</td>
    </tr>
    <tr>
      <th>49</th>
      <td>start_neighborhood=Kips Bay</td>
      <td>f36</td>
      <td>821</td>
    </tr>
    <tr>
      <th>13</th>
      <td>start_neighborhood=Tribeca</td>
      <td>f64</td>
      <td>813</td>
    </tr>
    <tr>
      <th>28</th>
      <td>start_neighborhood=Lower East Side</td>
      <td>f42</td>
      <td>786</td>
    </tr>
    <tr>
      <th>38</th>
      <td>start_neighborhood=Theater District</td>
      <td>f63</td>
      <td>745</td>
    </tr>
    <tr>
      <th>39</th>
      <td>start_neighborhood=Midtown</td>
      <td>f45</td>
      <td>736</td>
    </tr>
    <tr>
      <th>5</th>
      <td>start_neighborhood=Greenwich Village</td>
      <td>f32</td>
      <td>733</td>
    </tr>
    <tr>
      <th>19</th>
      <td>start_neighborhood=Clinton Hill</td>
      <td>f15</td>
      <td>703</td>
    </tr>
    <tr>
      <th>33</th>
      <td>start_neighborhood=Chinatown</td>
      <td>f13</td>
      <td>695</td>
    </tr>
    <tr>
      <th>20</th>
      <td>start_neighborhood=Williamsburg</td>
      <td>f73</td>
      <td>683</td>
    </tr>
    <tr>
      <th>48</th>
      <td>start_neighborhood=Murray Hill</td>
      <td>f48</td>
      <td>681</td>
    </tr>
    <tr>
      <th>31</th>
      <td>start_neighborhood=Dumbo</td>
      <td>f19</td>
      <td>680</td>
    </tr>
    <tr>
      <th>44</th>
      <td>start_neighborhood=Civic Center</td>
      <td>f14</td>
      <td>660</td>
    </tr>
    <tr>
      <th>12</th>
      <td>start_neighborhood=Battery Park City</td>
      <td>f1</td>
      <td>649</td>
    </tr>
  </tbody>
</table>
</div>

And it can be interesting to look at a random tree from xgboost too sometimes, again extracting from the above mentioned notebook.

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-10-21-look-at-model-plot_files/2020-10-21-look-at-model-plot_5_0.png">



### Annotating my earlier posts

#### xgb notes
[xgboost notes](https://michal.piekarczyk.xyz/2020/06/21/notes-xgboost.html )


#### Glue notes
[Glue notes](https://github.com/namoopsoo/learn-citibike/blob/2020-oct/notes/2020-08-25-glue.md)
Here I face the challenges of taking the model from model bundle to demo site. There were a lot of challenges involved. My concept was to use the Google Static Map API to display the top neighborhood predictions. Hitting this API properly did take a little bit of time, but it was not that bad. And later on, I updated the whole AWS Lambda approach so the lambda function calls the API with the result from the dockerized SageMaker served model.

Admittedly, the most time consuming part was figuring out the API Gateway Cognito "Unauthenticated Authentication". AWS has this Cognito service which manages user/password based authentication for you but it also lets you use Anonymous authentication. But there must be a lot of degrees of freedom in how this is used, because I could not find good documentation on how to set this up properly for my usecase at all.

I had used API Gateway for authentication through CORS in the past and I recalled a bit of nuance that for example you may have setup CORS properly for `200` status codes, but if your program crashes with a `500` then your browser will scream about a CORS error, because the response is not returning the expected `allow-origin-blah` header. In the past this had taken me a while to figure out, but now I luckily had that knowledge in my back pocket. In any case, it is worth it for the serverless approach.


#### Automation made the process very convenient
https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-07-local-docker-notes.md

I also described my build process in the earlier mentioned [glue notes](https://github.com/namoopsoo/learn-citibike/blob/2020-oct/notes/2020-08-25-glue.md) too. With so many tweaks to the python side, the model and the javascript side, being able to build and deploy with quick `make` style commands made everything faster. I document some of these [here](https://github.com/namoopsoo/learn-citibike/blob/master/docs/common_tasks.md) too.

#### quick pearson's chi squared independence test
quick pearson's chi squared independence test
https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-05.md

#### Looking at hyperparameter tuning results
* ( EDIT: After writing the below section, I realized I had already [here earlier, on 2020-07-24 ](https://michal.piekarczyk.xyz/2020/07/24/understanding-tuning-results.html) , described some of these results already haha. Doing the work twice, forgetting what I had done.  )  

* I spent a bit of time on hyper parameter tuning, looking at the results, fixing some parameters two focus on two others at a time.

* So per [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#looking-at-num_round-fundamentally) ,
the `num_round` as expected improves logloss,

```python
keep_fixed = {
 'max_depth': 3,
 'learning_rate': 0.01,
 'colsample_bylevel': 0.1,
 'colsample_bynode': 1,
 'colsample_bytree': 0.1,
 'subsample': 0.1,
 'num_round': 10,
        }
col1, col2, metric_col = 'max_depth', 'num_round', 'logloss'
fp.compare_tuning(df, feature_col_1=col1,
             feature_col_2=col2,
             metric_col=metric_col,
             keep_fixed=fvu.without(
                 keep_fixed, keys=[col1, col2]))
```

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_11_0.png">

And maybe this is good as a sanity check, but more rounds take more time, ( [per here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#walltime) )

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_13_0.png">

And from [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#look-at-walltime-and-learning-rate-again) it was interesting to see that walltime is stable mostly when it comes to learning rate except sometimes...

<!-- <img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_15_0.png"> -->

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_33_0.png">


And per [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#also-learning-rate-vs-acc) at least per the fixed parameters, the `0.1` learning rate is better than the `0.01` learning rate.

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_17_0.png">

And per  [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#look-at-subsample-w-different-rounds)  , `subsample` is just not appearing to be influencing accuracy.

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_20_0.png">

And per [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#hmm-colsample_bylevel)  , the rando column sampling may have just removed the good columns

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_22_0.png">


#### Train and test accuracy comparison
* [Here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-16-local.md) , I took all of my `1000+` models from earlier, (which were on S3 so I had to copy them locally for convenience) and calculated accuracy, logloss and karea metrics for the training data, in order to be able to get learning curves to understand underfitting/overfitting.
* Just showing ihere an example run for one model...

```python

# As per https://github.com/namoopsoo/learn-citibike/blob/2020-revisit/notes/2020-07-10-aws.md
# the data dir was artifacts/2020-07-08T143732Z  ... going to re-create that locally too
#
datadir = '/opt/program/artifacts/2020-07-08T143732Z'
artifactsdir = '/opt/program/artifacts/2020-07-10T135910Z'
train_results = []

train_loc = f'{datadir}/train.libsvm'
dtrain = xgb.DMatrix(f'{train_loc}?format=libsvm')
actuals = dtrain.get_label()
print('evaluate using ', train_loc)


train_data = load_svmlight_file(train_loc)
X_train = train_data[0].toarray()
y_train = train_data[1]

%%time
########
# Try one
i = 0
bundle = joblib.load(f'{artifactsdir}/{i}_bundle_with_metrics.joblib')
model = bundle['xgb_model']

y_prob_vec = model.predict(dtrain)
predictions = np.argmax(y_prob_vec, axis=1)

logloss = fu.big_logloss(actuals, y_prob=y_prob_vec,
                         labels= list(range(54)))
acc = accuracy_score(actuals, predictions)
balanced_acc = balanced_accuracy_score(actuals, predictions)

correct_kth, karea = fm.kth_area(y_train, y_prob_vec,
        num_classes=54)

```

```
CPU times: user 31.3 s, sys: 110 ms, total: 31.4 s
Wall time: 21.4 s
```

```
acc, balanced_acc, karea

```

```
(0.05276320740101365,
 0.03727538888502701,
 0.6435250908504123)
```

The whole thing, took about `10 hours` as measured by the final line from `tqdm`,

```
100%|█████████▉| 1052/1054 [10:00:57<01:08, 34.27s/it]
```

##### Putting that together,
[Here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-16-local.md#2020-07-23) putting that together ..

training and test accuracy are pretty consistently close, with training accuracy being slightly better as expected. So there is no evidence overall of overfitting. But perhaps some evidence of underfitting .

The first thing I just looked at the parameters fixed by just what happened to be the first model built, so pretty arbitrary and comparing over the number of rounds. The results not unexpected not showing much learning happening.


<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-16-local_files/2020-07-16-local_28_0.png">

Then I took the model with the best test accuracy results,

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
 ```

 And plotted all the train/test metrics across rounds, and this figure definitely shows learning happening . Very exciting!

 <img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-16-local_files/2020-07-16-local_31_0.png">


##### Also looked for the biggest gap between train/test accuracy
* And per the below,  interestingly, it's seeming like the biggest train/test gap is very small..

```python
alldf['train_test_acc_delta'] = alldf.apply(lambda x: abs(x['acc'] - x['train_acc']), axis=1)
alldf.sort_values(by='train_test_acc_delta').iloc[-1]
```

```python
train_acc                     0.128123
train_balanced_acc            0.111239
i                                 1241
train_logloss                  3.40954
train_karea                   0.767823
max_depth                            5
learning_rate                      0.1
objective               multi:softprob
num_class                           54
base_score                         0.5
booster                         gbtree
colsample_bylevel                    1
colsample_bynode                     1
colsample_bytree                     1
gamma                                0
max_delta_step                       0
min_child_weight                     1
random_state                         0
reg_alpha                            0
reg_lambda                           1
scale_pos_weight                     1
seed                                42
subsample                          0.4
verbosity                            0
acc                            0.12253
balanced_acc                  0.104698
logloss                        3.43584
walltime                       2327.88
karea                         0.760578
num_round                          100
train_test_acc_delta        0.00559313
Name: 1242, dtype: object
```


#### Initial time of day look
https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-08-05-woe.md

 super

#### discuss
https://github.com/namoopsoo/learn-citibike/blob/2020-oct/notes/2020-08-25-glue.md


#### Feature importances
[notes](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-26-feature-importances.md)

From the many hyper parameter tuning jobs I had run, I used the xgboost feature importance functionality to dump the perceived feature importances for all of the models. And in the [notes](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-26-feature-importances.md#2020-08-02) I plotted feature importances against accuracy for all of them.

For example, here are some of the more interesting plots,

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_37_0.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_37_1.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_37_2.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_37_3.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_37_4.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_37_5.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_37_6.png">

The point here is that I had one hot encoded all of the starting neighborhoods. I am hoping of course that if a particular starting location looks important, then that should mean it is important in discriminating where you go next. Meaning it narrows down where you go. On the other hand, if your starting location is boring then that should mean it is more like a hub and there are too many destinations for the start along to be a helpful feature.

In the above plots, there is a wide range of models and they are showing that for some reason high importance does not necessarily mean high accuracy. If anything, I want to make a mental note that maybe these kinds of plots can be indicators of something wrong and some kind of under-fitting in particular. Or weak fitting at least. And one of the other scenarios is that fitting is weak, because there is not enough entropy in the data available to yield helpful discrimination with a model. No matter how well XGBoost can extract information, if the raw material does not have any diamonds, then we will be stuck.

The other thought is that there is an overfitting danger around not just an imbalance in the target variable (aka the destination neighborhood) but an imbalance in the starting locations too. This is why it would be really interesting to also look at the entropy of the multiclass outputs for signs of clear uncertainty for specific examples. Putting a pin on this [in the follow-on section](#follow-on)

The time of day features look like this, below, but again, this is not to say that these views represent the full story.

<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_40_79.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_40_80.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_40_81.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_40_82.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_40_83.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_40_84.png">
<img src="https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-26-feature-importances_files/2020-07-26-feature-importances_40_85.png">

Thinking about this abit more in retrospect, these particular representations are probably not very meaningful to look at because if there are trends they need to be looked at "localizing" or "fixing" some of the parameters. Because these representations are all over the place but the relationship may still be hidden inside.


I think one of the top [follow ons](#follow-on) has to be to find better time of day splits. I chose my time of day splits based on a model in my head, and so there is definitely some room for  exploration here.


### Follow On

#### Time of day more splitting exploration
Find some more interesting techniques to try out different segmentation of the time of day. ( I'm thinking "adaptive binning " as described [here](https://towardsdatascience.com/understanding-feature-engineering-part-1-continuous-numeric-data-da4e47099a7b)  )

#### Better understanding of model uncertainty
* As discussed in the [feature importances section](#feature-importances), it would be really interesting to take the test dataset and for the output probability vectors of all of the examples, to calculate the multi-class entropy, to see if indeed high uncertainty is associated with worse correctness rank (`kth accuracy` and `karea` in other terminology I have been using).
* Of course this is really tricky from an _Active Learning_ point of view, because I can see a scenario where adding more training examples around the cases which have a higher uncertainty may improve the accuracy for the related test examples , but that feels like there is a risk of overfitting to the test set. In any case, however, if the live data is not reflective of the training/test data  distributions ( covariate shift ), then refreshing the model is important.


### Some lessons for the future

#### Approach to training and artifacts
Training and hyperparameter tuning takes a long time. Dumping artifacts along the way, including models and results (for example using json), is helpful to allow another notebook to actively monitor the results as they are running. And doing this is also helpful because notebooks that run long experiments can sometimes crash. So it is nice to save intermediary results.

#### Notebooks
I like the concept of keeping a daily notebook, because keeping several experiments in one notebook can risk running out of memory and sometimes it is difficult to load large notebooks on github, even if they are turned into markdown, if there are a lot of images.

#### Write sooner rather than later
* Although it is tempting to just keep trying more and more experiments and to keep iterating the frontier forward, I think a difficult lesson to learn is that putting together the results of the day or the week takes much more time when done weeks or months later. I think summarizing and discussing your results as you go along is way more useful.
* But if you do wait, another idae is to just create a notebook table of concents as I am doing below, as a way of having quick chronological reference about the work that was done.

### Notebooks TOC


* [2020-07-10](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-10-aws.md) , like "2020-07-09-aws" , another hyperparameter tuning round here. `max_depth` , `subsample` , `colsample_bytree` .
* [2020-07-11](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md) , here I plot a bunch of results (on my laptop) , from the  _2020-07-10_ notebook running on aws.
* [2020-07-16-local.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-16-local.md)  , recalculataing train metrics for the ~1250 or so models from the hyper parameter tuning session
* [2020-07-26-feature-importances.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-26-feature-importances.md) , looking at feature importances , reverse engineering my `proc_bundle` , to get back my list of feature names, which I had not done originally. Initially trying `model.get_score()`  , dumping from each model. This actually took `3.5 hours`. I plotted features and accuracy in a few ways to try to gauge features being more oftan associated with high accuracy models. Plotting the correlation of feature importance and acuracy. I think this was not a super useful method. Ultimately, [the fscore approach was better](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-21-look-at-model-plot.md)
* [2020-08-05-woe.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-08-05-woe.md) ,  EDA on the time_of_day feature, visual histogram comparisons. Not the most fruitful however.
* [2020-08-17-bundle-glue.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-08-17-bundle-glue.md)
* [2020-08-18-glue.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-08-18-glue.md) some reverse engineering to repurpose my preprocessor bundle for live etraffic. And combining preprocessor and model to make a joblib bundle with everything in it. And drafint a `full_predict` method.
* [2020-08-22-static-map-api.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-08-22-static-map-api.md)  getting setup with the Google Static Map API . Very nice.
* [2020-08-25-glue.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-08-25-glue.md) Docker entry code end to end live code. And building the code for the lambda that calls Docker. Unfortunately xgboost does not fit on the lambda. And oops lambda cannot write to the file system. And working through the new API Gateway authentication methods here. I wrote some support code for quick lambda deployment because I ended up using many iterations to get this right. Content type weirdness. Javascript plus cognito. This was not documented very well, so a lot of blundering here.  Can't believe I finally made all of this work. This was insane.
* [2020-10-20-karea-worst.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-20-karea-worst.md) K Area worst case scenario.
* [2020-10-21-look-at-model-plot.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-21-look-at-model-plot.md) looking at Fscore and as well as plotting individual trees with graphviz . Also some interesting issues with versions of xgboost in docker and lack of backward compatibility.
* [2020-10-21-uncertainty-xgboost.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-21-uncertainty-xgboost.md) this is mainly just a footnote about the idea around measuring uncertainty in xgboost. But this is likely not super reliable.
* [2020-10-22-features-v3.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-22-features-v3.md)  Take a quick look at time of day distribution
* [2020-10-23-quick-new-v3-proc-bundle.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-23-quick-new-v3-proc-bundle.md) one more model iteration using new features.
* [2020-10-25.md](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-10-25.md)  evaluate new v3. But although not yet done any tuning, so far this does not seem significantly better, with karea `0.761` versus earlier best `0.760` karea.
