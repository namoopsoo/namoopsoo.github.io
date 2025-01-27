---
date: 2025-01-27
title: fun pool embedding bug
---

Recently, I had been interested in locally reproducing the [ typesense huggingface ](https://huggingface.co/typesense/models/tree/main/all-MiniLM-L12-v2) models on my laptop. I want to experiment with the https://typesense.org nodes, but I also want to be able to use the same embedding models on my laptop for local development. 

I noticed that the models in the typesense section of hugging face are in the `model.onnx` format which I had not encountered before. I learned how to get them running locally and I was able to compare that the vectors on a typesense cluster I was running matched vectors I generated locally. 

However, I was extending the model from single query embedding to batch embedding yesterday and I stumbled upon the weirdnes bug of one query being embedded differently depending on whether I embedded it alone versus in a batch. Eventually I understood what my bug was and after facepalming, wrote up and tested a fix!

## Setting up the onnx model locally

## The bug

## The resolution
