---
date: 2023-06-13
title: semantic code search part 2
---
public:: true
blog-date:: 2023-06-13
Ok continuing from [last time](/post/2023-06-11-semantic-code-search-first-stab/), where I ran `sentence_transformers` model `'msmarco-MiniLM-L-6-v3'`  against  a code search problem of comparing query lines against a source code corpus actually from the [sentence_transformers github](https://github.com/UKPLab/sentence-transformers) 

This time, I wanted to write some code around measuring the successful hits from a model run using cosine similarity from sentence_transformers
# Query set choice
I expanded the set of queries slightly, but not that much yet so I could focus on the evaluation code.
## Initially building a dataset, had a snag with reproducibility
So take earlier queries, adding some more manually, and building dataset from them, 

```python
queries = [
    "snapshot_download",
    "SentenceEvaluator",
    "get_torch_home",
    "os.path.join",
    "flax_model.msgpack",
    "torch.nn.functional.normalize",
    "BATCH_HARD_TRIPLET_LOSS",
    "SentenceTransformer('model-name')",
    "DEPRECATED: This class is no longer used",
    "module_config['path']",
    "config_sentence_transformers.json",
    "os.path.join(checkpoint_path, subdir)"
    "torch.nn.utils.clip_grad_norm",
    "getEffectiveLevel",
    "torch.cuda",
]

corpus = [x["line"] for x in dataset if "Sentence" in x["path"]]

import json
import os
import pandas as pd 
import code_search as cs
from pathlib import Path
from date_utils import utc_ts

repos_dir = os.getenv("REPOS_DIR")
target_dir = Path(repos_dir) / "sentence-transformers"
dataset = cs.build_texts_from_repository(target_dir)
workdir = Path(repos_dir) / "code_search"
# Let me save the dataset actually, and build from there, 

df = pd.DataFrame.from_records(dataset)
path = (workdir / "datasets" / f"{utc_ts()}-dataset.csv")
print("saving", path.relative_to(repos_dir))
# saving code_search/datasets/2023-06-13T164234Z-dataset.csv

# Only the non-blank lines,
df[df.line != ""].shape, df.shape  # ((16593, 3), (21953, 3))

df.to_csv(path, index=False)
df2 = pd.read_csv(path)
print(df.equals(df2))  # False,
```
oops was getting False , because of blank lines,
```python

In [20]: df.iloc[:2]
Out[20]: 
   line_number                                         line      path
0            0  from setuptools import setup, find_packages  setup.py
1            1                                               setup.py

In [21]: df2.iloc[:2]
Out[21]: 
   line_number                                         line      path
0            0  from setuptools import setup, find_packages  setup.py
1            1                                          NaN  setup.py


```
### But yea that's okay, I updated the `build_texts_from_repository`  func to ignore blanks
```python
def build_texts_from_repository(repo_dir):
    """Return a dataset of the non-blank lines of code
    """
    dataset = []

    for path in chain(
        Path(repo_dir).glob("**/*.py"),
        Path(repo_dir).glob("**/*.md"),
    ):
        assert path.is_file() and path.suffix
        lines = path.read_text().splitlines()

        dataset.extend(
            [
                {
                    "line_number": i,
                    "line": line,
                    "path": str(path.relative_to(repo_dir))}
                for i, line in enumerate(lines)
                if line.strip() != ""
            ]
        )
    return dataset

```
12:52 slightly updated my func, `"build_texts_from_repository"` to not include the blank lines or lines with just whitespace also !

ok trying again, 
```python

import json
import os
import pandas as pd 
import code_search as cs
from pathlib import Path
from date_utils import utc_ts

repos_dir = os.getenv("REPOS_DIR")
target_dir = Path(repos_dir) / "sentence-transformers"
dataset = cs.build_texts_from_repository(target_dir)
workdir = Path(repos_dir) / "code_search"

df = pd.DataFrame.from_records(dataset)

# Now should be only the non-blank lines,
print("blanks", df[df.line == ""].shape[0])  # blanks 0

path = (workdir / "datasets" / f"{utc_ts()}-dataset.csv")
print("saving", path.relative_to(repos_dir))
# saving code_search/datasets/2023-06-13T170451Z-dataset.csv

df.to_csv(path, index=False)
df2 = pd.read_csv(path)
print(df.equals(df2))  # True

# And vanilla python equals?
df2.to_dict(orient="records") == dataset
# Out[62]: True

```
13:05 ok cool, worked this time !
13:48 save the subset, too, 
```python

# Only the subset with sentence filenames, 
path = (workdir / "datasets" / f"{utc_ts()}-dataset-sentence-filenames.csv")
print("saving", path.relative_to(repos_dir))
# saving code_search/datasets/2023-06-13T174927Z-dataset-sentence-filenames.csv

df = pd.DataFrame.from_records(
    [x for x in dataset if "Sentence" in x["path"]]
)
df.to_csv(path, index=False)
print("read equals", df.equals(pd.read_csv(path)))  # read equals True
```


## The query set
13:37 ok lets run the simplistic search first,

```python
def build_query_dataset(queries, dataset):
    """
    Args:
        queries: plain list of strings
        dataset: list of dictionaries with ["line_number", "line", "path"]
            Example

            [{'line_number': 35,
              'line': '            name = "_"+name',
              'path': 'sentence_transformers/evaluation/MSEEvaluatorFromDataFrame.py'},
             {'line_number': 110,
              'line': 'if not os.path.exists(queries_filepath):',
              'path': 'examples/training/ms_marco/train_bi-encoder_mnrl.py'},
             {'line_number': 52,
              'line': "tracer = logging.getLogger('elasticsearch') ",
              'path': 'examples/training/data_augmentation/train_sts_indomain_bm25.py'}]

    """
    search_results = []
    for query in tqdm(queries):
        findings = [
            {"query": query, **x
             }
            for x in dataset if query in x["line"]
        ]
        search_results.extend(findings)
    return search_results

```
```python
import os
from pathlib import Path
import code_search as cs
import pandas as pd

repos_dir = os.getenv("REPOS_DIR")
path = (Path(repos_dir) /
        "code_search/datasets/2023-06-13T174927Z-dataset-sentence-filenames.csv"
       )
dataset = pd.read_csv(path).to_dict(orient="records")

queries = [
    "snapshot_download",
    "SentenceEvaluator",
    "get_torch_home",
    "os.path.join",
    "flax_model.msgpack",
    "torch.nn.functional.normalize",
    "BATCH_HARD_TRIPLET_LOSS",
    "SentenceTransformer('model-name')",
    "DEPRECATED: This class is no longer used",
    "module_config['path']",
    "config_sentence_transformers.json",
    "os.path.join(checkpoint_path, subdir)"
    "torch.nn.utils.clip_grad_norm",
    "getEffectiveLevel",
    "torch.cuda",
]

search_results = cs.build_query_dataset(queries, dataset)
100%|███████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 14/14 [00:00<00:00, 6913.96it/s]

In [5]: len(search_results)
Out[5]: 43
  
In [8]: len(queries)
Out[8]: 14

searchdf = pd.DataFrame.from_records(search_results)
searchdf["query"].value_counts()
# 
os.path.join                                20
torch.cuda                                   5
SentenceEvaluator                            4
config_sentence_transformers.json            3
snapshot_download                            2
get_torch_home                               2
flax_model.msgpack                           1
torch.nn.functional.normalize                1
BATCH_HARD_TRIPLET_LOSS                      1
SentenceTransformer('model-name')            1
DEPRECATED: This class is no longer used     1
module_config['path']                        1
getEffectiveLevel                            1
Name: query, dtype: int64
```
13:59 ok haha that was instantaneous. Ok so lets evaluate the sentence_transformer accuracy then,
Maybe this is a bit unbalanced, but this is good enough for now.

# And running the query
## semantic search
And again using the use of semantic_search as nicely described in https://www.sbert.net/examples/applications/semantic-search/README.html#python ,

14:55 For now let's use the number `20` from above, as the number of results to retrieve for each query, since that is the max number of  results we get for any query.
```python
import torch
import os
import pandas as pd
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.util import semantic_search
from importlib import reload
import code_search as cs

hf_token = os.getenv("HF_TOKEN")
embedder = SentenceTransformer(
    'msmarco-MiniLM-L-6-v3',
    use_auth_token=hf_token,
)
repos_dir = os.getenv("REPOS_DIR")
path = (Path(repos_dir) /
        "code_search/datasets/2023-06-13T174927Z-dataset-sentence-filenames.csv"
       )
dataset = pd.read_csv(path).to_dict(orient="records")
corpus = [x["line"] for x in dataset]
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

queries = [
    "snapshot_download",
    "SentenceEvaluator",
    "get_torch_home",
    "os.path.join",
    "flax_model.msgpack",
    "torch.nn.functional.normalize",
    "BATCH_HARD_TRIPLET_LOSS",
    "SentenceTransformer('model-name')",
    "DEPRECATED: This class is no longer used",
    "module_config['path']",
    "config_sentence_transformers.json",
    "os.path.join(checkpoint_path, subdir)"
    "torch.nn.utils.clip_grad_norm",
    "getEffectiveLevel",
    "torch.cuda",
]

top_k = 20  # hat is the max number of  results we get for any query so far.

resultsdf = cs.run_semantic_search(embedder, dataset, queries, top_k)
```
## Merge results
16:46 merging results and initial dataset, the results are pytorch tensors which looks like they are treated as objects in pandas land ,

```python
ipdb> p resultsdf.head()
            score          idx              query
0  tensor(0.6807)   tensor(73)  snapshot_download
1  tensor(0.5153)   tensor(24)  snapshot_download
2  tensor(0.4511)   tensor(72)  snapshot_download
3  tensor(0.3790)  tensor(584)  snapshot_download
4  tensor(0.3619)   tensor(55)  snapshot_download
ipdb> p resultsdf.head().dtypes
score    object
idx      object
query    object
dtype: object
ipdb> 

```
so let me cast that,
```python
ipdb> p resultsdf.astype({"idx": "int", "score": "float"}).merge(truthdf, left_on="idx", right_index=True, how="left").head()
      score  idx              query  line_number                                               line                                          path
0  0.680669   73  snapshot_download           86                      snapshot_download(model_na...  sentence_transformers/SentenceTransformer.py
1  0.515324   24  snapshot_download           25  from .util import import_from_string, batch_to...  sentence_transformers/SentenceTransformer.py
2  0.451125   72  snapshot_download           85                      # Download from hub with c...  sentence_transformers/SentenceTransformer.py
3  0.379038  584  snapshot_download          725                                   optimizer.step()  sentence_transformers/SentenceTransformer.py
4  0.361899   55  snapshot_download           62                  cache_folder = os.path.join(to...  sentence_transformers/SentenceTransformer.py
ipdb> 
```
```python
In [25]: with ipdb.launch_ipdb_on_exception():
    ...:     resultsdf = cs.run_semantic_search(embedder, dataset, queries, top_k)
    ...: 
100%|████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 14/14 [00:00<00:00, 100.97it/s]

In [26]: resultsdf.head()
Out[26]: 
      score              query  line_number                                               line                                          path
0  0.680669  snapshot_download           86                      snapshot_download(model_na...  sentence_transformers/SentenceTransformer.py
1  0.515324  snapshot_download           25  from .util import import_from_string, batch_to...  sentence_transformers/SentenceTransformer.py
2  0.451125  snapshot_download           85                      # Download from hub with c...  sentence_transformers/SentenceTransformer.py
3  0.379038  snapshot_download          725                                   optimizer.step()  sentence_transformers/SentenceTransformer.py
4  0.361899  snapshot_download           62                  cache_folder = os.path.join(to...  sentence_transformers/SentenceTransformer.py

```

## Evaluate
17:11 ok so how to evaluate truth against the results now

Maybe, given a threshold, like `0.5` , how many hits and misses.
Perhaps one way to evaluate , would be to left join `truthdf` with `resultsdf` in order to count the hits at least. And misses are the left anti-join then.
```python
import pandas as pd
from date_utils import utc_ts
repos_dir = os.getenv("REPOS_DIR")

search_results = cs.build_query_dataset(queries, dataset)
truthdf = pd.DataFrame.from_records(search_results)
workdir = Path(repos_dir) / "code_search"
In [37]: set(truthdf.columns.tolist()) & set(resultsdf.columns.tolist())
Out[37]: {'line', 'line_number', 'path', 'query'}
  
eval_df = pd.merge(
    truthdf,
    resultsdf.drop(["line"], axis=1),
    on=["query", "path", "line_number"],
    how="left")

path = (workdir 
        / f"{utc_ts()}-evaldf.csv")
print("saving", path.relative_to(repos_dir))
# saving code_search/2023-06-13T213516Z-evaldf.csv

eval_df.to_csv(path, index=False)
```
```python
In [46]: eval_df
Out[46]: 
                                       query  line_number                                               line                                               path     score
0                          snapshot_download           25  from .util import import_from_string, batch_to...       sentence_transformers/SentenceTransformer.py  0.515324
1                          snapshot_download           86                      snapshot_download(model_na...       sentence_transformers/SentenceTransformer.py  0.680669
2                          SentenceEvaluator           24          from .evaluation import SentenceEvaluator       sentence_transformers/SentenceTransformer.py  0.700384
3                          SentenceEvaluator          576               evaluator: SentenceEvaluator = None,       sentence_transformers/SentenceTransformer.py  0.749687
4                          SentenceEvaluator          756      def evaluate(self, evaluator: SentenceEval...       sentence_transformers/SentenceTransformer.py  0.403172
5                          SentenceEvaluator            0                           class SentenceEvaluator:  sentence_transformers/evaluation/SentenceEvalu...  0.818287
6                             get_torch_home           56                      from torch.hub import _get...       sentence_transformers/SentenceTransformer.py  0.865429
7                             get_torch_home           58                      torch_cache_home = _get_to...       sentence_transformers/SentenceTransformer.py  0.859171
8                               os.path.join           60                      torch_cache_home = os.path...       sentence_transformers/SentenceTransformer.py       NaN
9                               os.path.join           62                  cache_folder = os.path.join(to...       sentence_transformers/SentenceTransformer.py       NaN
10                              os.path.join           82                  model_path = os.path.join(cach...       sentence_transformers/SentenceTransformer.py  0.662760
11                              os.path.join           84                  if not os.path.exists(os.path....       sentence_transformers/SentenceTransformer.py  0.737865
12                              os.path.join           93              if os.path.exists(os.path.join(mod...       sentence_transformers/SentenceTransformer.py  0.704441
13                              os.path.join          362          with open(os.path.join(path, 'config_s...       sentence_transformers/SentenceTransformer.py       NaN
14                              os.path.join          371                  model_path = os.path.join(path...       sentence_transformers/SentenceTransformer.py  0.666143
15                              os.path.join          377          with open(os.path.join(path, 'modules....       sentence_transformers/SentenceTransformer.py  0.623291
16                              os.path.join          428          with open(os.path.join(path, "README.m...       sentence_transformers/SentenceTransformer.py  0.619979
17                              os.path.join          487                  create_model_card = replace_mo...       sentence_transformers/SentenceTransformer.py       NaN
18                              os.path.join          494                      file_path = os.path.join(r...       sentence_transformers/SentenceTransformer.py  0.800986
19                              os.path.join          520                      shutil.rmtree(os.path.join...       sentence_transformers/SentenceTransformer.py       NaN
20                              os.path.join          774              eval_path = os.path.join(output_pa...       sentence_transformers/SentenceTransformer.py  0.621379
21                              os.path.join          788          self.save(os.path.join(checkpoint_path...       sentence_transformers/SentenceTransformer.py  0.598843
22                              os.path.join          795                      old_checkpoints.append({'s...       sentence_transformers/SentenceTransformer.py       NaN
23                              os.path.join          816          config_sentence_transformers_json_path...       sentence_transformers/SentenceTransformer.py       NaN
24                              os.path.join          825          model_card_path = os.path.join(model_p...       sentence_transformers/SentenceTransformer.py  0.637539
25                              os.path.join          834          modules_json_path = os.path.join(model...       sentence_transformers/SentenceTransformer.py  0.627189
26                              os.path.join          841              module = module_class.load(os.path...       sentence_transformers/SentenceTransformer.py       NaN
27                              os.path.join           20          for line in open(os.path.join(self.fol...  sentence_transformers/readers/LabelSentenceRea...  0.568704
28                        flax_model.msgpack           90                                          ignore...       sentence_transformers/SentenceTransformer.py  0.427975
29             torch.nn.functional.normalize          183                          embeddings = torch.nn....       sentence_transformers/SentenceTransformer.py  0.624402
30                   BATCH_HARD_TRIPLET_LOSS           13      This dataset can be used for some specific...  sentence_transformers/datasets/SentenceLabelDa...  0.738400
31         SentenceTransformer('model-name')            5          model = SentenceTransformer('model-name')      docs/package_reference/SentenceTransformer.md  0.909370
32  DEPRECATED: This class is no longer used            8      DEPRECATED: This class is no longer used. ...  sentence_transformers/datasets/SentencesDatase...  0.766369
33                     module_config['path']          841              module = module_class.load(os.path...       sentence_transformers/SentenceTransformer.py  0.627141
34         config_sentence_transformers.json          362          with open(os.path.join(path, 'config_s...       sentence_transformers/SentenceTransformer.py  0.548365
35         config_sentence_transformers.json          815          # Check if the config_sentence_transfo...       sentence_transformers/SentenceTransformer.py  0.662415
36         config_sentence_transformers.json          816          config_sentence_transformers_json_path...       sentence_transformers/SentenceTransformer.py  0.760809
37                         getEffectiveLevel          135              show_progress_bar = (logger.getEff...       sentence_transformers/SentenceTransformer.py  0.428602
38                                torch.cuda          103              device = "cuda" if torch.cuda.is_a...       sentence_transformers/SentenceTransformer.py  0.779811
39                                torch.cuda          215                      if torch.cuda.is_available():       sentence_transformers/SentenceTransformer.py  0.835975
40                                torch.cuda          216                  target_devices = ['cuda:{}'.fo...       sentence_transformers/SentenceTransformer.py  0.616090
41                                torch.cuda          637                from torch.cuda.amp import autocast       sentence_transformers/SentenceTransformer.py  0.695091
42                                torch.cuda          638               scaler = torch.cuda.amp.GradScaler()       sentence_transformers/SentenceTransformer.py  0.645202
```
17:40 ok cool , although wonder how not all the "os.path.join" lines were matched. Maybe some debugging to do.
Also should still built the [[anti join]] to get the misses aka [[false-positive]] too.
