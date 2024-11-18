---
date: 2024-11-09
title: embedding and pgvector query speedup
---


Wow, I found a very silly issue that was holding back this query.

The data is a langchain embedding table of items associated with places, as well as a second table with those place addresses along with their longitude, latitude.


Also, as I had a slower query, executed through sqlalchemy, like 

```python
from sqlalchemy.sql import text

with foo.engine.connect() as conn:
    data = {"vector": [0.06014461815357208, 0.07383278757333755, 0.010295705869793892, -0.058833882212638855,], "longitude": "", "latitude": ""}
    sql = """
    """
    statement = text(sql)
    # TODO also parameterize the `limit 10` ? fetchmany()
    results = conn.execute(statement, data).mappings().fetchall()
```
I'm glad about three strategies I used to help speed up the debugging. Namely, (1) deconstructing the sqlalchemy code, into a raw SQL query I could play with, (2) using DBeaver to quickly throw my raw SQL query against postgresql, for super fast iteration, and (3) of course using `explain analyze` to look at query plans to understand where the bottle neck may be.


One of the cool ways to get a raw compiled sql query from the sqlalchemy sql-injection-parameterized-safe style, is to use, the following,

```python
from sqlalchemy.dialects import postgresql

data = ...
# Manually bind parameters to the statement
compiled_statement = statement.bindparams(**data).compile(
    dialect=postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
)

# Print the full SQL query
print(compiled_statement)
```

here, I was able to get the full raw query, with the caveat that somehow this did not work for the `::vector` type. For the vector type, I was getting the error, 


```
CompileError: No literal value renderer is available for literal value "[0.06014461815357208, 0.07383278757333755, 0.010295705869793892, -0.058833882212638855, -0.05129999294877052, 0.04266410320997238, -0.0666459202766418 ... (16698 characters truncated) ... 86563494801521, 0.018577834591269493, 0.007432953920215368, -0.008351198397576809, 0.007157791871577501, -0.021720286458730698, -0.012219857424497604]" with datatype NULL

```

so although I could get a nice bound compiled statement from the longitude and latitude, for the vector itself, I needed to,  use, string substitution, therefore for debugging, I needed to slightly stray from the parameterized safe sql code, but just for debugging purposes. 

```python
vector_string = f"[{', '.join(map(str, vector))}]"
```
So ultimately my debugging style looked like this,


```python

from sqlalchemy import text
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import text

from langchain_huggingface import HuggingFaceEmbeddings


longitude, latitude = "-73.942095", "40.795055"
query = "here is the text I want to embed"
max_miles = 10

embeddings_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

vector = embeddings_model.embed_query(query)
meters_in_mile = 1609.34
max_distance = miles * meters_in_mile  # meters in a mile.

# Convert the list to a string representation
vector_string = f"[{', '.join(map(str, vector))}]"

data = {
  "longitude": longitude, 
  "latitude": latitude, 
  "vector": vector_string, 
  "max_distance": max_distance,
  "meters_in_mile": meters_in_mile,
}    

statement = text("explain analyze " + sql)

# Compile the statement
compiled_statement = statement.bindparams(**data).compile(
    dialect=postgresql.dialect(),
    compile_kwargs={"literal_binds": True}
)

# Print the full SQL query
print(compiled_statement)

with db.engine.connect() as conn:
    results = conn.execute(compiled_statement)

results.fetchall()
```

So skipping to the punchline, ultimately my bug waas I was not using a postgis geography index I had on the places table , because I was using the longitude, latitude values instead . 


So during debugging, I saw the queryplan bottle neck, 

And when I switched to the `geopoint` , finally I started seeing the `geopoint` index being used.



Before, ... showing just the critical part of the slow query plan here, 


```
 ('                                ->  Sort  (cost=6692214.98..6692215.11 rows=52 width=91) (actual time=3202.609..3206.447 rows=15568 loops=3)',),
 ("                                      Sort Key: (st_distance((st_makepoint(places.longitude, places.latitude))::geography, '0101000020E610000068AED3484B7C52C0B9C2BB5CC4654440'::geography, true))",),
 ('                                      Sort Method: quicksort  Memory: 2796kB',),
 ('                                      Worker 0:  Sort Method: quicksort  Memory: 2525kB',),
 ('                                      Worker 1:  Sort Method: quicksort  Memory: 2274kB',),
 ('                                      ->  Parallel Seq Scan on places  (cost=0.00..6692213.50 rows=52 width=91) (actual time=24.712..3161.100 rows=15568 loops=3)',),
 ("                                            Filter: st_dwithin((st_makepoint(longitude, latitude))::geography, '0101000020E610000068AED3484B7C52C0B9C2BB5CC4654440'::geography, '16093.4'::double precision, true)",),
 ('                                            Rows Removed by Filter: 396493',),
 ('Planning Time: 0.420 ms',),
 ('Execution Time: 4194.575 ms',)]

```
and after, again showing just the interesting part of the query plan,

```

                    ->  Nested Loop  (cost=1658.73..143584.64 rows=16 width=171) (actual time=107.942..1563.590 rows=5931 loops=3)
                          ->  Parallel Bitmap Heap Scan on places  (cost=1658.31..142944.00 rows=52 width=91) (actual time=107.366..310.280 rows=15568 loops=3)
                                Filter: st_dwithin(geopoint, '0101000020E610000068AED3484B7C52C0B9C2BB5CC4654440'::geography, '16093.4'::double precision, true)
                                Rows Removed by Filter: 2941
                                Heap Blocks: exact=14630
                                ->  Bitmap Index Scan on idx_places_geopoint  (cost=0.00..1658.28 rows=17299 width=0) (actual time=53.029..53.029 rows=55526 loops=1)
                                      Index Cond: (geopoint && _st_expand('0101000020E610000068AED3484B7C52C0B9C2BB5CC4654440'::geography, '16093.4'::double precision))
                          ->  Index Scan using ix_langchain_pg_embedding_place_id on langchain_pg_embedding lang  (cost=0.42..12.30 rows=2 width=852) (actual time=0.032..0.038 rows=0 loops=46703)
                                Index Cond: (((cmetadata ->> 'place_id'::text))::uuid = places.id)
Planning Time: 5.488 ms
Execution Time: 1630.725 ms
```

## lat / lng originally flipped ! 
A few weeks back, I was getting some weird query results, though I ignored them. everything was so far away! I figured okay I'll just debug this later. turned out everything was far away because my longitude and latitude were flipped and therefore everything was was ordered by a distance that essentially 9,000 miles away !! 😆

## currently, not using that hnsw index
This may very well change very soon, when my batch data insert finishes, but for the initial testing, been using without hnsw index, because it cannot be used easily when using another join. 

let me double check,  I think I settled on materialized, which is the so called "non lazy" CTE, faster, anyway, for my initial test case. my initial prediction, is, 🤞, additional data will not affect speed, because a subset odd pre computed each time. 


