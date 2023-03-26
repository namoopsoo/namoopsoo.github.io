---
title: Alternate Day Feasting
date: 2023-03-25
tags:
  - fasting
  - nutrition
cover:
  image: "https://s3.amazonaws.com/my-blog-content/2023/2023-03-25-Alternate-Day-Feasting/2023-03-26T191146-figure_1679859645507_0.png"
---
### First Stab at Alternate Day Feasting

#### Wait Don't you mean Alternate Day Fasting?
Haha yes but I am still working up to the level of stoicism required to do proper [Alternate Day Fasting](https://www.dietdoctor.com/weight-loss/alternate-day-fasting) and a low stress life also helps especially if you rely on snacks to counter the stress of the daily Work-From-Home-Wake-Up-Surprise-You-Are-At-Work-And-Work-Throughout-The-Entire-Day-Life haha!
      
But having already been doing Time Restricted Feeding for several years now, I think I have the stoicism requirements to at least give Alternate Day Feasting a go, which is basically aiming at calorie restriction every other day.

#### I have pulled my daily calorie data from Carb Manager and electronic weigh-in data from a Withings scale I have.
      
The first plot I did looks like 
      
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-03-25-Alternate-Day-Feasting/2023-03-25T175301-figure-flip-the-order_1679801795782_0.png" width="90%">}}

      
but maybe it is a bit noisy since it has all the data for each day, so trying also a 7 day average too,
      
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-03-25-Alternate-Day-Feasting/2023-03-26T204315-figure_1679863701207_0.png" width="90%">}}

Also tried , 7 day sum too, 
{{< figure src="https://s3.amazonaws.com/my-blog-content/2023/2023-03-25-Alternate-Day-Feasting/2023-03-26T204150-figure_1679863710325_0.png" width="90%">}}



#### So What happened?
Well the whole reason I started looking at all this was that I started a Work From Home job in December 2021 and although prior to that, I used to bike-commute to work every day, now bike rides in 2022 I admit have been way shorter, say, 3 to 6 miles a day as opposed to 12+ miles a day. 
      
And alarmingly I saw my weight go up in 2022, perhaps similar to what I recall Iñigo San-Millán described in this interview, https://peterattiamd.com/inigosanmillan/ with Peter Attia , about cyclists who reduce their cycling without reducing their calorie intake.
      
Of course I was nowhere near a professional cyclist and I'm sure the weight gain is related to a lack of stress management to a large extent, but nevertheless, basically starting 2023, every other day, I aimed for a lower amount of calories.
      
The first plot above does not show this very well, but the second chart, which takes 7-day averages, hopefully does a better job.

There are also other behavior changes I'm trying too that are not being plotted here, including the replacement of highly processed food with slightly less processed food and also improving the overall [protein to energy ratio](https://www.dietdoctor.com/high-protein/eat-more-protein).

#### How to generate these plots?
There was a bit of trial and error I can describe later, but basically, 
```python
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pylab
from pathlib import Path
from datetime import datetime, date, timedelta

from core.date_utils import utc_ts


def make_xtick_labels(x, step=5):
    '''Given x, step the labels every <step>
    Aka, take every <step>th x label
    '''
    x_ticks = [i for i in  range(len(x)) if i % step == 0]
    x_labels = [x[i] for i in x_ticks]
    return x_ticks, x_labels

root_dir = Path(os.getenv("ROOT_DIR"))

def get_data():
    # Prepare food df
    food_logs_loc = (root_dir / "CarbManager/daily_logs_20210312-20230318_fe628b90-9859-4259-ab49-1ba3ce95b90c.csv")
    food_df = pd.read_csv(food_logs_loc)

    cols = ["RawDate", "Meal", "Calories"]
    food_df["RawDate"] = food_df["Date"].map(lambda x: x.split(" ")[0])
    food_df[food_df.Meal.isin(["Snack", "Dinner", "Lunch", "Breakfast"])][cols].iloc[-10:]
    food_agg_df = food_df[["RawDate", "Calories"]].groupby(by=["RawDate"]).sum().reset_index()


    weight_loc = root_dir / ("withings/2023-03-18-data_MIC_1679186118/weight.csv")
    weight_df = pd.read_csv(weight_loc)
    cols = ["Date", "Weight (lb)"]
    weight_df[cols].sort_values(by="Date").iloc[-10:]
    weight_df["RawDate"] = weight_df["Date"].map(lambda x: x.split(" ")[0])
    cols = ["RawDate", "Weight (lb)"]
    weight_agg_df = weight_df[cols].groupby(by="RawDate").min().reset_index()
    return food_agg_df, weight_agg_df

def find_closest_date(dates, date):
    """
    Examples 
    In [13]: from datetime import datetime, timedelta
        ...: 
        ...: start_date = datetime(2022, 1, 1)
        ...: dates = [start_date + timedelta(days=x) for x in range(1000)]

    In [14]: find_closest_date(dates, datetime(2023, 1, 1))
    Out[14]: datetime.datetime(2023, 1, 1, 0, 0)

    In [15]: start_date = datetime(2022, 1, 1)
        ...: dates = [start_date + timedelta(days=7) for x in range(1000)]

    In [16]: find_closest_date(dates, datetime(2023, 1, 1))
    Out[16]: datetime.datetime(2022, 1, 8, 0, 0)

        
    """
    assert dates
    smallest = np.inf
    closest_date = None
    for x in sorted(dates):
        if delta := (x - date).total_seconds() < smallest:
            closest_date = x
            smallest = delta
        else:
            break
    assert closest_date
    return closest_date


def plot_data(food_agg_df, weight_agg_df, start_date, end_date, labels=None):

    fig = plt.figure(figsize=(12, 4))
    ax1 = fig.add_subplot(111)

    color = "tab:blue"
    weight_label = labels.get("weight_label", "Weight (lb)")
    food_label = labels.get("food_label", "Calories")
    ax1.set_ylabel(weight_label, color=color)
    narrowed_df1 = weight_agg_df[
        weight_agg_df["RawDate"] >= start_date.strftime("%Y-%m-%d")
    ]

    data1 = narrowed_df1.to_dict(orient="list")
    x1, y1 = data1["RawDate"], data1["Weight (lb)"]

    X = narrowed_df1["RawDate"].tolist()
    x_ticks, x_labels = make_xtick_labels(X, step=3)
    ax1.set_xticks(x_ticks)
    ax1.set_xticklabels(x_labels, rotation=-45)

    ax1.plot(x1, y1, color=color)

    # vertical labels
    if labels:
        if v_labels := labels.get("v_labels"):
            for (k, v) in v_labels.items():
                # Find closest value to k, in x_labels,
                closeset = find_closest_date(
                    [datetime.strptime(x, "%Y-%m-%d") for x in x_labels],
                    datetime.strptime(k, "%Y-%m-%d")
                )
                ax1.axvline(closeset.strftime("%Y-%m-%d"), label=v)

    # Flip,
    ax2 = ax1.twinx()

    data2 = food_agg_df[food_agg_df["RawDate"] >= start_date.strftime("%Y-%m-%d")].to_dict(
        orient="list"
    )
    color = "tab:red"
    x2, y2 = data2["RawDate"], data2["Calories"]
    ax2.plot(x2, y2, color=color)
    ax2.set_xlabel("Date")
    ax2.set_ylabel(food_label, color=color)
    out_loc = f"output-data/{utc_ts()}-figure.png"
    ax1.legend()
    ax1.grid(True)
    print("out_loc", out_loc)
    pylab.savefig(out_loc, bbox_inches="tight")


def bucket_n_days(df, days, aggregate_type):
    """ Aggregate days with mean or sum.
    """
    df["timestamp"] = pd.to_datetime(df["RawDate"])
    if aggregate_type == "mean":
        agg_df = df.groupby(pd.Grouper(key="timestamp", freq=f"{days}D")).mean().reset_index()
    elif aggregate_type == "sum":
        agg_df = df.groupby(pd.Grouper(key="timestamp", freq=f"{days}D")).sum().reset_index()

    agg_df["RawDate"] = agg_df["timestamp"].map(lambda x: x.strftime("%Y-%m-%d"))
    return agg_df

# Plot day by day data,
food_agg_df, weight_agg_df = get_data()
start_date = date(2022, 1, 1) # "2023-01-01"
end_date = date(2023, 3, 17)

plot_data(
    food_agg_df, weight_agg_df, start_date, end_date,
    labels={
        "vlabels": {"2023-01-01": "ADF starts"},
        "food_label": "Calories",
        "weight_label": "Weight (lb)",
    },
)



# Try 3 day average of weight, and 3 day total, for calories, 
# weight_agg_3day_df = bucket_n_days(weight_agg_df, 3)
# food_agg_3day_df  = bucket_n_days(food_agg_df, 3)
# plot_data(food_agg_3day_df, weight_agg_3day_df, start_date, end_date)

# Try 7 days
weight_agg_7day_df = bucket_n_days(weight_agg_df, 7, aggregate_type="mean")
food_agg_7day_df  = bucket_n_days(food_agg_df, 7, aggregate_type="mean")
plot_data(
    food_agg_7day_df,
     weight_agg_7day_df,
     start_date,
     end_date,
     labels={
         "v_labels": {"2023-01-01": "ADF starts"},
         "food_label": "Calories 7 day mean",
         "weight_label": "Weight (lb) 7 day mean",
     },
)


# Sum agg instead
food_agg_7day_df  = bucket_n_days(food_agg_df, 7, aggregate_type="sum")
plot_data(
    food_agg_7day_df,
     weight_agg_7day_df,
     start_date,
     end_date,
     labels={
         "v_labels": {"2023-01-01": "ADF starts"},
         "food_label": "Calories 7 day sum",
         "weight_label": "Weight (lb) 7 day mean",
     },
)
```
      
I am doing the version control on [github](https://github.com/namoopsoo/fasting-analyze/blob/main/2023-03-18-notebook.py), too.

