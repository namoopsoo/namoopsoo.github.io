---
layout: post
title:  "Bike Share Learn Reboot"
date:   2020-10-20 10:00:05 -0400
---

<img src="https://s3.amazonaws.com/my-blog-content/2020/2020-10-20-bike-share-learn-reboot/IMG_8499.jpg" width="40%">


### What
This project is a reboot of [my earlier project](/portfolio/citibike-project-readme.html) of predicting bicycle ride share riders destinations.
https://bike-hop-predict.s3.amazonaws.com/index.html

This time around I used XGBoost, newer features, hyper parameter tuning and I have a <a href="https://bike-hop-predict.s3.amazonaws.com/index.html" target="_blank"> demo site </a> as well.   ._
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
* [Xgboost notes](#earlier-xgboost-notes)
* [Previously](#previously-vs-this-time)
* [model highlights](#model-highlights)
* data used
* [Glue notes](#glue-notes)
* [Looking at hyperparameter tuning results](#looking-at-hyperparameter-tuning-results)
* [Follow on](#follow-on)

### Earlier Xgboost notes
* [xgboost notes](https://michal.piekarczyk.xyz/2020/06/21/notes-xgboost.html )

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

Extracting from [this notebook](https://github.com/namoopsoo/learn-citibike/edit/master/notes/2020-10-21-look-at-model-plot.md) ,

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

I think one of the top [follow ons](#follow-on) has to be to find better time of day splits. I chose my time of day splits based on a model in my head, and so there is definitely some room for  exploration here.

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

I spent a bit of time on hyper parameter tuning, looking at the results, fixing some parameters two focus on two others at a time.

So per [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#looking-at-num_round-fundamentally) ,
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
<img src"https://github.com/namoopsoo/learn-citibike/raw/master/notes/2020-07-11-local_files/2020-07-11-local_13_0.png>

And from [here](https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#learning-rate-and-walltime) it was interesting to see that walltime is stable mostly when it comes to learning rate except sometimes...

<img src="https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local_files/2020-07-11-local_15_0.png">

https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md
https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-11-local.md#learning-rate-and-walltime

https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-07-16-local.md

#### Initial time of day look
https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-08-05-woe.md

 super

#### discuss
https://github.com/namoopsoo/learn-citibike/blob/2020-oct/notes/2020-08-25-glue.md

### Follow On

#### Time of day more splitting exploration
Find some more interesting techniques to try out different segmentation of the time of day.

#### Better understanding of model uncertainty
* As discussed in the [feature importances section](#feature-importances), it would be really interesting to take the test dataset and for the output probability vectors of all of the examples, to calculate the multi-class entropy, to see if indeed high uncertainty is associated with worse correctness rank (`kth accuracy` and `karea` in other terminology I have been using).
* Of course this is really tricky from an _Active Learning_ point of view, because I can see a scenario where adding more training examples around the cases which have a higher uncertainty may improve the accuracy for the related test examples , but that feels like there is a risk of overfitting to the test set. In any case, however, if the live data is not reflective of the training/test data  distributions ( covariate shift ), then refreshing the model is important.
