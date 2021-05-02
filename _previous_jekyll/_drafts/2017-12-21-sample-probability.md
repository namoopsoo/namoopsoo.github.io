---
layout: post
title: What does sampling do to a rate
date:   2017-12-28 15:00:01 -0500
category: pandas
tags: sampling,probability,visualization,pandas
---


### Notes

if we have error T,F, in a population of Sentry data. but we have the roughly 10% sampled output. And observe an error rate, what is the probability range for this error rate? 

(side context is that these are "address validation" sentry logs. and my "error rate" here is the address output being empty [] ). Otherwise it is the (1 - pass rate) basically. 

This would be cool to do some example code around, w/ trials. 

### trials
There are a few ways to think about this. Sampling feels like removing items from a bag and throwing out 90% of them, but at random, for example.

For a simpler scenario, let's first use the Python `random` library to see what sampling does to the _True Rate_.

#### Setup
```python
import pandas as pd
import random

n_experiments = 100000
n_trials = 10000

def run_an_experiment(n_trials):
    '''Run an experiment, for n trials,

    With sampling probability, use a trial result
    for the tabulation, otherwise, ignore it
    '''
    counts = {'sampled_true': 0,
            'sampled_false': 0}

    for i in range(n_trials):
        r = random.random()
        if r < 0.1:
            # True rate
            p = random.random()
            if p < 0.8:
                counts['sampled_true'] += 1
            else:
                counts['sampled_false'] += 1

    return counts

def main():
    experiments = []

    for i in range(n_experiments):
        result = run_an_experiment(n_trials)
        experiments.append(result)
    dfraw = pd.DataFrame.from_records(experiments)
    return dfraw
```
* running this...
```python
In [1]: import experiment


In [2]: results = experiment.main()

In [3]: len(results)
Out[3]: 100

In [4]: results[:5]
Out[4]: 
[{'sampled_false': 210, 'sampled_true': 840},
 {'sampled_false': 199, 'sampled_true': 821},
 {'sampled_false': 170, 'sampled_true': 775},
 {'sampled_false': 186, 'sampled_true': 840},
 {'sampled_false': 214, 'sampled_true': 784}]


```
* Okay. that was instantaneous and output looks normal. Let's get more trials in there... ( Changed from `100` to `100,000` trials...
```python

In [7]: %time results2 = experiment.main()
CPU times: user 2min 18s, sys: 171 ms, total: 2min 19s
Wall time: 2min 19s

In [8]: len(results2)
Out[8]: 100000

In [15]: dfraw = pd.DataFrame.from_records(results2)

In [19]:     dfraw['sampleTrueRate'] = dfraw.sampled_true / (dfraw.sampled_true +
    ...:  dfraw.sampled_false)
    ...: 

In [20]: dfraw.head()
Out[20]: 
   sampled_false  sampled_true  sampleTrueRate
0            194           754        0.795359
1            212           795        0.789474
2            200           780        0.795918
3            194           822        0.809055
4            201           774        0.793846
```
* now lets bin this sample true rate , using the nearest hundredth.
```python

In [26]: dfraw.sampleTrueRate.head().map(lambda x: decimal.Decimal(x).quantize(de
    ...: cimal.Decimal('0.01')))
Out[26]: 
0    0.80
1    0.79
2    0.80
3    0.81
4    0.79
Name: sampleTrueRate, dtype: object

In [27]: dfraw['sampleTrueRateRounded'] = dfraw.sampleTrueRate.map(lambda x: deci
    ...: mal.Decimal(x).quantize(decimal.Decimal('0.01')))

In [30]: dfraw.head()
Out[30]: 
   sampled_false  sampled_true  sampleTrueRate sampleTrueRateRounded
0            194           754        0.795359                  0.80
1            212           795        0.789474                  0.79
2            200           780        0.795918                  0.80
3            194           822        0.809055                  0.81
4            201           774        0.793846                  0.79

In [32]: dfraw['unit'] = [1]*dfraw.shape[0]

In [36]: gpby = dfraw[['sampleTrueRateRounded', 'unit']].groupby(by='sampleTrueRa
    ...: teRounded')

In [37]: import numpy as np

In [39]: bindf = gpby.aggregate(np.sum)

In [40]: bindf.shape
Out[40]: (12, 1)

In [41]: bindf
Out[41]: 
                        unit
sampleTrueRateRounded       
0.74                       1
0.75                      22
0.76                     311
0.77                    2228
0.78                    9327
0.79                   22550
0.80                   30571
0.81                   23367
0.82                    9352
0.83                    2040
0.84                     217
0.85                      14

In [42]: bindf.sum()
Out[42]: 
unit    100000
dtype: int64

```
* Just looking at this, we see that we don't have `100%` of the trials on `(0.79,0.81)`, but it is a lot there.
```python
In [45]: newdf = pd.DataFrame(index=range(bindf.shape[0]))

In [46]: newdf['sampleTrueRateRounded'] = bindf.index



In [53]: newdf['Frequency'] = bindf.unit.values

In [55]: newdf['RelativeFrequency'] = newdf.Frequency/100000

In [56]: newdf
Out[56]: 
   sampleTrueRateRounded  Frequency  RelativeFrequency
0                   0.74          1            0.00001
1                   0.75         22            0.00022
2                   0.76        311            0.00311
3                   0.77       2228            0.02228
4                   0.78       9327            0.09327
5                   0.79      22550            0.22550
6                   0.80      30571            0.30571
7                   0.81      23367            0.23367
8                   0.82       9352            0.09352
9                   0.83       2040            0.02040
10                  0.84        217            0.00217
11                  0.85         14            0.00014

In [57]: newdf.RelativeFrequency.sum()
Out[57]: 1.0

In [59]: newdf.to_csv('/blahblah/repo/sample-probabili
    ...: ty-experiment-2017-12/experiment-2-binned.csv', index=False)


```
####  Meanwhile in jupyter...




