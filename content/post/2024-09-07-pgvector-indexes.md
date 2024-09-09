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