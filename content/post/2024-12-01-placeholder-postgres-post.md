---
title: other interesting topics on postgres and kubernetes
date: 2024-12-01
---


Have not covered yet, a few other cool topics. 

Can go into more detail later, but, for now some highlights.

### Runtime embeddings to save money
At one point in a recent postgres pgvector retrieval project, a really cool epiphany was, w.r.t. indexing in pgvector both a concatenated blob of items and granular items, that it is not necessary to also embed the low level items because they can be embedded at runtime and it is not that time consuming. The dataset is a corpus dishes grouped by menus. The initial design was to allow a two step embedding search, first across the concatenated menu embeddings to narrow down, and then on the menu level, to search the dish item level embeddings a second time. But disk space wise, it became clear that the dish items and their embedding hnsw index would take up an enormous amount. There are typically 10 dishes per menu so a proportionally `~10x` larger space was needed. But the duhh moment was that maybe we don't even need to store the dish item level index at all because maybe we can embed the dishes on the fly when we already have done a first pass, ending up with maybe 5 to 10 menus. Now we would only need to embed maybe 50 to 100 dishes and that would not be too slow. And indeed embedding and searching through 50 to 100 dishes did take time but it appeared to be worth the precious postgresql disk space saved. Of course depending on future query latency requirements it is always possible to reconsider this.

### Kubernetes batch embedding jobs
Also the experience of working through building a kubernetes app, for handling the above, leveraging postgres as well as in memory embedding was super fun. And doing the batch embedding of a very large corpus of documents , within the same kubernetes app, was super fun as well.

Initially, I was using my laptop to create the embeddings, because I was just constraining the problem to a subset of the full dataset. Therefore at that point it was more expedient to do the embedding quick and dirty and spend the time on massaging and proving out the postgresql table structures and indexes. But when at one point, the postgresql structure was set, the next most important task was to see how the postgresql queries would perform at full scale and not just the mere `<1%` of the data. And so the next step was to update the main Docker image that I was using initially for a proof of concept search app, to also run batch embedding. A fun detail here was that as an idea of building out the batch embedding code, the prefix of the uuid of the primary id of the data was used as a partition key. So it was possible to say, test small changes to the code on a prefix like `000` or `1efa`, which would contain only `1/4096th` and `1/65536th` of the data, respectively. And then when confident the code was running correctly, I would crank things up to `1/256th`, and therefore it was easy to track what percent of the work was finished and still remaining.

### postgresql storage caps and google cloud quotas
And lots of interesting problems were encountered. One of these, was the challenge of building embeddings on postgresql , scaling up workers to do this, tweaking batch sizes, and doing it so as not to take a year say, but under a month instead. And at one point, my queries were very slow and I ended up rebuilding the index, and was close to reaching the cap on the postgresql disk pace, looking at the capacity getting filled up, as I was running the various vacuum and reindexing happening, but taking a very long time,after midnight and through 2 and 3 am, unsure precisely whether I would run out of disk space. I remember trying to devise predictions, while measuring whether my updates improved query time with various query analyses. So late into the night I remember watching HBO's beautiful animated Scavengers Reign, to try to stay awake while the slow low level database operations ran.

Along the way I also reached a few Google cloud quotas put in place that each needed to be adjusted, such as the number of simultaneous kubernetes jobs.

So yea this is just scratching the surface, but I should really fill in the fun details.

### The denormalize postgis geopoint and pgvector tables for speed up idea
Per an interesting idea from a friend, at one point I combined the pgvector and geopoint tables on the idea that at the time, hnsw indexing was not supported when using materialized CTE in postgresql. So the earlier query first used a materialized CTE to isolate geopoint locations by mile radius and then apply a vector search on the subset. However, it was looking like no matter what tweaks I was using, the hnsw index just did not pop up in the postgresql query plan. However, the geopoint subset was quite small and the non-hnsw index that would kick in after was still doing decently. And in particular, another idea was that hey, why not do back to back staggered queries like progressive jpeg loading back in the 1990s? 5 mile initially, then you see results immediately and query further for more.

Another interesting idea I had is hey we don't necessarily need a radius result , we can just fetch the result that appears in the bounding box . And as I was looking through the various postgis queries and found something like this is possible.

The initial radius query I had been using for a while was something like 

```sql
SELECT *
FROM blah_table
WHERE ST_DWithin(geom, ST_MakePoint(longitude, latitude), radius, true);
```

and I didn't fully get the bounding box query running but in general it was something like this, 

```sql
SELECT ST_Extent(geom) AS bounding_box
FROM blah_table;
```

The denormalization idea, meant, no more join and then theoretically, hnsw index can kick in? I should look back at my notes but I think I recall hnsw index still did not kick in because the materialized CTE for thte postgis was still needed. 

But the denormalization theoretically, was also to potentially speed things up since a join is not as instantaneous as just reading straight from a single table.  However, I recall what happened was that denormalized, meant that the materialized geopoint CTE actually needed to sift through more data and so that part may have counteracted the speed benefit of the denormalization. So ultimately a balancing act. I should fill in more details with my notes. But super fun problems !


