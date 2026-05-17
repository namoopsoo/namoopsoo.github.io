---
title: "Gpx Bike Tour Overlay"
# slug: "2026-05-10--gpx-bike-tour-overlay"
date: 2026-05-10T12:04:02-04:00
# draft: true

# optional thumbnail
images:
  - "https://s3.amazonaws.com/my-blog-content/2026-05-10--gpx-bike-tour-overlay/IMG_1027.jpg"
cover:
  image: "https://s3.amazonaws.com/my-blog-content/2026-05-10--gpx-bike-tour-overlay/IMG_1027.jpg"
---

I had a bike commute where I happened to join the 2026 May 3rd 5 borough bike tour<sup>[1](#references)</sup>. I was curious how much overlap I had. 

The below is an overlay output from a vibe coded ChatGPT session, extracting the overlay data using gpx from my strava data and gpx from the bike tour that looks like is here<sup>[2](#references)</sup>. So in my mind it felt like 5 miles. And looks like it was about 5.92 miles.



# Build the overlap


```python
from pathlib import Path
from create_bike_overlap_map import read_gpx_points, plot_overlay
```


```python
strava_gpx = "data/Evening_E_Bike_Ride.gpx"
tour_gpx = "data/Five_Boro_Bike_Tour.gpx"
strava_pts = read_gpx_points(strava_gpx)
tour_pts = read_gpx_points(tour_gpx)
```


```python
strava_pts[:2], strava_pts[-2:], tour_pts[:2], tour_pts[-2:]
```




    ([(-73.979077, 40.689653), (-73.979077, 40.689653)],
     [(-73.937761, 40.767267), (-73.937752, 40.767274)],
     [(-74.01496, 40.70474), (-74.01426, 40.70628)],
     [(-74.075024, 40.642269), (-74.075015, 40.642433)])




```python
tolerance_m = 20
png_out_file = Path("bike_tour_overlap_map.png")
geojson_out = Path("bike_tour_overlap_segments.geojson")

plot_overlay(
    strava_pts,
    tour_pts,
    tolerance_m,
    png_out_file,
    geojson_out,
)
```

    Wrote bike_tour_overlap_map.png
    Wrote bike_tour_overlap_segments.geojson
    Matched miles: 5.92



{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-05-10--gpx-bike-tour-overlay/overlay-strava-5boro-bike-tour.png" width="50%">}}
    


# Building this blogpost
This blogpost was built, by running the ipynb notebook here<sup>[4](#references)</sup> and converting the ipynb to markdown

# References
1. https://www.bike.nyc/wp-content/uploads/2025/04/2025-Tour-Map.png
2. gpx data here, https://ridewithgps.com/routes/46474401
3. did not find gpx data here though, https://www.nycbikemaps.com/maps/five-boro-bike-tour-map/interactive-5-boro-bike-tour-map/
4. https://github.com/namoopsoo/gpx-stuff
5. https://support.ridewithgps.com/hc/en-us/articles/13004717775515-Send-to-Device-on-Mobile#export-to-share:~:text=their%20Files%20app.-,Export%20to%20Share,-Once%20you%27ve%20exported
