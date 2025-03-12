---
title: transformer architecture sweet spot
date: 2025-03-09
---

_(DRAFT for now )_

# What is the transformer architecture?
Let me try for a, hopefully a sweet spot explanation.


A deep neural network, trained by back propagation, with language data, first by self supervised learning (aka pre-training) using Masked Language Modeling, and then by fine tuning, for tasks like text summarization, part of speech labeling, Name Entity Recognition labeling, question answering, translation, and others.

Self supervision, by way of next token prediction or more generally masked language modeling , lets a model to be trained without human generated labels.

It may be that a diagram is not the best way of explaining the attention mechanism that is the core of the transformer, but instead linear algebra or just matrix math more generally.


## Names for concepts,
(borrowing notation and concepts from https://sebastianraschka.com/blog/2023/self-attention-from-scratch.html , )

query sequence, $$q^{(i)}$$, for embedded input $$i$$. As well as key sequence, and value sequence, built from the query, key and value weight matrices .

attention vector per each input element.

And query and key sequences are involved in a dot product to produce unnormalized attention weights.

$$\omega_{ij} = q^{(i)^T} k^{(j)}$$ 

Normalized attention weights are _softmaxed_ unnormalized attention weights, along with a scaling factor, $$1/{\sqrt d_{k}}$$ , 

like, 

 $$\alpha_{2,i} = softmax(\frac{\omega_{2,i}}{{\sqrt d_{k}}})$$


Finally, after computing $$ \alpha_{2,1}, \alpha_{2,j}, ..., \alpha_{2,T} $$  for all terms, related to the $$x^{(2)}$$ input token, we also have the *context vector* $$z^{(2)} = \sum_{j=1}^{T} \alpha_{2,j} v^{(j)}$$