```python
%matplotlib inline

import seaborn as sns
import pandas as pd

```

    /usr/local/miniconda3/envs/blogplt/lib/python3.6/site-packages/matplotlib/font_manager.py:281: UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.
      'Matplotlib is building the font cache using fc-list. '



```python
fn = '/Users/michal/LeDropbox/Dropbox/Code/repo/sample-probability-experiment-2017-12/experiment-2-binned.csv'

```


```python
binned_df = pd.read_csv(fn)
binned_df
```




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
      <th>sampleTrueRateRounded</th>
      <th>Frequency</th>
      <th>RelativeFrequency</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.74</td>
      <td>1</td>
      <td>0.00001</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.75</td>
      <td>22</td>
      <td>0.00022</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.76</td>
      <td>311</td>
      <td>0.00311</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.77</td>
      <td>2228</td>
      <td>0.02228</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.78</td>
      <td>9327</td>
      <td>0.09327</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0.79</td>
      <td>22550</td>
      <td>0.22550</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0.80</td>
      <td>30571</td>
      <td>0.30571</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0.81</td>
      <td>23367</td>
      <td>0.23367</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0.82</td>
      <td>9352</td>
      <td>0.09352</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0.83</td>
      <td>2040</td>
      <td>0.02040</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0.84</td>
      <td>217</td>
      <td>0.00217</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0.85</td>
      <td>14</td>
      <td>0.00014</td>
    </tr>
  </tbody>
</table>
</div>




```python
ax = sns.barplot(x="sampleTrueRateRounded", y="RelativeFrequency", data=binned_df, 
                 palette="Blues_d")
```


![png](output_3_0.png)

<img src="https://my-blog-content.s3.amazonaws.com/2017/12-21/output_3_0.png"/>



### Side notes
 If we have a proportion of p = P(T) = 0.10 and q = P(F) = 0.9 , and we choose 10% (aka sampling rate),  this is basically like a  (10000C1000)(p^x)(q^y) for example if n=10,000. And that is for a specific value of x + y = 1000 being chosen.

so yea, sampling is binomial distribution.

