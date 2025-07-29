---
date: 2025-01-11
title: objective comparison of embedding models for your use case
---


Recently, I got to the point in a project, of looking into TypeSense as an option for embedding hosting for search. Prior, I was working with one particular embedding model, `all-mpnet-base-v2`, which intuitively and anecdotally performed decently well for my retrieval task. But yea that was the problem, my information was anecdotal and cherry-picked. But when I started looking into TypeSense, I noticed my model of choice was not in the list, https://huggingface.co/typesense/models , and that gave me the direct motivation to finally run a comparison.

Very interestingly in particular, my current choice, `all-mpnet-base-v2`, being a 768 dimension model and the out-of-the-box typesense model, `all-MiniLM-L12-v2`, being a 384 dimension model, and also seemingly under my exploration was also good, led me to compare these. And the main reason here being that given the size of the data in the project at hand, being in the `5 million records` space, and the [ TypeSense back of the envelope ](https://typesense.org/docs/guide/system-requirements.html#for-keyword-search) calculations, choosing between these models meant choosing between paying `$381.60/month` and `$727.20/month` ! 


## So given the motivation, how did I compare these embedding models? 
I did some research and found out about Mean Average Precision (MAP) first, tried that out and also later tried  Mean Reciprocal Rank (MRR), because the bulk of the effort to calculate MAP was building a ground truth dataset and the code to then calculate MRR was trivial.

First the results briefly. So, surprisingly, I found, that although the models performed more or less similarly, the lower dimension model actually appears to be slightly better.

| model | dimensions | MAP | MRR |
| --- | --- | --- | --- |
| "all-MiniLM-L12-v2" | 384 | 0.628 | 0.841 |
|  "all-mpnet-base-v2" | 768 | 0.552 | 0.654 |

I created a dataset with `21` queries, and selected `81 documents`, marking the ones that are relevant for each query. I added these ground truth indications into a `queries.yaml` , looking sort of like the following, since the use case is about querying for documents pertaining to food dishes.

```
- query: Tacos al Pastor
  relevant_docs:
  - id: 120a6b8c-be0c-4913-aaec-1d87422e556b
    text: Al Pastor Super Taco
  - id: 34e7a8e4-fb51-4445-9c63-e0b24989b5a6
    text: Pastor Tacos
  - id: f3cc33f9-c144-44ac-9394-2ac83421dbc9
    text: Al Pastor Taco
- query: French Onion Soup
  relevant_docs:
  - id: 1d9c19df-0a44-4010-a1b2-ea8eae6aa100
    text: French Onion Soup
  - id: d3fd9ffa-31c1-41a5-b681-3f12c8356793
    text: French Onion Soup
  - id: e3573b5b-4a29-4d9d-ad5b-2adc3401cb4f
    text: French Onion Soup - CROCK
```

The documents were larger than the section of text in the `text:` field, but the small snippet was helpful in debugging. Overall, I actually have a corpus of millions of documents, so building a dataset was something I have been procrastinating for a while, since it created a kind of analysis paralysis. However I found I could bootstrap creating a dataset, by first creating, by hand, a list of food queries and then using one of the models, to select out documents, with high cosine similarity. And then, came the task of a lot of manual labor of verifying the relevance of documents by hand. This was definitely tedious. I ended up writing a good chunk of code for doing the bootstrapping, however, and that was super helpful. 

Interestingly, I had run an initial calculation of MAP and MRR, with slightly worse results than above, but I realized I forgot to cross-mark document relevance, that is, after retrieving this union of the `81` relevant documents, I forgot to then also, rerun the cosine similarity, of all queries, one more time, on all the documents, in case there were some documents that were relevant to multiple queries, which I forgot to mark in the `queries.yaml`. This turned out indeed to be the case and when I updated my ground truth `queries.yaml` , subsequently my MAP and MRR scores went up.
