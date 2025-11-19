---
title: lazy execution pitfalls
date: 2025-11-17
draft: true
---

Spark lazy execution is great for many reasons, like, you can sanity check, run through a multi step feature engineering pipeline and just look at the first top 5 results, very quickly without running each step fully on your perhaps large dataset.

But the downside, is you can have corrupt parquet that you dont discover until an hour or more into a full run.

This happened to me recently and I wonder should I implement some early fail fast  data validation step . And is there precedent for it.

I had an issue where literally an hour into a  long multi-step pipeline,   I got an error about a missing parquet file and I look and see there are multiple series of parquet in the directory in question. 

I do a 
df = spark.read.parquet(adls_path)
df.count() 
And no crash , 
But I try , 
df.orderBy("the_primary_key").display() 
And that reproduces the crash.

I wonder hmm maybe that orderBy style smoke test might be good to run for all data at the beginning? 

Or is there a more "pysparkian" best practice ? Have people  written about this pain in general? Does everyone just solve it in a bespoke way? 
