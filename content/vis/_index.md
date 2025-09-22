---
title: "Sheet-Powered Chart"
---

Below is a chart driven by a Google Sheet published as CSV.

{{< sheetchart
  csv="https://docs.google.com/spreadsheets/d/1341IFRW4NeoOBWy3ybnRNcebbaZ2buoeIuB_30exCrE/export?format=csv&gid=0"
  labelsCol="DateEarned"
  valueCol="PointsEarned"
  title="Demo: 7-day Rolling Average"
  compute="rolling7"
>}}
