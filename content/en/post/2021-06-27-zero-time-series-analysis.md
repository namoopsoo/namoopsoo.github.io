---
title: Fasting Data Time Series Analysis Notebook
tags:
  - time-series
  - notebook
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

### 2021-06-30

#### quick notes
* Also realized that the time between fasts can be a feature too.

* For each "row", we can basically say the "End time" is a separator between what happened before a fasting event, which can be used to create the "X" or independent variables and what happens after is the "Y" or dependent variables.
* So for each row, if using pandas for example, we want a way to take perhaps 4 or more rows surrounding it and that would be used to create the features.
* Perhaps this feels like a job for  [rolling window](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.core.window.rolling.Rolling.apply.html#pandas.core.window.rolling.Rolling.apply) , [interesting article](https://towardsdatascience.com/dont-miss-out-on-rolling-window-functions-in-pandas-850b817131db)

```python

# most recent fast started before midnight


```

#### updated feature list

#### Feature list initial
* most recent fast started before midnight
* most recent fast ended before 20:00
* most recent fast more than 18 hours
* most recent fast more than 16 hours
* most recent fast more than 14 hours
* last two fasts, average start time before midnight
* last two fasts, both start time before midnight
* last two fasts, average end time before 20:00
* last two fasts, average more than 18 hours
* last two fasts, average more than 16 hours
* last two fasts, max is more than 18 hours
* last two fasts, min is more than 18 hours
* last two fasts, m in is more than 16 hours
* last two feeding windows, average less than 4 hours

### 2021-07-07

#### tried this rolling calc
* Looks good just need to calibrate the direction.
```python
df['RollingHoursMean2Fasts'] = df['Hours'].rolling(2).mean()

In [8]: df.iloc[:10]                                                                  
Out[8]:
      Date  Start    End  Hours  Night Eating  RollingHoursMean2Fasts
0  6/26/21  01:57    NaN    NaN           NaN                     NaN
1  6/25/21  00:14  17:17   17.0           NaN                     NaN
2  6/24/21  01:50  18:39   16.0           NaN                    16.5
3  6/23/21  01:02  19:21   18.0           NaN                    17.0
4  6/22/21  00:06  17:52   17.0           NaN                    17.5
5  6/21/21  01:46  20:55   19.0           NaN                    18.0
6  6/20/21  04:39  13:28    8.0           NaN                    13.5
7  6/19/21  02:37  18:21   15.0           NaN                    11.5
8  6/18/21  01:41  18:41   17.0           NaN                    16.0
9  6/17/21  01:02  21:38   20.0           NaN                    18.5
```

### 2021-07-09

* Add index too...

```python
import datetime
df['StartDt'] =  df.apply(lambda x: datetime.datetime(int(f"20{x.Date.split('/')[2]}"),
                                                      int(x.Date.split("/")[0]),
                                                      int(x.Date.split("/")[1]),
                                                      int(x.Start.split(":")[0]),
                                                      int(x.Start.split(":")[1])
                                                      ), axis=1)
df['id'] = df.apply(lambda x: x.StartDt.strftime("%Y-%m-%dT%H%M"), axis=1)

In [21]: df.iloc[:10]                                                                                                                 
Out[21]:
      Date  Start    End  Hours  Night Eating  RollingHoursMean2Fasts             StartDt               id
0  6/26/21  01:57    NaN    NaN           NaN                     NaN 2021-06-26 01:57:00  2021-06-26T0157
1  6/25/21  00:14  17:17   17.0           NaN                     NaN 2021-06-25 00:14:00  2021-06-25T0014
2  6/24/21  01:50  18:39   16.0           NaN                    16.5 2021-06-24 01:50:00  2021-06-24T0150
3  6/23/21  01:02  19:21   18.0           NaN                    17.0 2021-06-23 01:02:00  2021-06-23T0102
4  6/22/21  00:06  17:52   17.0           NaN                    17.5 2021-06-22 00:06:00  2021-06-22T0006
5  6/21/21  01:46  20:55   19.0           NaN                    18.0 2021-06-21 01:46:00  2021-06-21T0146
6  6/20/21  04:39  13:28    8.0           NaN                    13.5 2021-06-20 04:39:00  2021-06-20T0439
7  6/19/21  02:37  18:21   15.0           NaN                    11.5 2021-06-19 02:37:00  2021-06-19T0237
8  6/18/21  01:41  18:41   17.0           NaN                    16.0 2021-06-18 01:41:00  2021-06-18T0141
9  6/17/21  01:02  21:38   20.0           NaN                    18.5 2021-06-17 01:02:00  2021-06-17T0102
```
* Looking at above, I see that `RollingHoursMean2Fasts` for `2021-06-24T0150` is `16.5 = mean([17, 16])` , so the rows it is taking into account should be current row and next not current row and last

#### Next
* Make `RollingHoursMean2Fasts` be for current and previous fast , not current and future fast haha since cannot know the future!

### 2021-07-10

#### how to update the rolling window to reflect the last 2 fasts

```python

df['foo'] = df['Hours'].shift(-1)
df['RollingHoursMean2Fasts'] = df['Hours'].shift(-1).rolling(2).mean()
```
* Nice, per the below, this is perfect.
```python
In [33]: cols = ['id', 'Date', 'Start', 'End', 'Hours', 'RollingHoursMean2Fasts', 'foo']
    ...: df[cols].iloc[:10]                                                                                                           
Out[33]:
                id     Date  Start    End  Hours  RollingHoursMean2Fasts   foo
0  2021-06-26T0157  6/26/21  01:57    NaN    NaN                     NaN  17.0
1  2021-06-25T0014  6/25/21  00:14  17:17   17.0                    16.5  16.0
2  2021-06-24T0150  6/24/21  01:50  18:39   16.0                    17.0  18.0
3  2021-06-23T0102  6/23/21  01:02  19:21   18.0                    17.5  17.0
4  2021-06-22T0006  6/22/21  00:06  17:52   17.0                    18.0  19.0
5  2021-06-21T0146  6/21/21  01:46  20:55   19.0                    13.5   8.0
6  2021-06-20T0439  6/20/21  04:39  13:28    8.0                    11.5  15.0
7  2021-06-19T0237  6/19/21  02:37  18:21   15.0                    16.0  17.0
8  2021-06-18T0141  6/18/21  01:41  18:41   17.0                    18.5  20.0
9  2021-06-17T0102  6/17/21  01:02  21:38   20.0                    18.5  17.0
```

#### Ok, going to add two more features like this
* last two fasts, both start time before midnight, "LastTwoFastsStartedBeforeMidnight"

```python
def func(x):
    pass
    import ipdb; ipdb.set_trace()
    return all([18 <= int(a.split(":")[0]) <=23 for a in x])

df["LastTwoFastsStartedBeforeMidnight"] = df['Start'].shift(-1).rolling(2).apply(func)


```
* I encountered `DataError: No numeric types to aggregate` and deeper in there I also stumbled on
```
ValueError: could not convert string to float: '00:14'
```
* So got to convert first to a numerical..

```python
def func(data):
    return all([18 <= x <=23 for x in data])

df["StartHour"] = df["Start"].map(lambda x: int(x.split(":")[0]))

df["LastTwoFastsStartedBeforeMidnight"] = df['StartHour'].shift(-1).rolling(2).apply(func)

```
* Ok I think that worked ..

```python
In [57]: df.LastTwoFastsStartedBeforeMidnight.value_counts()                                                                          
Out[57]:
0.0    907
1.0    200
Name: LastTwoFastsStartedBeforeMidnight, dtype: int64

In [60]: cols = ['id', 'Date', 'Start', 'End', 'Hours', 'LastTwoFastsStartedBeforeMidnight',]
    ...: df[cols].iloc[35:45]                                                                                                         
Out[60]:
                 id     Date  Start    End  Hours  LastTwoFastsStartedBeforeMidnight
35  2021-05-21T2341  5/21/21  23:41  21:02   21.0                                0.0
36  2021-05-21T0026  5/21/21  00:26  20:31   20.0                                0.0
37  2021-05-20T0101  5/20/21  01:01  20:57   19.0                                0.0
38  2021-05-19T0008  5/19/21  00:08  20:29   20.0                                0.0
39  2021-05-17T2324  5/17/21  23:24  21:38   22.0                                1.0
40  2021-05-16T2300  5/16/21  23:00  20:21   21.0                                1.0
41  2021-05-15T2358  5/15/21  23:58  14:06   14.0                                0.0
42  2021-05-15T0110  5/15/21  01:10  21:42   20.0                                0.0
43  2021-05-14T0049  5/14/21  00:49  17:53   17.0                                0.0
44  2021-05-13T0015  5/13/21  00:15  17:26   17.0                                0.0
```

#### Next
* Ok at this point I should start throwing stuff into version control so creating these features and visualizing/analyzing them can be more deterministic/reproducible.
* And then I can try visualizing / understanding some features and see how predictive they are w.r.t. "does past behavior determine future behavior such as the length of the next fast".


### 2021-07-11

#### ok started things off in a new repo

```python
import os
import core.dataset as cd

import pandas as pd
workdir = os.getenv("WORKDIR")
datadir = os.getenv("DATADIR")

loc = f"{datadir}/2021-06-26-zero-fast.csv"
df = pd.read_csv(loc)

datasetdf = cd.build_dataset(df)

In [11]: datasetdf.iloc[:10]                                                                                                          
Out[11]:
      Date  Start    End  Hours  ...               id StartHour LastTwoFastsStartedBeforeMidnight  RollingHoursMean2Fasts
0  6/26/21  01:57    NaN    NaN  ...  2021-06-26T0157         1                               NaN                     NaN
1  6/25/21  00:14  17:17   17.0  ...  2021-06-25T0014         0                               0.0                    16.5
2  6/24/21  01:50  18:39   16.0  ...  2021-06-24T0150         1                               0.0                    17.0
3  6/23/21  01:02  19:21   18.0  ...  2021-06-23T0102         1                               0.0                    17.5
4  6/22/21  00:06  17:52   17.0  ...  2021-06-22T0006         0                               0.0                    18.0
5  6/21/21  01:46  20:55   19.0  ...  2021-06-21T0146         1                               0.0                    13.5
6  6/20/21  04:39  13:28    8.0  ...  2021-06-20T0439         4                               0.0                    11.5
7  6/19/21  02:37  18:21   15.0  ...  2021-06-19T0237         2                               0.0                    16.0
8  6/18/21  01:41  18:41   17.0  ...  2021-06-18T0141         1                               0.0                    18.5
9  6/17/21  01:02  21:38   20.0  ...  2021-06-17T0102         1                               0.0                    18.5

[10 rows x 10 columns]

In [12]: datasetdf.iloc[0]                                                                                                            
Out[12]:
Date                                             6/26/21
Start                                              01:57
End                                                  NaN
Hours                                                NaN
Night Eating                                         NaN
StartDt                              2021-06-26 01:57:00
id                                       2021-06-26T0157
StartHour                                              1
LastTwoFastsStartedBeforeMidnight                    NaN
RollingHoursMean2Fasts                               NaN
Name: 0, dtype: object

```

#### look at RollingHoursMean2Fasts briefly

```python
import matplotlib.pyplot as plt

import pylab
import date_utils as du

col = "RollingHoursMean2Fasts"
loc = f"{workdir}/{du.utc_ts()}-{col}.png"
with plt.style.context('fivethirtyeight'):
    plt.plot(datasetdf[col].tolist())
    plt.title(f'{col}')
    pylab.savefig(loc, bbox_inches='tight')
    pylab.close()

```

<img src="https://s3.amazonaws.com/my-blog-content/2021-06-27-zero-time-series-analysis/2021-07-11T173459-RollingHoursMean2Fasts.png" width="50%">


#### Next
* I think the main next thing to do is to create a "y" dependent variable for this dataset, which can for example be something like "hours fasted in next fast" or "hours until next fast" or "proportion of hours fasted in next 7 days".
* And with a dependent variable I can then see how predictive these features are, as a first iteration with only the twofeatures so far.
* And I can continue to add other features too.
