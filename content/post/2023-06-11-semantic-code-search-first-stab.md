---
date: 2023-06-11
title: Semantic code search first stab
---
public:: true
blog_date:: 2023-06-11
The idea here was to try out Sentence Transformers , https://sbert.net , on source code search. And as a first stab, a corpus was built with, hey why not, the code from the #sentence-transformers repo. 

The documentation at  https://www.sbert.net/examples/applications/semantic-search/README.html#python was used for the basic test here. And a small bit of code at the bottom here, shows how the lines from the python source files were written to a python list first. 

Also, the test results here look pretty decent, but the next step will be to create a reference set of the line numbers that were expected to be found, to get a good precision/recall score for this.
# Initial Learnings
## Learned about [[symmetric vs asymmetric semantic search]]
This distinction refers to #[[sentence similarity task]] where the query is of the same size or asymmetrically, smaller size, such as a one or two word query.
And wow that is exactly what. Iwas looking for !
So apparently this includes the "msmarco" models.

# Final test run
Had a few test runs today, iterating on the approach, using queries from files other than the ones I built a corpus for , #moment/doh haha . Also weirdly the msmarco model documented as the v3 that should be used is MIA somehow, but the v2 seems fine. And "msmarco-MiniLM-L-6-v3" is fine too. 

But here is the last run for today.
18:43 lets try just a few files, so I had initially passed queries I wrote out for the `CrossEncode.py` file , #moment/doh haha , so that is why below, I am pulling `'msmarco-MiniLM-L-6-v3'` and re-encoding because I was puzzled w/ the initial lackluster results and was trying a different model. But yea I realized and just trying this model with the good set of queries instead,
id:: 64864e08-de92-4127-9162-8b5b946b021b
id:: 6486561e-d050-4bca-bc74-64fa5b475ab4
```python
corpus = [x["line"] for x in dataset if "Sentence" in x["path"]]

embedder = SentenceTransformer(
    'msmarco-MiniLM-L-6-v3',
    use_auth_token=hf_token,
)

corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)


In [27]: set([x["path"] for x in dataset if "Sentence" in x["path"]])
Out[27]: 
{'docs/package_reference/SentenceTransformer.md',
 'sentence_transformers/SentenceTransformer.py',
 'sentence_transformers/datasets/ParallelSentencesDataset.py',
 'sentence_transformers/datasets/SentenceLabelDataset.py',
 'sentence_transformers/datasets/SentencesDataset.py',
 'sentence_transformers/evaluation/SentenceEvaluator.py',
 'sentence_transformers/readers/LabelSentenceReader.py'}


In [28]: len(corpus)
Out[28]: 1266

In [34]: %%time
    ...: corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)
    ...: 
    ...: 
# CPU times: user 22.3 s, sys: 4.25 s, total: 26.5 s
# Wall time: 14.8 s

queries = [
    "snapshot_download",
    "SentenceEvaluator",
    "get_torch_home",
    "os.path.join",
    "flax_model.msgpack",
    "torch.nn.functional.normalize",
]

top_k = min(5, len(corpus))
for query in queries:
    query_embedding = embedder.encode(query, convert_to_tensor=True)

    # We use cosine-similarity and torch.topk to find the highest 5 scores
    cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    top_results = torch.topk(cos_scores, k=top_k)

    print("\n\n======================\n\n")
    print("Query:", query)
    print("\nTop 5 most similar sentences in corpus:")

    for score, idx in zip(top_results[0], top_results[1]):
        print(corpus[idx].strip(), "(Score: {:.4f})".format(score))

    """
    # Alternatively, we can also use util.semantic_search to perform cosine similarty + topk
    hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=5)
    hits = hits[0]      #Get the hits for the first query
    for hit in hits:
        print(corpus[hit['corpus_id']], "(Score: {:.4f})".format(hit['score']))
    """
```
19:11 ok nice, this looks really good ! 
id:: 64864f3c-17ce-41b1-a279-39e89b1952e8
```
======================


Query: snapshot_download

Top 5 most similar sentences in corpus:
snapshot_download(model_name_or_path, (Score: 0.6807)
from .util import import_from_string, batch_to_device, fullname, snapshot_download (Score: 0.5153)
# Download from hub with caching (Score: 0.4511)
optimizer.step() (Score: 0.3790)
cache_folder = os.path.join(torch_cache_home, 'sentence_transformers') (Score: 0.3619)


======================


Query: SentenceEvaluator

Top 5 most similar sentences in corpus:
class SentenceEvaluator: (Score: 0.8183)
evaluator: SentenceEvaluator = None, (Score: 0.7497)
from .evaluation import SentenceEvaluator (Score: 0.7004)
the evaluator (Score: 0.5470)
# SentenceTransformer (Score: 0.5083)


======================


Query: get_torch_home

Top 5 most similar sentences in corpus:
from torch.hub import _get_torch_home (Score: 0.8654)
torch_cache_home = _get_torch_home() (Score: 0.8592)
torch_cache_home = os.path.expanduser(os.getenv('TORCH_HOME', os.path.join(os.getenv('XDG_CACHE_HOME', '~/.cache'), 'torch'))) (Score: 0.6630)
import torch (Score: 0.6166)
import torch (Score: 0.6166)


======================


Query: os.path.join

Top 5 most similar sentences in corpus:
file_path = os.path.join(root, filename) (Score: 0.8010)
if not os.path.exists(os.path.join(model_path, 'modules.json')): (Score: 0.7379)
if os.path.exists(os.path.join(model_path, 'modules.json')):    #Load as SentenceTransformer model (Score: 0.7044)
if os.path.exists(model_card_path): (Score: 0.6783)
if os.path.exists(model_name_or_path): (Score: 0.6707)


======================


Query: flax_model.msgpack

Top 5 most similar sentences in corpus:
model = SentenceTransformer('model-name') (Score: 0.4369)
ignore_files=['flax_model.msgpack', 'rust_model.ot', 'tf_model.h5'], (Score: 0.4280)
model: SentenceTransformer (Score: 0.4155)
the model to evaluate (Score: 0.4112)
Evaluate the model (Score: 0.4007)


======================


Query: torch.nn.functional.normalize

Top 5 most similar sentences in corpus:
torch.nn.utils.clip_grad_norm_(loss_model.parameters(), max_grad_norm) (Score: 0.7218)
torch.nn.utils.clip_grad_norm_(loss_model.parameters(), max_grad_norm) (Score: 0.7218)
embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1) (Score: 0.6244)
scaler = torch.cuda.amp.GradScaler() (Score: 0.5749)
from torch import nn, Tensor, device (Score: 0.5742)
```
## And code for building that corpus
ok cool, let me just focus on markdown and python
id:: 648728d8-5958-4df6-95d4-b81de6665974
Put the following into a file `code_search.py`
```python
from pathlib import Path
from itertools import chain


def build_texts_from_repository(repo_dir):
    """Return a dataset of the code
    """
    dataset = []
    file_types = []
    for path in chain(
        Path(repo_dir).glob("**/*.py"),
        Path(repo_dir).glob("**/*.md"),
    ):
        assert path.is_file() and path.suffix
        lines = path.read_text().splitlines()
        
        dataset.extend(
            [{"line_number": i,
               "line": line,
               "path": str(path.relative_to(repo_dir))}
        for i, line in enumerate(lines)
         ]
        )
    return dataset

```
```python
import os
import code_search as cs
from pathlib import Path
repos_dir = os.getenv("REPOS_DIR")
target_dir = Path(repos_dir) / "sentence-transformers"
dataset = cs.build_texts_from_repository(target_dir)

```
double checking , 
```python

In [12]: dataset[:10]
Out[12]: 
[{'line_number': 0,
  'line': 'from setuptools import setup, find_packages',
  'path': 'setup.py'},
 {'line_number': 1, 'line': '', 'path': 'setup.py'},
 {'line_number': 2,
  'line': 'with open("README.md", mode="r", encoding="utf-8") as readme_file:',
  'path': 'setup.py'},
 {'line_number': 3,
  'line': '    readme = readme_file.read()',
  'path': 'setup.py'},
 {'line_number': 4, 'line': '', 'path': 'setup.py'},
 {'line_number': 5, 'line': '', 'path': 'setup.py'},
 {'line_number': 6, 'line': '', 'path': 'setup.py'},
 {'line_number': 7, 'line': 'setup(', 'path': 'setup.py'},
 {'line_number': 8,
  'line': '    name="sentence-transformers",',
  'path': 'setup.py'},
 {'line_number': 9, 'line': '    version="2.2.2",', 'path': 'setup.py'}]

In [13]: set([Path(x["path"]).suffix for x in dataset])
Out[13]: {'.md', '.py'}
```



