---
title: odd pyspark window function behavior
date: 2023-09-23
---



Working through this odd window function behavior, 

```python
from pyspark.sql.window import Window
import pyspark.sql.functions as F

toy_df = spark.createDataFrame(
    [{'feature': 'feat1', 'category': 'cat1', 'Drift score': 0.0, 'group': 'blah', 'baseline_date': '20191231', 'compare_date': '20230131'}, {'feature': 'feat1', 'category': 'cat1', 'Drift score': 0.0, 'group': 'blah', 'baseline_date': '20220131', 'compare_date': '20230131'}, {'feature': 'feat1', 'category': 'cat1', 'Drift score': 0.0, 'group': 'blah', 'baseline_date': '20220731', 'compare_date': '20230131'}, {'feature': 'feat2', 'category': 'cat1', 'Drift score': 0.16076398135644604, 'group': 'blah', 'baseline_date': '20191231', 'compare_date': '20230131'}, {'feature': 'feat2', 'category': 'cat1', 'Drift score': 0.07818495131083669, 'group': 'blah', 'baseline_date': '20220131', 'compare_date': '20230131'}, {'feature': 'feat2', 'category': 'cat1', 'Drift score': 0.07164427544566881, 'group': 'blah', 'baseline_date': '20220731', 'compare_date': '20230131'}, {'feature': 'feat3', 'category': 'cat1', 'Drift score': 0.2018208744775895, 'group': 'blah', 'baseline_date': '20191231', 'compare_date': '20230131'}, {'feature': 'feat3', 'category': 'cat1', 'Drift score': 0.06897468871439233, 'group': 'blah', 'baseline_date': '20220131', 'compare_date': '20230131'}, {'feature': 'feat3', 'category': 'cat1', 'Drift score': 0.07111383432227428, 'group': 'blah', 'baseline_date': '20220731', 'compare_date': '20230131'}, {'feature': 'feat5', 'category': 'cat1', 'Drift score': 0.20151850543660316, 'group': 'blah', 'baseline_date': '20191231', 'compare_date': '20230131'}, {'feature': 'feat5', 'category': 'cat1', 'Drift score': 0.05584133483840621, 'group': 'blah', 'baseline_date': '20220131', 'compare_date': '20230131'}, {'feature': 'feat5', 'category': 'cat1', 'Drift score': 0.056223672793567, 'group': 'blah', 'baseline_date': '20220731', 'compare_date': '20230131'}, {'feature': 'feat6', 'category': 'cat1', 'Drift score': 0.10648175064912868, 'group': 'blah', 'baseline_date': '20191231', 'compare_date': '20230131'}, {'feature': 'feat6', 'category': 'cat1', 'Drift score': 0.03398787644288803, 'group': 'blah', 'baseline_date': '20220131', 'compare_date': '20230131'}, {'feature': 'feat6', 'category': 'cat1', 'Drift score': 0.027693531284292805, 'group': 'blah', 'baseline_date': '20220731', 'compare_date': '20230131'}, {'feature': 'feat7', 'category': 'cat1', 'Drift score': 0.12696742943404185, 'group': 'blah', 'baseline_date': '20191231', 'compare_date': '20230131'}, {'feature': 'feat7', 'category': 'cat1', 'Drift score': 0.07147622765870758, 'group': 'blah', 'baseline_date': '20220131', 'compare_date': '20230131'}, {'feature': 'feat7', 'category': 'cat1', 'Drift score': 0.07478091185430771, 'group': 'blah', 'baseline_date': '20220731', 'compare_date': '20230131'}, {'feature': 'feat8', 'category': 'cat2', 'Drift score': 0.11779958630386245, 'group': 'blah', 'baseline_date': '20191231', 'compare_date': '20230131'}, {'feature': 'feat8', 'category': 'cat2', 'Drift score': 0.04240444683921199, 'group': 'blah', 'baseline_date': '20220131', 'compare_date': '20230131'}]
)
toy_df.show()

+--------------------+-------------+--------+------------+-------+-----+
|         Drift score|baseline_date|category|compare_date|feature|group|
+--------------------+-------------+--------+------------+-------+-----+
|                 0.0|     20191231|    cat1|    20230131|  feat1| blah|
|                 0.0|     20220131|    cat1|    20230131|  feat1| blah|
|                 0.0|     20220731|    cat1|    20230131|  feat1| blah|
| 0.16076398135644604|     20191231|    cat1|    20230131|  feat2| blah|
| 0.07818495131083669|     20220131|    cat1|    20230131|  feat2| blah|
| 0.07164427544566881|     20220731|    cat1|    20230131|  feat2| blah|
|  0.2018208744775895|     20191231|    cat1|    20230131|  feat3| blah|
| 0.06897468871439233|     20220131|    cat1|    20230131|  feat3| blah|
| 0.07111383432227428|     20220731|    cat1|    20230131|  feat3| blah|
| 0.20151850543660316|     20191231|    cat1|    20230131|  feat5| blah|
| 0.05584133483840621|     20220131|    cat1|    20230131|  feat5| blah|
|   0.056223672793567|     20220731|    cat1|    20230131|  feat5| blah|
| 0.10648175064912868|     20191231|    cat1|    20230131|  feat6| blah|
| 0.03398787644288803|     20220131|    cat1|    20230131|  feat6| blah|
|0.027693531284292805|     20220731|    cat1|    20230131|  feat6| blah|
| 0.12696742943404185|     20191231|    cat1|    20230131|  feat7| blah|
| 0.07147622765870758|     20220131|    cat1|    20230131|  feat7| blah|
| 0.07478091185430771|     20220731|    cat1|    20230131|  feat7| blah|
| 0.11779958630386245|     20191231|    cat2|    20230131|  feat8| blah|
| 0.04240444683921199|     20220131|    cat2|    20230131|  feat8| blah|
+--------------------+-------------+--------+------------+-------+-----+
```

