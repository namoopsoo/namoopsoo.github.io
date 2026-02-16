---
title: "Coldest"
date: 2026-02-15T13:07:28-05:00
draft: false

# optional thumbnail
images:
  - "https://s3.amazonaws.com/my-blog-content/2026-02-14-coldest/IMG_9715_preview.jpeg"
cover:
  image: "https://s3.amazonaws.com/my-blog-content/2026-02-14-coldest/IMG_9715_preview.jpeg"
---

Recently, myself and the rest of NYC went through a cold spell and news outlets reported<sup>[2](#references)</sup> the 13 day stretch of sub-zero weather, ending Feb 6th, was not longer than a 16 stretch in 1881. And this was shorter than a 1963 stretch, but tying a 2018-01-13 streak.

But this recent winter sure felt extreme. I know there is a recency bias, but I figured, why not also compare the area under the curve too. So I ranked the coldest 14-day stretches, using available data of the past decade. And then tried to visualize the spans of the coldest years too.

But even by that measure, it still looks like 2018 was colder.

## Sourcing
Doing this all with a ChatGPT agent, that obtained the data from a weather api I hadn't heard about before, open meteo<sup>[1](#references)</sup>, so I figured let's just plot all the data first as a sanity check.

{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-02-14-coldest/nyc_temperature_time_series_2016_2026.png" width="90%">}}

## What to compare
I wanted to compare the area under the curve, but I didn't want to mess around with negative numbers, so I figured it would be safer to use the highs and not the lows, since the Fahrenheit lows will have negatives, but in NY, spot checking, I didn't see any days where there were highs that were negative Fahrenheit. This is not yet the arctic luckily!

So here is how I phrased the metric for comparison in my prompt, for using the *feels like* data and just the standard temperature data too. 

```python
w14_feels_like_high_F(t) = feels_like_high_F(t - 14) + feels_like_high_F(t - 13) + ... + feels_like_high_F(t - 1) 
```

```python
w14_high_temp_F(t) = w14_high_temp_F(t - 14) + w14_high_temp_F(t - 13) + ... + w14_high_temp_F(t - 1)
```


## Ranked spans
I was kind of shocked to see that you have to show the coldest 20 spans of the *feels like* temps and top 18 of the actual temps, to even include `2026`!


```sh
┌────────────┬───────────────────────┬───────────────────────────┐
│ date       ┆ w14_feels_like_high_F ┆ w14_feels_like_high_F_avg │
│ ---        ┆ ---                   ┆ ---                       │
│ str        ┆ f64                   ┆ f64                       │
╞════════════╪═══════════════════════╪═══════════════════════════╡
│ 2018-01-09 ┆ 148.3                 ┆ 10.592857                 │
│ 2018-01-08 ┆ 159.3                 ┆ 11.378571                 │
│ 2018-01-10 ┆ 163.0                 ┆ 11.642857                 │
│ 2018-01-11 ┆ 178.1                 ┆ 12.721429                 │
│ 2018-01-07 ┆ 190.2                 ┆ 13.585714                 │
│ 2018-01-12 ┆ 220.5                 ┆ 15.75                     │
│ 2015-03-01 ┆ 242.6                 ┆ 17.328571                 │
│ 2018-01-06 ┆ 244.5                 ┆ 17.464286                 │
│ 2015-03-02 ┆ 250.6                 ┆ 17.9                      │
│ 2018-01-13 ┆ 261.7                 ┆ 18.692857                 │
│ 2015-03-03 ┆ 266.8                 ┆ 19.057143                 │
│ 2015-03-04 ┆ 277.0                 ┆ 19.785714                 │
│ 2018-01-05 ┆ 285.9                 ┆ 20.421429                 │
│ 2015-03-05 ┆ 290.6                 ┆ 20.757143                 │
│ 2018-01-14 ┆ 299.0                 ┆ 21.357143                 │
│ 2018-01-04 ┆ 304.0                 ┆ 21.714286                 │
│ 2018-01-15 ┆ 305.3                 ┆ 21.807143                 │
│ 2015-03-06 ┆ 312.6                 ┆ 22.328571                 │
│ 2018-01-16 ┆ 316.3                 ┆ 22.592857                 │
│ 2025-01-28 ┆ 318.3                 ┆ 22.735714                 │
└────────────┴───────────────────────┴───────────────────────────┘
```

```sh
┌────────────┬─────────────────┬─────────────────────┐
│ date       ┆ w14_high_temp_F ┆ w14_high_temp_F_avg │
│ ---        ┆ ---             ┆ ---                 │
│ str        ┆ f64             ┆ f64                 │
╞════════════╪═════════════════╪═════════════════════╡
│ 2018-01-09 ┆ 308.5           ┆ 22.035714           │
│ 2018-01-08 ┆ 317.7           ┆ 22.692857           │
│ 2018-01-10 ┆ 319.3           ┆ 22.807143           │
│ 2018-01-11 ┆ 330.8           ┆ 23.628571           │
│ 2018-01-07 ┆ 344.8           ┆ 24.628571           │
│ 2015-03-01 ┆ 358.5           ┆ 25.607143           │
│ 2018-01-12 ┆ 364.0           ┆ 26.0                │
│ 2015-03-02 ┆ 365.7           ┆ 26.121429           │
│ 2015-03-03 ┆ 383.2           ┆ 27.371429           │
│ 2018-01-06 ┆ 391.5           ┆ 27.964286           │
│ 2015-03-04 ┆ 395.0           ┆ 28.214286           │
│ 2018-01-13 ┆ 397.9           ┆ 28.421429           │
│ 2015-03-05 ┆ 408.0           ┆ 29.142857           │
│ 2018-01-05 ┆ 422.9           ┆ 30.207143           │
│ 2015-03-06 ┆ 424.8           ┆ 30.342857           │
│ 2018-01-14 ┆ 429.3           ┆ 30.664286           │
│ 2015-03-07 ┆ 430.1           ┆ 30.721429           │
│ 2025-01-28 ┆ 433.9           ┆ 30.992857           │
│ 2015-03-08 ┆ 435.1           ┆ 31.078571           │
│ 2018-01-15 ┆ 436.5           ┆ 31.178571           │
└────────────┴─────────────────┴─────────────────────┘
```



# References
1. https://open-meteo.com/en/docs/historical-weather-api
2. https://www.bbc.com/news/articles/cd9g8nxdexko


<sup>[xxx](#references)</sup>

