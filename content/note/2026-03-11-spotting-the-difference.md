---
date: 2026-03-11
title: spotting the difference
---

I had a crazy issue where a databricks job was taking over 13  hours and failing which had tzken just over 1 hour previously on another  workspace.

Turned out after a bit of staring at logs I had a face palming moment because yet again I got bit by spot instances/spot workers.

I found in my logs Spark UI these weird errors, "Executor 1 removed" 
"Executor 2 removed" ,..  thinking memory issues or asymmetric shuffle issues but then hovered my mouse and saw 

```
Executor 1 Removed at 2026/03/10 19:17:48
Reason: {"cause": "spot instance preemption","detectionMechanism": null}

```

i had tried many solutions. including skew detection, suspectijg skew issue. 

```python
(df.groupBy(spark_partition_id().alias("partition"))
.count()
.orderBy(col("count").desc())
.display())
```






