---
date: 2025-01-27
title: fun pool embedding bug
---

Recently, I had been interested in locally reproducing the [ typesense huggingface ](https://huggingface.co/typesense/models/tree/main/all-MiniLM-L12-v2) models on my laptop. I want to experiment with the https://typesense.org nodes, but I also want to be able to use the same embedding models on my laptop for local development. 

I noticed that the models in the typesense section of hugging face are in the `model.onnx` format which I had not encountered before. I learned how to get them running locally and I was able to compare that the vectors on a typesense cluster I was running matched vectors I generated locally. 

However, I was extending the model from single query embedding to batch embedding yesterday and I stumbled upon the weirdnes bug of one query being embedded differently depending on whether I embedded it alone versus in a batch. Eventually I understood what my bug was and after facepalming, wrote up and tested a fix!

## Setting up the onnx model locally
So I learned that the typical huggingface python library was not sufficient here.

### install a new library
```sh
cd ~/.python_venvs
uv venv --python 3.11 dish
source dish/bin/activate
which python  # /Users/michal/.python_venvs/dish/bin/python
python --version  # Python 3.11.7
uv pip install ipython
uv pip install optimum[onnxruntime]
```

And I [ downloaded ](https://huggingface.co/typesense/models/tree/main/all-MiniLM-L12-v2) the `config.json	model.onnx	vocab.txt` three files to a new folder, `onnx_models/all-MiniLM-L12-v2`.


### actually it took a few attempts to load the model
Initially I was getting a numpy v1 vs v2 error, 

```python
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

# Load the model
model = ORTModelForSequenceClassification.from_pretrained("all-MiniLM-L12-v2")

# Load tokenizer if available
tokenizer = AutoTokenizer.from_pretrained("all-MiniLM-L12-v2")

# Prepare input
inputs = tokenizer("Hello world!", return_tensors="pt")

# Perform inference
outputs = model(**inputs)
print(outputs.logits)
```

```
A module that was compiled using NumPy 1.x cannot be run in
NumPy 2.2.0 as it may crash. To support both 1.x and 2.x
versions of NumPy, modules must be compiled with NumPy 2.0.
Some module may need to rebuild instead e.g. with 'pybind11>=2.12'.

If you are a user of the module, the easiest solution will be to
downgrade to 'numpy<2' or try to upgrade the affected module.
We expect that some modules will need time to support NumPy 2.
```

### Retrying with python 3.9 and numpy 1.x

```sh
uv venv --python 3.9 dish  # Using CPython 3.9.18 interpreter at: /usr/local/opt/python@3.9/bin/python3.9
source dish/bin/activate
uv pip install ipython optimum[onnxruntime] "numpy<2"

# I saw numpy==1.26.4 , nice!
```

and now loading was fine, 
```python
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer

model_id = "all-MiniLM-L12-v2"

# Load the model
model = ORTModelForFeatureExtraction.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

# Prepare input
inputs = tokenizer("Hello world!", return_tensors="pt")

# Perform inference
outputs = model(**inputs)

# Retrieve embeddings from last_hidden_state (for example)
embeddings = outputs.last_hidden_state
print(embeddings.shape)  # e.g., [batch_size, seq_length, hidden_dim]
```
```
torch.Size([1, 5, 384])
```

## The bug

## The resolution
