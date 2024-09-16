---
title: How to query pgvector data leveraging multiple indexes
date: 2024-09-14
---

First, an embedding  table was created, using langchain pgvector. (TODO show that example).


### Initial query which was working,

using, a `chosen_embedding`, of some uuid I randomly picked from the vector table, using the cosine similarity `<=>` as an `ORDER BY`,


```sql
explain analyze with myblah(chosen_embedding, chosen_id) as (
    values (
      (SELECT embedding FROM langchain_pg_embedding 
       WHERE id = '280aefd0-cb15-4a54-924d-aab37ee8a816'
      ), '280aefd0-cb15-4a54-924d-aab37ee8a816')
)
SELECT 
substr(id, 0, 8) as id, 
substr(document, 0, 40) as doc, 
round(
  1 - cast(embedding <=> chosen_embedding as numeric), 3
) as score,
cmetadata->'name' as name
FROM langchain_pg_embedding, myblah
WHERE id != chosen_id
ORDER BY embedding <=> chosen_embedding
LIMIT 100;

```

with, output, we see below, the `ix_embedding_hnsw` index created last time does have an index scan.

```
                                                                                      QUERY PLAN                                                                                       
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Limit  (cost=173.46..219.18 rows=100 width=136) (actual time=3.608..4.641 rows=39 loops=1)
   InitPlan 1 (returns $0)
     ->  Index Scan using ix_langchain_pg_embedding_id on langchain_pg_embedding langchain_pg_embedding_1  (cost=0.41..8.43 rows=1 width=32) (actual time=0.035..0.038 rows=1 loops=1)
           Index Cond: ((id)::text = 'a80aefd0-cba5-4a54-924c-aab37ee8a816'::text)
   InitPlan 2 (returns $1)
     ->  Index Scan using ix_langchain_pg_embedding_id on langchain_pg_embedding langchain_pg_embedding_2  (cost=0.41..8.43 rows=1 width=32) (actual time=0.097..0.099 rows=1 loops=1)
           Index Cond: ((id)::text = 'a80aefd0-cba5-4a54-924c-aab37ee8a816'::text)
   ->  Index Scan using ix_embedding_hnsw on langchain_pg_embedding  (cost=156.60..7722.42 rows=16548 width=136) (actual time=3.606..4.629 rows=39 loops=1)
         Order By: (embedding <=> $1)
         Filter: ((id)::text <> 'a80aefd0-cba5-4a54-924c-aab37ee8a816'::text)
         Rows Removed by Filter: 1
 Planning Time: 3.370 ms
 Execution Time: 8.088 ms
(13 rows)
```

## but next, querying , with a second table, that has postgis data, then the hnsw index is not used
TODO
