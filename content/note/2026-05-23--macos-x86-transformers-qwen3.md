---
title: "Macos X86 Transformers Qwen3"
# slug: "2026-05-23--macos-x86-transformers-qwen3"
date: 2026-05-23T18:44:38-04:00
# draft: true

# optional thumbnail
# images:
#  - "THUMBNAIL_PLACEHOLDER"
#cover:
#  image: "THUMBNAIL_PLACEHOLDER"
---

Quick note here for posterity. I wanted to setup a chromadb with maybe something similar to the `@cf/qwen/qwen3-embedding-0.6b` that I'm using on cloudflare out of the box. 

I setup a new `uv venv --python 3.13` and tried to pull in `uv pip install sentence-transformers chromadb markdown-it-py` and then I wanted to , try qwen3<sup>[1](#references)</sup> from hugging face,


```python

from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")
```

however I ran into several installation roadblocks. Anyway without getting into all the hurdles, ultimately I realized per reading the torch docs<sup>[3](#references)</sup>  and the versions of torch available<sup>[4](#references)</sup>, that my `x86` mac torch support stopped at `torch<2.3`. And after it was only arm64, if I wanted to just grab the wheel file directly. And the torch website recommended python 3.10 . And well, that torch 2.2.2 requires `numpy<2`. And the last twist was that huggingface started listing the qwen3 architecture only by `transformers>=4.51.0`, which can also be seen on their model card<sup>[2](#references)</sup> .

## What worked
So anyways here is what worked, 
```sh
uv venv --python 3.10

```
```
uv pip install\
  "transformers==4.51.0" \
  "sentence-transformers==2.7.0"\
  "numpy<2" \
  torch~=2.2.2\
  chromadb markdown-it-py\
  ipython
```
and finally testing with test code, 

```python

from sentence_transformers import SentenceTransformer

# Load the model
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")


# The queries and documents to embed
queries = [
    "What is the capital of China?",
    "Explain gravity",
]
documents = [
    "The capital of China is Beijing.",
    "Gravity is a force that attracts two bodies towards each other. It gives weight to physical objects and is responsible for the movement of planets around the sun.",
]

# Encode the queries and documents. Note that queries benefit from using a prompt
# Here we use the prompt called "query" stored under `model.prompts`, but you can
# also pass your own prompt via the `prompt` argument
query_embeddings = model.encode(queries, prompt_name="query")
document_embeddings = model.encode(documents)

# Compute the (cosine) similarity between the query and document embeddings

print(similarity)
from sentence_transformers.util import cos_sim
cos_sim(query_embeddings, document_embeddings)
```
```
tensor([[0.7646, 0.1414],
        [0.1355, 0.6000]])
```
The only small difference from the typical example was that my version of transformers does not have the special form, 
```python
similarity = model.similarity(query_embeddings, document_embeddings)
``` 
anyway, maybe there will be other surprises, but so far that has worked.

# References
1. https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
2. https://huggingface.co/Qwen/Qwen3-Embedding-0.6B#sentence-transformers-usage
3. https://pytorch.org/get-started/locally/
4. https://download.pytorch.org/whl/torch/
