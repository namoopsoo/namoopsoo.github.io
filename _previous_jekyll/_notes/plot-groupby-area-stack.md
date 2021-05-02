---
layout: post
title: Stacked area chart, using pandas dataframe and groupby date
date:   2017-11-29 17:00:01 -0500
category: pandas
tags: visualization
---

* the pandas part... will present this part later...
```python
df = pd.DataFrame({  # 7
'id': [1,2,3,4,5,6,7],
'date': ['2017-11-01', '2017-11-01', '2017-11-02', '2017-11-02', '2017-11-02', '2017-11-04', '2017-11-04', ],
'pushups': [True, False, True, True, False, False, False],
'crunches': [True, True, False, True, False, False, True],
})


def aggreg_proportions_by_row(row):
    '''Apply func used to help dedupe log data '''
    if row.shape[0] > 0:
        num_rows = row.shape[0]
        new_dict = {'units': num_rows}

        for key in ['pushups', 
                        'crunches', ]:
            foo_dict = row[key].value_counts()
            num_True = foo_dict.get(True, 0)
            new_dict.update({
                        key: num_True,
                        key + 'Proportion': num_True/num_rows}),
        new_row = pd.Series(new_dict)
        return new_row

proportions_by_date_df = df.groupby(
        by='date').apply(aggreg_proportions_by_row)

proportion_keys = ['crunchesProportion',
'pushupsProportion']

def make_xtick_labels(x, step=5):
    '''Given x, step the labels every <step>
    Aka, take every <step>th x label
    '''
    x_ticks = [i for i in  range(len(x)) if i % step == 0]
    x_labels = [x[i] for i in x_ticks]
    return {'x_ticks': x_ticks, 'x_labels': x_labels}

# Make data ready for output...
x_labels = proportions_by_date_df.index.tolist()
x = range(len(x_labels))
y = proportions_by_date_df[proportion_keys].transpose().values
y_list = y.tolist()

data = {'y': y_list, 'x': x, 'labels': proportion_keys}
data.update(make_xtick_labels(x_labels, step=1))

fn = '/Users/michal/Downloads/2017-11-30-blah-data.json'
with open(fn, 'w') as fd:
    json.dump(data, fd)
```
* jupyter...
```python
fn = '/Users/michal/Downloads/2017-11-30-blah-data.json'
with open(fn) as fd:
    data = json.load(fd)
x = data['x']
x_labels = data['x_labels']
x_ticks = data['x_ticks']
y = data['y']
labels = data['labels']

# Plot
plt.stackplot(x, y, labels=labels)
plt.legend(loc='upper left')

# use the plt.xticks function to custom labels
plt.xticks(x_ticks, x_labels, rotation=45, fontweight='bold', fontsize='10', horizontalalignment='right')
```
* ==>
![image](https://s3.amazonaws.com/my-blog-content/33415651-e1488734-d565-11e7-88cb-6eeb67574c43.png)
* In the above, used https://stackoverflow.com/a/12608937 , to finally understand how to "step" the tick marks of x axis


