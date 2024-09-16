---
title: string to int conversion nulling
date: 2024-09-13
---

I had this interesting situqtion, where I wanted to plot some numbers that were nested inside of struct columns. They were row counts in a delta table history output, but in any case, I tried to plot them, but my plot treated them as categories. 
Ok realizing they were strings, I cast them to integers, but then I got nulls. After a bit of trial and error I realized they were probably laerger than 32bit! 
Casting to big int, aka, `long`, did the trick.

```python
spark.createDataFrame(
  [["3731556164"], ["3731530835"], ["1731530835"]], ["numOutputRows"]
).withColumn(
  "numOutputRows_i", f.col("numOutputRows").cast("int")
).withColumn(
    "numOutputRows_l", f.col("numOutputRows").cast("long")
).show()
```


```
+-------------+---------------+---------------+
|numOutputRows|numOutputRows_i|numOutputRows_l|
+-------------+---------------+---------------+
|   3731556164|           null|     3731556164|
|   3731530835|           null|     3731530835|
|   1731530835|     1731530835|     1731530835|
+-------------+---------------+---------------+
```

posted my answer on [stacko](https://stackoverflow.com/questions/74400140/pyspark-converting=string-to-integer-results-in-null-values/78979934#78979934) too 