## Applying the window function here, 

```python
w = Window.partitionBy("group", "feature", "compare_date", ).orderBy(F.col("Drift score").desc())
(
    toy_df
    .withColumn("mean_score", F.round(F.mean("Drift score").over(w), 4))
    .withColumn("max_score", F.round(F.max("Drift score").over(w), 4))
    .withColumn("min_score", F.round(F.min("Drift score").over(w), 4))
    .withColumn("baseline_date_max_score", F.first("baseline_date").over(w))
    .withColumn("row_num", F.row_number().over(w))
    .where(F.col("row_num") == 1)
    .drop("row_num")
    .select("category", "feature", "compare_date", "mean_score", "max_score", "min_score", "baseline_date_max_score")
    .show()
)

+--------+-------+------------+----------+---------+---------+-----------------------+
|category|feature|compare_date|mean_score|max_score|min_score|baseline_date_max_score|
+--------+-------+------------+----------+---------+---------+-----------------------+
|    cat1|  feat1|    20230131|       0.0|      0.0|      0.0|               20191231|
|    cat1|  feat2|    20230131|    0.1608|   0.1608|   0.1608|               20191231|
|    cat1|  feat3|    20230131|    0.2018|   0.2018|   0.2018|               20191231|
|    cat1|  feat5|    20230131|    0.2015|   0.2015|   0.2015|               20191231|
|    cat1|  feat6|    20230131|    0.1065|   0.1065|   0.1065|               20191231|
|    cat1|  feat7|    20230131|     0.127|    0.127|    0.127|               20191231|
|    cat2|  feat8|    20230131|    0.1178|   0.1178|   0.1178|               20191231|
+--------+-------+------------+----------+---------+---------+-----------------------+
```

I was confused why are the min, max and mean all the same. I thought, could it be my data is corrupted and some of my partitions only have one row?

I took out the filter by "row_num", to try debugging,

