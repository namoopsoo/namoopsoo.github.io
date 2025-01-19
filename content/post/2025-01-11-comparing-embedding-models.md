---
date: 2025-01-11
title: objective comparison of embedding models for your use case
---


Recently, I got to the point in a project, of looking into TypeSense as an option for embedding hosting for search. Prior, I was working with one particular embedding model, `all-mpnet-base-v2`, which intuitively and anecdotally performed decently well for my retrieval task. But yea that was the problem, my information was anecdotal and cherry-picked. But when I started looking into TypeSense, I noticed my model of choice was not in the list, https://huggingface.co/typesense/models , and that gave me the direct motivation to finally run a comparison.

Very interestingly in particular, my current choice, `all-mpnet-base-v2`, being a 768 dimension model and the out-of-the-box typesense model, `all-MiniLM-L12-v2`, being a 384 dimension model, and also seemingly under my exploration was also good, led me to compare these. And the main reason here being that given the size of the data in the project at hand, being in the `5 million records` space, and the [ TypeSense back of the envelope ](https://typesense.org/docs/guide/system-requirements.html#for-keyword-search) calculations, choosing between these models meant choosing between paying `$381.60/month` and `$727.20/month` ! 
