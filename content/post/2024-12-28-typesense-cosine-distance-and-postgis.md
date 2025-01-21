---
title: postgis and the order by cosine distance
date: 2024-12-28
---


a bit tricky, not super intuitive in the docs, but I finally found how to builf a typesense query to do what I had previously done with postgres, that is, first constrain by postgis distance and then order by cosine distance.
 

with a `text_embedding` column that embeds a `text` column, and `lat` `lng` available as well, flattened on the same collection, it is possible to query like so,
```json
{	
      "q": query,
      "query_by": "text_embedding",
      "filter_by": 
          f"location:({lat}, {lng}, {radius_km} km)",
      "sort_by": "_vector_distance:asc",
      "exclude_fields": "text_embedding",
      'page': 1,
      'per_page': 100
    }
```
