---
title: build ground truth golden dataset for comparing embedding models faster with chromadb
date: 2025-02-01
---

Initially, thinking that I wanted to create this grand truth data set quickly, a started out by having a four loop and sampling data from my giant data set of documents, looking for matches to input queries, but this ended up being pretty slow and tedious.
today I switched to just setting up a local index using chroma DB. and this ended up being extremely fast because I am not having to redo the embedding.

But yeah, initially it was counterintuitive. Why should I spend the effort to index all the data but it ended up saving a lot of time I think, especially if I want to scale this and get more ground data. 



## initial motivation to speed this up 
in a previous post, I described applying Mean Average Precision as well as Mean  Reciprocal Rank,
such that MAP gives a good overall discounted measure of what was retrieved and MRR tells you how quickly you see the first important query results that are relevant, but I wanted to also have a metric somewhere in the middle
so I wanted to implement precision at K, but in order to do that and need to have more relevant documents for each query.

and with my current approach of doing a lot of sampling on the data, I was not getting enough hits and so I figured why not just index the whole thing and then I can quickly get all the hits that are there.
and indeed that paid off because searching is now instantaneous.
