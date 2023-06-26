---
date: 2023-06-25
title: everybody loves reynauds
---
# Inspiration
Haha so per the joke of a friend about "Reynaud's" sounds like "Raymond" as in "Everyone loves Raymond" , I was wondering, can sentence transformers tell the difference?
But haha spoiler alert sort is is that if a model finds this funny then that might also not really understand the medical condition at play here , haha nervous laughter, 😅
# Quick look
let's compare this first  embedding model

```python
import os
from sentence_transformers.util import semantic_search, cos_sim
from sentence_transformers import SentenceTransformer, util

import torch
hf_token = os.getenv("HF_TOKEN")
embedder = SentenceTransformer(
    'msmarco-MiniLM-L-6-v3',
    use_auth_token=hf_token,
)

corpus = ["Everybody Loves Raymond",
         " blood vessels go into a temporary spasm",
         "blocked flow of blood in fingers",
         "Everybody Loves Numbness",
         "Everybody Loves cold fingers",
         "Everybody Loves Reindeer",
         "Everybody Loves Riynudno"]
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

query = "Everybody Loves Raynaud"
query_embedding = embedder.encode(query, convert_to_tensor=True)

cos_scores = cos_sim(query_embedding, corpus_embeddings)[0]
top_results = torch.topk(cos_scores, k=7)

cos_scores, top_results

print("Query:\n", query, "\n")

for score, idx in zip(top_results[0], top_results[1]):
    print(corpus[idx].strip(), "(Score: {:.4f})".format(score))

```
output 
```python
Query:
 Everybody Loves Raynaud 

Everybody Loves Raymond (Score: 0.5585)
Everybody Loves Reindeer (Score: 0.4803)
Everybody Loves cold fingers (Score: 0.4661)
Everybody Loves Riynudno (Score: 0.4394)
Everybody Loves Numbness (Score: 0.3434)
blocked flow of blood in fingers (Score: 0.0891)
blood vessels go into a temporary spasm (Score: -0.0003)
```
I don't think that embedding model is using a semantic embedding space, but rather just a more simplistic text similarity embedding.
Or maybe the vocabulary is too small and simply does not include medical terminology?

# Hmm okay lets look at more embedding models
Ok, lets use a bunch from https://www.sbert.net/docs/pretrained_models.html ,
Let's try a different maybe larger embedding model 

```python
from tqdm import tqdm

def compare_raymond(model_name, query, corpus):
    hf_token = os.getenv("HF_TOKEN")
    embedder = SentenceTransformer(
        model_name,
        use_auth_token=hf_token,
    )

    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    query_embedding = embedder.encode(query, convert_to_tensor=True)

    cos_scores = cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=len(corpus))

    cos_scores, top_results
    # print("Query:\n", query, "\n")

    results = []
    for score, idx in zip(top_results[0], top_results[1]):
        results.append(
          {"sentence": corpus[idx].strip(), 
           "score": round(float(score), 4),
           "model_name": model_name})
        # print(corpus[idx].strip(), "(Score: {:.4f})".format(score))
    return results
        
        
corpus = ["Everybody Loves Raymond",
          " blood vessels go into a temporary spasm",
          "blocked flow of blood in fingers",
          "Everybody Loves Numbness",
          "Everybody Loves cold fingers",
          "Everybody Loves Reindeer",
          "Everybody Loves Riynudno"]
query = "Everybody Loves Raynaud"
model_names = ["all-MiniLM-L12-v2", 
              "all-mpnet-base-v2",
              "all-distilroberta-v1",
              "multi-qa-distilbert-cos-v1",
              "msmarco-MiniLM-L-6-v3"]
results = []
for model_name in tqdm(model_names):
    print("\n=====================")
    print("Lets try", model_name)
    results.extend(compare_raymond(model_name, query, corpus))
    
df = pd.DataFrame.from_records(results)    
```
## Interesting
Some results, so looking here, some models appear to score the semantic medical concepts higher, such as "all-MiniLM-L12-v2" , and most of the others appear to be somewhat confused haha.

```python
In [63]: df.sort_values(by=["model_name", "score"], ascending=False)
Out[63]: 
                                   sentence   score                  model_name
21                  Everybody Loves Raymond  0.5439  multi-qa-distilbert-cos-v1
22                 Everybody Loves Riynudno  0.4822  multi-qa-distilbert-cos-v1
23                 Everybody Loves Reindeer  0.3610  multi-qa-distilbert-cos-v1
24             Everybody Loves cold fingers  0.3152  multi-qa-distilbert-cos-v1
25                 Everybody Loves Numbness  0.3014  multi-qa-distilbert-cos-v1
26         blocked flow of blood in fingers  0.0435  multi-qa-distilbert-cos-v1
27  blood vessels go into a temporary spasm  0.0012  multi-qa-distilbert-cos-v1
28                  Everybody Loves Raymond  0.5585       msmarco-MiniLM-L-6-v3
29                 Everybody Loves Reindeer  0.4803       msmarco-MiniLM-L-6-v3
30             Everybody Loves cold fingers  0.4661       msmarco-MiniLM-L-6-v3
31                 Everybody Loves Riynudno  0.4394       msmarco-MiniLM-L-6-v3
32                 Everybody Loves Numbness  0.3434       msmarco-MiniLM-L-6-v3
33         blocked flow of blood in fingers  0.0891       msmarco-MiniLM-L-6-v3
34  blood vessels go into a temporary spasm -0.0003       msmarco-MiniLM-L-6-v3
7                  Everybody Loves Riynudno  0.4585           all-mpnet-base-v2
8                  Everybody Loves Numbness  0.4368           all-mpnet-base-v2
9              Everybody Loves cold fingers  0.4192           all-mpnet-base-v2
10                 Everybody Loves Reindeer  0.3416           all-mpnet-base-v2
11                  Everybody Loves Raymond  0.2641           all-mpnet-base-v2
12         blocked flow of blood in fingers  0.2256           all-mpnet-base-v2
13  blood vessels go into a temporary spasm  0.1393           all-mpnet-base-v2
14                 Everybody Loves Riynudno  0.7082        all-distilroberta-v1
15                  Everybody Loves Raymond  0.5761        all-distilroberta-v1
16                 Everybody Loves Reindeer  0.4612        all-distilroberta-v1
17                 Everybody Loves Numbness  0.4181        all-distilroberta-v1
18             Everybody Loves cold fingers  0.3880        all-distilroberta-v1
19         blocked flow of blood in fingers  0.0297        all-distilroberta-v1
20  blood vessels go into a temporary spasm -0.0023        all-distilroberta-v1
0              Everybody Loves cold fingers  0.4929           all-MiniLM-L12-v2
1                  Everybody Loves Numbness  0.4379           all-MiniLM-L12-v2
2          blocked flow of blood in fingers  0.4075           all-MiniLM-L12-v2
3                  Everybody Loves Riynudno  0.3814           all-MiniLM-L12-v2
4                   Everybody Loves Raymond  0.3706           all-MiniLM-L12-v2
5   blood vessels go into a temporary spasm  0.3055           all-MiniLM-L12-v2
6                  Everybody Loves Reindeer  0.2809           all-MiniLM-L12-v2
```

# Okay so then
Actually wow this is kind of inspiring, with respect to another problem I was facing in that if semantic similarity was not working for me earlier maybe it is because the embedding model I was using just was not trained on the subject matter I was trying to use it on.

And a different one is needed or I need to fine tune one instead if that is easier.

