---
title: build ground truth golden dataset for comparing embedding models faster with chromadb
date: 2025-02-01
---

Initially, thinking that I wanted to create this grand truth data set quickly, a started out by having a four loop and sampling data from my giant data set of documents, looking for matches to input queries, but this ended up being pretty slow and tedious.
today I switched to just setting up a local index using chroma DB. and this ended up being extremely fast because I am not having to redo the embedding.

But yeah, initially it was counterintuitive. Why should I spend the effort to index all the data but it ended up saving a lot of time I think, especially if I want to scale this and get more ground data. 