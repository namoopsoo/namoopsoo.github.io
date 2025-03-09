---
title: transformer architecture sweet spot
date: 2025-03-09
---

# What is the transformer architecture?
Let me try for a, hopefully a sweet spot explanation.

A deep neural network, trained by back propagation, with language data, first by self supervised learning (aka pre-training) using Masked Language Modeling, and then by fine tuning, for tasks like text summarization, part of speech labeling, Name Entity Recognition labeling, question answering, translation, and others.

Self supervision, by way of next token prediction or more generally masked language modeling , lets a model to be trained without human generated labels.

It may be that a diagram is not the best way of explaining the attention mechanism that is the core of the transformer, but instead linear algebra or just matrix math more generally.


mathjax test, 

$$a_4 \ne b_4$$

or take 2, 


$$a\_4 \ne b\_4$$
