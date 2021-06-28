---
title: Fasting Data Time Series Analysis Notebook
tags: time-series, notebook
date: 2021-06-27
summary: This is a notebook of the day to day activity of a look into three years of fasting data.
---

This is a notebook of the day to day activity of a look into three years of fasting data.

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

### 2021-06-28

#### build dataset...

```python
import os
import pandas as pd
workdir = os.getenv("WORKDIR")
datadir = os.getenv("DATADIR")

loc = f"{datadir}/2021-06-26-zero-fast.csv"
df = pd.read_csv(loc)



In [3]: df.shape                                                                
Out[3]: (1109, 5)

In [4]: df.iloc[:4]                                                             
Out[4]:
      Date  Start    End  Hours  Night Eating
0  6/26/21  01:57    NaN    NaN           NaN
1  6/25/21  00:14  17:17   17.0           NaN
2  6/24/21  01:50  18:39   16.0           NaN
3  6/23/21  01:02  19:21   18.0           NaN
```
* Probably the simples question, is what is a unit of fasting? A fast can start and end on two different dates or it can start and end on the same day.
* A Fast can also span multiple days and it can also happen while traveling, resulting in different time zones messing with the data.
* However this dataset doesn't appear to have time zones, so I wonder if it kind of simplifies that.
* Simplest I think is to ignore the first row for example,

```
      Date  Start    End  Hours  Night Eating
0  6/26/21  01:57    NaN    NaN           NaN

```
* Since this fast is on-going. So a fast unit has a start and an end.

```python
In [6]:  df[df.Hours.isnull()].shape, df.shape                                  
Out[6]: ((1, 5), (1109, 5))
```
* Ok per above only the latest fast would be null then.


#### Next
* Start writing that dataset
* write a fast id perhaps as the "start-date-start-time" which would be unique, and has to have defined end of course.
* And figure out what does that "Night Eating" column mean.
* names for the features I started writing out.
