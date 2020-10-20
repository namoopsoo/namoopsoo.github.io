

### What
This project is a reboot of [my earlier project](portfolio/citibike-project-readme.html)

This time around I used XGboost, newer features, hyper parameter tuning and I have a <a href="https://bike-hop-predict.s3.amazonaws.com/index.html" target="_blank"> demo site </a> as well.   ._

### TOC (wip)
* model highlights
* data used

### Earlier posts
* [xgboost notes](https://michal.piekarczyk.xyz/2020/06/21/notes-xgboost.html )




### Model Highlights

The top features are like so.



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


#### Glue notes
[Glue notes](https://github.com/namoopsoo/learn-citibike/blob/2020-oct/notes/2020-08-25-glue.md)
Here I face the challenges of taking the model from model bundle to demo site. There were a lot of challenges involved. My concept was to use the Google Static Map API to display the top neighborhood predictions. Hitting this API properly did take a little bit of time, but it was not that bad. And later on, I updated the whole AWS Lambda approach so the lambda function calls the API with the result from the dockerized SageMaker served model.

Admittedly, the most time consuming part was figuring out the API Gateway Cognito "Unauthenticated Authentication". AWS has this Cognito service which manages user/password based authentication for you but it also lets you use Anonymous authentication. But there must be a lot of degrees of freedom in how this is used, because I could not find good documentation on how to set this up properly for my usecase at all.

I had used API Gateway for authentication through CORS in the past and I recalled a bit of nuance that for example you may have setup CORS properly for `200` status codes, but if your program crashes with a `500` then your browser will scream about a CORS error, because the response is not returning the expected `allow-origin-blah` header. In the past this had taken me a while to figure out, but now I luckily had that knowledge in my back pocket. In any case, it is worth it for the serverless approach.


#### Automation made the process very convenient
https://github.com/namoopsoo/learn-citibike/blob/master/notes/2020-06-07-local-docker-notes.md

I also described my build process in the earlier mentioned [glue notes](https://github.com/namoopsoo/learn-citibike/blob/2020-oct/notes/2020-08-25-glue.md) too. With so many tweaks to the python side, the model and the javascript side, being able to build and deploy with quick `make` style commands made everything faster. I document some of these [here](https://github.com/namoopsoo/learn-citibike/blob/master/docs/common_tasks.md) too.


### Follow On

#### Better understanding of model uncertainty
* As discussed in the [feature importances section](#feature-importances), it would be really interesting to take the test dataset and for the output probability vectors of all of the examples, to calculate the multi-class entropy, to see if indeed high uncertainty is associated with worse correctness rank (`kth accuracy` and `karea` in other terminology I have been using).
* Of course this is really tricky from an _Active Learning_ point of view, because I can see a scenario where adding more training examples around the cases which have a higher uncertainty may improve the accuracy for the related test examples , but that feels like there is a risk of overfitting to the test set. In any case, however, if the live data is not reflective of the training/test data  distributions ( covariate shift ), then refreshing the model is important. 