```python
w = Window.partitionBy("group", "feature", "compare_date", ).orderBy(F.col("Drift score").desc())
(
    toy_df
    .withColumn("mean_score", F.round(F.mean("Drift score").over(w), 4))
    .withColumn("max_score", F.round(F.max("Drift score").over(w), 4))
    .withColumn("min_score", F.round(F.min("Drift score").over(w), 4))
    .withColumn("baseline_date_max_score", F.first("baseline_date").over(w))
    .withColumn("row_num", F.row_number().over(w))

    .select("category", "feature", "compare_date", "Drift score" , "mean_score", "max_score", "min_score",  )
    .show()
)

+--------+-------+------------+--------------------+----------+---------+---------+
|category|feature|compare_date|         Drift score|mean_score|max_score|min_score|
+--------+-------+------------+--------------------+----------+---------+---------+
|    cat1|  feat1|    20230131|                 0.0|       0.0|      0.0|      0.0|
|    cat1|  feat1|    20230131|                 0.0|       0.0|      0.0|      0.0|
|    cat1|  feat1|    20230131|                 0.0|       0.0|      0.0|      0.0|
|    cat1|  feat2|    20230131| 0.16076398135644604|    0.1608|   0.1608|   0.1608|
|    cat1|  feat2|    20230131| 0.07818495131083669|    0.1195|   0.1608|   0.0782|
|    cat1|  feat2|    20230131| 0.07164427544566881|    0.1035|   0.1608|   0.0716|
|    cat1|  feat3|    20230131|  0.2018208744775895|    0.2018|   0.2018|   0.2018|
|    cat1|  feat3|    20230131| 0.07111383432227428|    0.1365|   0.2018|   0.0711|
|    cat1|  feat3|    20230131| 0.06897468871439233|     0.114|   0.2018|    0.069|
|    cat1|  feat5|    20230131| 0.20151850543660316|    0.2015|   0.2015|   0.2015|
|    cat1|  feat5|    20230131|   0.056223672793567|    0.1289|   0.2015|   0.0562|
|    cat1|  feat5|    20230131| 0.05584133483840621|    0.1045|   0.2015|   0.0558|
|    cat1|  feat6|    20230131| 0.10648175064912868|    0.1065|   0.1065|   0.1065|
|    cat1|  feat6|    20230131| 0.03398787644288803|    0.0702|   0.1065|    0.034|
|    cat1|  feat6|    20230131|0.027693531284292805|    0.0561|   0.1065|   0.0277|
|    cat1|  feat7|    20230131| 0.12696742943404185|     0.127|    0.127|    0.127|
|    cat1|  feat7|    20230131| 0.07478091185430771|    0.1009|    0.127|   0.0748|
|    cat1|  feat7|    20230131| 0.07147622765870758|    0.0911|    0.127|   0.0715|
|    cat2|  feat8|    20230131| 0.11779958630386245|    0.1178|   0.1178|   0.1178|
|    cat2|  feat8|    20230131| 0.04240444683921199|    0.0801|   0.1178|   0.0424|
+--------+-------+------------+--------------------+----------+---------+---------+
```

### Now this looked even more weird, since somehow the min, max and mean were different for different rows in the partitions. 

I forget where, I read somewhere that the use of the `orderBy`, which I needed for one of the columns, was creating a weird situation for the min max mean columns, so I took that out. 

## Ended  up with 

