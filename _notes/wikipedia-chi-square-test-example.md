---
layout: post
title: Doing the wikipedia chi square example
date:   2017-11-26 12:00:01 -0500
---

The simple goal here is to take the example in https://en.wikipedia.org/wiki/Chi-squared_test#Example_chi-squared_test_for_categorical_data and finish calculating the test statistic. It looks like at the time of this writing that was left as an exercise for the reader.




```python
from __future__ import division
```


```python
import numpy as np
```


```python
# lets say oee(o,e) is the calculation done in each of the 3x4 cells
oee = lambda o,e: ((o - e)**2)/e
```


```python
data = np.array([[90,60,104,95],[30,50,51,20],[30,40,45,35]])
```


```python
# Total number of people sampled.
total = data.sum()
```


```python
total
```




    650




```python
num_classes, num_neighborhoods = data.shape[0], data.shape[1]
```


```python
num_classes, num_neighborhoods
```




    (3, 4)




```python
# totals for each neighborhood
neighborhood_totals = [
    sum([data[i][j] for i in range(num_classes)]) for j in range(num_neighborhoods)]
```


```python
neighborhood_totals
```




    [150, 150, 200, 150]




```python
# get expected value of a class on a given neighborhood
```


```python
# lets find the expected values for each of the three classes white collar, blue collar and no collar
class_totals = [data[i].sum() for i in range(num_classes)]
```


```python
class_totals
```




    [349, 151, 150]




```python
class_probability_priors = [class_totals[i]/total for i in range(num_classes)]
```


```python
class_probability_priors
```




    [0.53692307692307695, 0.2323076923076923, 0.23076923076923078]




```python
expected_values = [
    [((neighborhood_totals[j])*(class_totals[i]/total))
     for j in range(num_neighborhoods)]
    for i in range(num_classes)]
```


```python
expected_values
```




    [[80.538461538461547,
      80.538461538461547,
      107.38461538461539,
      80.538461538461547],
     [34.846153846153847,
      34.846153846153847,
      46.46153846153846,
      34.846153846153847],
     [34.61538461538462, 34.61538461538462, 46.153846153846153, 34.61538461538462]]




```python
# sum of cells on first neighborhood expected values should match the actual sum ...
print 80.54 + 34.85 + 34.62
print neighborhood_totals[0]
```

    150.01
    150



```python
# ok cool ^^ that looks about right.
```


```python
# lets get the values of (observed - expected)^2 / (expected)  , for each of the 3x4 cells
parts = np.array([[oee(data[i][j], expected_values[i][j])
         for j in range(num_neighborhoods)]
          for i in range(num_classes)])
```


```python
parts
```




    array([[  1.11152744e+00,   5.23760194e+00,   1.06678422e-01,
              2.59672324e+00],
           [  6.73968416e-01,   6.59008321e+00,   4.43326541e-01,
              6.32518254e+00],
           [  6.15384615e-01,   8.37606838e-01,   2.88461538e-02,
              4.27350427e-03]])




```python
# the chi square test statistic
test_statistic = parts.sum()
```


```python
test_statistic
```




    24.571202858582595




```python
expected_values[0][3], oee(95, expected_values[0][3])
```




    (80.538461538461547, 2.596723238557046)


So if per the wikipedia page, the number of degrees of freedom here 
is `(3 - 1)(4 - 1) = 6`
just eye balling https://en.wikipedia.org/wiki/File:Chi-square_pdf.svg  , I think the probability of `24.57` given k=6 degrees of freedom is a bit low...

So the null hypothesis that " each persons neighborhood of residence is independent of the persons occupational classification " feels like it can be rejected.. 

```python
# for the sake of argument... lets engineer a dataset which should pass the null hypothesis...
# basically lets match the expected values... approximatly.. 
data2 = np.array([
    [np.floor(expected_values[i][j]) for j in range(num_neighborhoods)]
          for i in range(num_classes)
])
```


```python
data2
```




    array([[  80.,   80.,  107.,   80.],
           [  34.,   34.,   46.,   34.],
           [  34.,   34.,   46.,   34.]])




```python
# total here should be roughly like total above i think
data2.sum()
```




    643.0




```python
# calculate the test statistic for data2...
def get_test_statistic(the_data):
    total = the_data.sum()
    num_classes, num_neighborhoods = the_data.shape[0], the_data.shape[1]
    
    neighborhood_totals = [
    sum([the_data[i][j] for i in range(num_classes)]) for j in range(num_neighborhoods)]

    neighborhood_totals = [
        sum([the_data[i][j] for i in range(num_classes)])
        for j in range(num_neighborhoods)]

    class_totals = [the_data[i].sum() for i in range(num_classes)]

    expected_values = [
        [((neighborhood_totals[j])*(class_totals[i]/total))
         for j in range(num_neighborhoods)]
        for i in range(num_classes)]

    parts = np.array([[oee(the_data[i][j], expected_values[i][j])
         for j in range(num_neighborhoods)]
          for i in range(num_classes)])

    test_statistic = parts.sum()
    return test_statistic

```


```python
get_test_statistic(data2)
```




    0.0044994022598769338




```python
# wow thats almost 0 but hmm.. the probability value for a chi-square distribution of k=6 ,
# for x=0.004499 is pretty small.. 
# hmmm..
```
