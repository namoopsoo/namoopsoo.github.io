---
title: "Covid Vaccine 2 Temperatures"
date: 2021-05-29T21:05:06-04:00
tags: []
featured_image: ""
description: "Some temperature data"
summary: "Some temperature data"
---

#### Siri was suggesting that I do the vaccine remotely, but I ended up going in person
<img src="https://s3.amazonaws.com/my-blog-content/2021-05-07-covid-vaccine-2-temps/Capture d’écran 2021-05-30 à 16.33.57.png" width="50%">

#### And I thought would be nice to collect and plot some of the temperatures

<img src="https://s3.amazonaws.com/my-blog-content/2021-05-07-covid-vaccine-2-temps/2021-05-30T200945Z-fig.png" width="50%">

Here, I'm working with some self temperatures I collected in `data.csv`. Although the tylenol did not appear to have an immediate affect on my fever, I remember feeling I was cooler after even half an hour. 

(And I have some other supporting funcs [below](#some-other-supporting-functions)  )

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

    fig = plt.figure(figsize=(12,4))
    ax = fig.add_subplot(111)
    ax.plot(X, Y)

    x_labels = [unix_ts_to_dt_ts(x) for x in ax.get_xticks()]
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

#### Some other supporting functions

```python
import time
import datetime

def utc_ts():
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).strftime('%Y-%m-%dT%H%M%SZ')

def dt_to_unix_ts(dt):
    return time.mktime(dt.timetuple())

def ts_to_dt(ts):
    return datetime.datetime.strptime(ts, '%Y-%m-%d %H.%M.%S')

def unix_ts_to_dt_ts(unix_ts, utc_to_est=True):
    dt = datetime.datetime.utcfromtimestamp(unix_ts)

    if utc_to_est:
       return dt.replace(tzinfo=pytz.UTC).astimezone(pytz.timezone('US/Eastern')).strftime('%Y-%m-%d %H:%M:%S EST')
    else:
       return dt.strftime('%Y-%m-%d %H:%M:%S Z')

```