```python
w = Window.partitionBy("group", "feature", "compare_date", )
(
    toy_df
    .withColumn("mean_score", F.round(F.mean("Drift score").over(w), 4))
    .withColumn("max_score", F.round(F.max("Drift score").over(w), 4))
    .withColumn("min_score", F.round(F.min("Drift score").over(w), 4))
    .withColumn("baseline_date_max_score", F.first("baseline_date").over(w.orderBy(F.col("Drift score").desc())))
    .withColumn("row_num", F.row_number().over(w.orderBy("Drift score")))
    .select("category", "feature", "compare_date", "Drift score" , "mean_score", "max_score", "min_score", "baseline_date_max_score" )

    .show()
)

+--------+-------+------------+--------------------+----------+---------+---------+-----------------------+
|category|feature|compare_date|         Drift score|mean_score|max_score|min_score|baseline_date_max_score|
+--------+-------+------------+--------------------+----------+---------+---------+-----------------------+
|    cat1|  feat1|    20230131|                 0.0|       0.0|      0.0|      0.0|               20191231|
|    cat1|  feat1|    20230131|                 0.0|       0.0|      0.0|      0.0|               20191231|
|    cat1|  feat1|    20230131|                 0.0|       0.0|      0.0|      0.0|               20191231|
|    cat1|  feat2|    20230131| 0.16076398135644604|    0.1035|   0.1608|   0.0716|               20191231|
|    cat1|  feat2|    20230131| 0.07818495131083669|    0.1035|   0.1608|   0.0716|               20191231|
|    cat1|  feat2|    20230131| 0.07164427544566881|    0.1035|   0.1608|   0.0716|               20191231|
|    cat1|  feat3|    20230131|  0.2018208744775895|     0.114|   0.2018|    0.069|               20191231|
|    cat1|  feat3|    20230131| 0.07111383432227428|     0.114|   0.2018|    0.069|               20191231|
|    cat1|  feat3|    20230131| 0.06897468871439233|     0.114|   0.2018|    0.069|               20191231|
|    cat1|  feat5|    20230131| 0.20151850543660316|    0.1045|   0.2015|   0.0558|               20191231|
|    cat1|  feat5|    20230131|   0.056223672793567|    0.1045|   0.2015|   0.0558|               20191231|
|    cat1|  feat5|    20230131| 0.05584133483840621|    0.1045|   0.2015|   0.0558|               20191231|
|    cat1|  feat6|    20230131| 0.10648175064912868|    0.0561|   0.1065|   0.0277|               20191231|
|    cat1|  feat6|    20230131| 0.03398787644288803|    0.0561|   0.1065|   0.0277|               20191231|
|    cat1|  feat6|    20230131|0.027693531284292805|    0.0561|   0.1065|   0.0277|               20191231|
|    cat1|  feat7|    20230131| 0.12696742943404185|    0.0911|    0.127|   0.0715|               20191231|
|    cat1|  feat7|    20230131| 0.07478091185430771|    0.0911|    0.127|   0.0715|               20191231|
|    cat1|  feat7|    20230131| 0.07147622765870758|    0.0911|    0.127|   0.0715|               20191231|
|    cat2|  feat8|    20230131| 0.11779958630386245|    0.0801|   0.1178|   0.0424|               20191231|
|    cat2|  feat8|    20230131| 0.04240444683921199|    0.0801|   0.1178|   0.0424|               20191231|
+--------+-------+------------+--------------------+----------+---------+---------+-----------------------+
```

## Finally 
Can now filter out the non aggregate rows 

```python
w = Window.partitionBy("group", "feature", "compare_date", )
(
    toy_df
    .withColumn("mean_score", F.round(F.mean("Drift score").over(w), 4))
    .withColumn("max_score", F.round(F.max("Drift score").over(w), 4))
    .withColumn("min_score", F.round(F.min("Drift score").over(w), 4))
    .withColumn("baseline_date_max_score", F.first("baseline_date").over(w.orderBy(F.col("Drift score").desc())))
    .withColumn("row_num", F.row_number().over(w.orderBy("Drift score")))
    .where(F.col("row_num") == 1)
    .drop("row_num")
    .select("category", "feature", "compare_date", "mean_score", "max_score", "min_score", "baseline_date_max_score" )

    .show()
)

+--------+-------+------------+----------+---------+---------+-----------------------+
|category|feature|compare_date|mean_score|max_score|min_score|baseline_date_max_score|
+--------+-------+------------+----------+---------+---------+-----------------------+
|    cat1|  feat1|    20230131|       0.0|      0.0|      0.0|               20191231|
|    cat1|  feat2|    20230131|    0.1035|   0.1608|   0.0716|               20191231|
|    cat1|  feat3|    20230131|     0.114|   0.2018|    0.069|               20191231|
|    cat1|  feat5|    20230131|    0.1045|   0.2015|   0.0558|               20191231|
|    cat1|  feat6|    20230131|    0.0561|   0.1065|   0.0277|               20191231|
|    cat1|  feat7|    20230131|    0.0911|    0.127|   0.0715|               20191231|
|    cat2|  feat8|    20230131|    0.0801|   0.1178|   0.0424|               20191231|
+--------+-------+------------+----------+---------+---------+-----------------------+
```

What explains this odd behavior?



## Face palm !
I did not notice this at the time, but a colleague pointed out 🤦‍♂️ that although min, max, mean don't require orderBy, but when providing it, they will offer cumulative quantities. Indeed spot checking this he was right ! Nice 😀

