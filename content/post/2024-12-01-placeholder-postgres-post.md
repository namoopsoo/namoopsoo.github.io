---
title: other interesting topics on postgres and kubernetes
date: 2024-12-01
---


Have not covered yet, a few other cool topics. 

Can go into more detail later, but, for now some highlights.

At one point in a recent postgres pgvector retrieval project, a really cool epiphany was, w.r.t. indexing in pgvector both a concat blob of items and granular items, that it is not necessary to also embed the low level items because they can be embedded at runtime and it is not that time consuming.

Also the experience of working through building a kubernetes app, for handling the above, leveraging postgres as well as in memory embedding was super fun. And doing the batch embedding of a very large corpus of documents , within the same kubernetes app, was super fun as well.

And lots of interesting problems were encountered. One of these, was the challenge of building embeddings on postgresql , scaling up workers to do this, tweaking batch sizes, and doing it so as not to take a year say, but under a month instead. And at one point, my queries were very slow and I ended up rebuilding the index, and was close to reaching the cap on the postgresql disk pace, looking at the capacity getting filled up, as I was running the various vacuum and reindexing happening, but taking a very long time,after midnight and through 2 and 3 am, unsure precisely whether I would run out of disk space. I remember trying to devise predictions, while measuring whether my updates improved query time with various query analyses. So late into the night I remember watching HBO's beautoful animated Scavengers Reign, to try to stay awake while the slow low level database operations ran.

So yea this is just scratching the surface, but I should really fill in the fun details.

