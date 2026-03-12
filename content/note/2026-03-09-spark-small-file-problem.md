---
title: Spark small file problem
date: 2026-03-09
---

Making a mental note, today I encountered what is referred to as the spark small file problem [1]. Well, though I did not realize it initially anyway. 

I was running a pretty complicated feature engineering notebook, trying to reproduce the results of a colleague. I set up a databricks workflow DAG on a recent evening, looking forward to seeing what happened a following morning. The result surprised me. I woke up to a job that ran for 13 hours and crashed with a shuffle flavored error.

```python
Py4JJavaError: An error occurred while calling o1714.parquet.
org.apache.spark.SparkException: Job aborted due to stage failure: ShuffleMapStage 304 .... has failed the maximum allowale numer of times: 4. Most recent failure reason: 
org.apache.spark.shuffle.MetadataFetchFailedException: Missing an output location for shuffle 78 partition 0

```

Trying to dig in further, since the error was indicative of skew, I ran

```python
from pyspark.sql.functions import spark_partition_id, count, col

(df.groupBy(spark_partition_id().alias("partition"))
  .count()
  .orderBy(col("count").desc())
  .display()
)
```
in order to observe, the `df` that was close to the write to parquet, whether there was indeed a skew. The partitions appeared to be of like sizes. 

Our of curiosity, I just decided to look at some of the various source datasets that were being read in, filtered and joined in various ways, to see whether perhaps there were multiple parquet series writes into the folder in question. I had in the past experienced some very weird behavior in a  case like this, where multiple parquet series were copied to one folder and reading this produced some very weird duplicate errors. 

In any case, I saw there was only one series, though I saw this one series had 2850 parquet files. That looked quite odd, because I am more used to seeing sizes under 500.  They were all around ~19MB or so. I looked around and indeed [1] this was a small file problem. A sort of a death by a thousand paper cuts.

Apparently this can create additional overhead that affects performance. Actually I encountered this issue in AWS land with hive and Athena a long while back, w.r.t. what happens if you try to partition your data too deeply. I was interested in taking full advantage of Athena partitioning, along year, month, and I was applying some categories to kinds of real time traffic being logged. But I was reading that it is not a good idea to partition too deeply and so I backed off on that. 

In any case bacck to parquet, so I decided to read the parquet folder plainly, 

```python
blah_df = spark.read.parquet("path/to/folder").limit(100).display()
```
but amazingly even just this took `6 minutes` to run! 

As a quick experiment, I coalesced this into 1/10th of the partitions, 

```python
blah_df.coalesce(285).write("path/to/fewer")
reread_df = spark.read.parquet("path/to/fewer")
reread_df.limit(100).display()
```
and indeed lo and behold, this took just `5 seconds`! 

I was rerunning the full pipeline with more memory as well and that completed in just over an hour,  in the meantime, but now that I saw this other good result, I am also rerunning the pipeline with the original memory footprint, to see what happens.

# Well there was more to the story!
After doing the rerun, I went from 13 hours to 11 hours, but still the same `org.apache.spark.shuffle.MetadataFetchFailedException` crash. 

```
org.apache.spark.shuffle.MetadataFetchFailedException: Missing an output location for shuffle 78 partition 0

```

I did some more research, learning this literally is saying , during a shuffle attempt, that is, moving data from one executor to another , needed for joins or groupbys or any operation where rows for some column values are scattered across executors and need to find their way to an executor that is grouping by a specific column value say. In my case, the transformqtion has a pivot towards the end , where column values become new columns and so this would require a complete redistribution of data towzrds the end. 

But still, why the error? Looking at Spark UI, there were lots of these failures actually and there were lots of dead executors and lots of new ones spun up. And the shuffle writes were in the several tens of Gigabytes. 

An idea from a copilot GPT  was that timeouts led to executor deaths and so I should try a spark config that says to persist shuffle data beyond executor death and one to increase timeouts. Reasoning was that, if a executor did a lot of work but took too long , lets increase the default timeout and keep shuffle data so the work doesnt need to be redone.

I tried this but it didnt work. So I looked at the Spark UI again. I dont know I was just trying to see does Spark UI show me the actual reason for the executor deaths? I hovered over them and wow major facepalm moment !🤦‍♂️🤦‍♂️🤦‍♂️ The reason was spot preemption! I looked at my cluster and indeed somehow my cluster was accidentally set to allow "spot instances". I don't even remember doing this  . I have been bitten by spot instances in the past too actually, also not knowing why the option was ticked. 

In any case wow, after getting rid of the spot instance option in my autoscaling setting, I tried again and of course no more preemptions and no more executor deaths and no more task failures!!

I know that in the past I have seen task failures related to low memory, just everything failing with OOM, but in this case, I specifically wanted to see this job run through a Standard_d16as_v5 as opposed to the heavier Standard_d32as_v5 that my colleague was using because I dont want to lean on just throwing more compute on a problem to solve it.

So actually initially I was able to indeed reproduce this with the Standard_d32as_v5 with about 1 hour, however that cluster, as I checked after the fact 🤦‍♂️, indeed did not have spot instances ticked ! 

And ultimately the Standard_d16as_v5 error free run without spot instance preemption, took 5 hours and change. 

So yea, as usual most problems are not what they seem surface level and have many layers! Im glad the answer was not messing around with the spark config afterall because that sounds tedious.

I hope to also at some point think whether pivots can be replaced with equivalent more graceful operations, and whether they are as shuffle heavy as I assume. 



# References
1. https://docs.azure.cn/en-us/databricks/optimizations/spark-ui-guide/slow-spark-stage-low-io#reading-a-lot-of-small-files
