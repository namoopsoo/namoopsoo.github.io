---
title: Fasting Data Time Series Analysis Notebook
tags: time-series, notebook
---

### 2021-06-27

#### Initial thoughts
* I have about 3 years of fasting data now and I would like to see if something interesting can be said about it. And if given some time series data, is it possible to predict the next day. Or at least something about the next day.
* I suspect the data is somewhat cyclical at least with respect to patterns of "restraint" and "indulgence" , but also maybe with respect to week and weekend.
* Initially I think I want to use frequency based features, but perhaps afterwards I can compare that with an LSTM approach.
* I also have some calorie data, but it is only for about 3 months or so, and maybe I can use that somehow too later.
* Perhaps I can even later on try using exercise data, sleep data if available. And there is of course temperature and weather data.

#### Next steps
* Write out some interesting questions I would like to answer.
* What is my feature list so far , as a sort of data dictionary.
* Can do some initial data exploration, with visualizations.
* Build a dataset based on some initial features,

#### Interesting Questions ?
* Given a sequence of days, is there an interesting target variable, such as the hours fasted, which can be predicted of the next day or even the next few days or next week?
* A core qualitative question is, whether a period of restraint (more fasting) is followed by a period of less restraint (less fasting)?
* And maybe an extension of the above is whether fasting appears to be cyclical and how would you even measure this?
* How does the number of prior days of activity improve the accuracy of the prediction of the next day?

#### Feature list initial
* most recent fast started before midnight
* most recent fast ended before 20:00
* most recent fast more than 18 hours
* most recent fast more than 16 hours
* most recent fast more than 14 hours
* last two fasts, average start time before midnight
* last two fasts, average end time before 20:00
* last two fasts, average more than 18 hours
* last two fasts, average more than 16 hours
* last two fasts, max is more than 18 hours
* last two fasts, min is more than 18 hours
* last two fasts, m in is more than 16 hours


#### Next
* Yea next I would like to start building out a dataset of these features
* And would be cool to visualize some of these features too, get some summary stats on them. 
