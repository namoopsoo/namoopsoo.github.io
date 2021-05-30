---
title: "Covid Vaccine 2 Temperatures"
date: 2021-05-29T21:05:06-04:00
tags: []
featured_image: ""
description: "Some temperature data"
summary: "Some temperature data"
---

```python
import time
import datetime
def make_xtick_labels(x, step=5):
    '''Given x, step the labels every <step>
    Aka, take every <step>th x label
    '''
    x_ticks = [i for i in  range(len(x)) if i % step == 0]
    x_labels = [x[i] for i in x_ticks]
    return x_ticks, x_labels

def utc_ts():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).strftime('%Y-%m-%dT%H%M%SZ')

def dt_to_unix_ts(dt):
    return time.mktime(dt.timetuple())

def ts_to_dt(ts):
    return datetime.datetime.strptime(ts, '%Y-%m-%d %H.%M.%S')

def unix_ts_to_dt_ts(unix_ts):
    return datetime.datetime.utcfromtimestamp(unix_ts).strftime('%Y-%m-%d %H:%M:%S')

```

```python
import datetime
import pytz
import pandas as pd
import matplotlib.pyplot as plt

workdir = ...

df = pd.read_csv(f'{workdir}/data.csv')
df = pd.read_csv(f'{workdir}/data.csv', index_col=None).sort_values(by='ts')                                                                      

# df.iloc[:2]                                                                                                                                       
#    Unnamed: 0                       ts event  temp
#22          22  2021-05-03 22.46.14.jpg  temp  97.7
#12          12  2021-05-04 16.48.19.jpg  temp  97.5

df.ts = df.ts.map(lambda x: x[:-4])
df['unixts'] = df.ts.map(lambda x:dt_to_unix_ts(ts_to_dt (x)) )
X = df[df.temp.notnull()].unixts.tolist()
Y = df[df.temp.notnull()].temp.tolist()

def plot(X, Y):
    plt.grid(True)
    title = "Temperature after vaccine"

    #with plt.style.context('fivethirtyeight'):

    fig = plt.figure(figsize=(12,4))
    ax = fig.add_subplot(111)
    ax.plot(X, Y)

    x_labels = [unix_ts_to_dt_ts(x) for x in ax.get_xticks()]
    # x_ticks, x_labels = make_xtick_labels(x, step=2)
    # ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_labels, rotation=-45)
    ax.set_title(title)

    tylenol_ts = df[df.event == 'tylenol'].iloc[0].unixts
    ax.axvline(tylenol_ts, label='tylenol', color='green')

    vaccine_ts = df[df.event == 'got vaccine'].iloc[0].unixts
    ax.axvline(vaccine_ts, label='vaccine', color='red')

    plt.legend()

    out_loc = f'{workdir}/{utc_ts()}-fig.png'
    # pylab.savefig(out_loc)
    pylab.savefig(out_loc, bbox_inches='tight')

    pylab.close()

```
