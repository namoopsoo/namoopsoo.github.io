

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



#### Glue notes
[Glue notes](https://github.com/namoopsoo/learn-citibike/blob/2020-oct/notes/2020-08-25-glue.md)
Here I face the challenges of taking the model from model bundle to demo site. There were a lot of challenges involved. My concept was to use the Google Static Map API to display the top neighborhood predictions. Hitting this API properly did take a little bit of time, but it was not that bad. And later on, I updated the whole AWS Lambda approach so the lambda function calls the API with the result from the dockerized SageMaker served model.

Admittedly, the most time consuming part was figuring out the API Gateway Cognito "Unauthenticated Authentication". AWS has this Cognito service which manages user/password based authentication for you but it also lets you use Anonymous authentication. But there must be a lot of degrees of freedom in how this is used, because I could not find good documentation on how to set this up properly for my usecase at all.

I had used API Gateway for authentication through CORS in the past and I recalled a bit of nuance that for example you may have setup CORS properly for `200` status codes, but if your program crashes with a `500` then your browser will scream about a CORS error, because the response is not returning the expected `allow-origin-blah` header. In the past this had taken me a while to figure out, but now I luckily had that knowledge in my back pocket. In any case, it is worth it for the serverless approach.
