---
title: postgresql , pgvector and indexing
date: 2024-09-07
---

placeholder. didnt get chance to write this up yet, but I had used langchain pgvector, to add embeddings to postgresql , I ran my queries, and noticed they were slow.

I read about pgvector indexing, and on psql, noticed my embedding column was missing an index!

I tried adding the HNSW index manually. 

Weird error about no dimensions on the vector column. ok learned need explicit dimension. Added it. 
Nice adding index worked.

Realized that dimension was also missing on the python langchain pgvector side too! probably if I had it, the index would have been added under the hood automatically?


## 2024-11-10 story
There were many crazy micro challenges along the way, but one memorable epithany on 2024-11-10 was that I had a very slow query which was performing a scan on longitude,latitude in my table of restaurants when looking for restaurants within a particular distance of the user’s location. This was mind boggling because I had a postgis index which was not getting used. But I realized the reason was that in my WHERE I was constructing and casting to geopoint on the fly , 

```sql
WHERE ST_DWithin(ST_MakePoint(longitude, latitude)::geography, myblah.my_location, 1609.34)
```
, and simply changing to
```sql
 WHERE ST_DWithin(geopoint, myblah.my_location, 16093.4)
```
 
to use the actual geopoint column I already had but forgot to use finally got the query to do an index scan, cutting from seconds to under a second!