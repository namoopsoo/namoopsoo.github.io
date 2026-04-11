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

# inference 
So my intuition for the way GPT inference works is, it starts with fixed weight matrices from pretraining, $$W_Q , W_K, W_V$$ , and during inference, we start with a blank session state. We introduce an input prompt, a sequence of tokens, which is embedded and becomes a matrix X of dimension (num_tokens, size_embedding_model). We also create positional embeddings for input tokens and add that into X. This X matrix is fed into the multihead attention where each head computes self attention scores on the full X  , using those pretrained $$W_Q, W_K, W_V$$ weight matrices that are specific for each head. And this produces now,  K , V cache matrices which represent the relationships between all tokens so far,  but in a masked way meaning token 3 attends to tokens 2 and 1  and token 2 attends to token 1 and token 1 attends to nothing. And the current Q and K  are now used to compute self attention weights , which are multiplied by V which comes from X multiplied by $$W_V$$ . 

And all the self attention outputs for each head pass through their own feed forward network. Then all of those feed forward results of each head are concatenated. After, we come up with  logits for the next token, which we softmax to obtain probabilities against our vocabulary, and argmaxing that gives us just one output token. Now that token is simply one more token attached to the original prompt. And if we did not track the K V cache, we would need to recompute all the causal masked relationships  but since we have it, we just need to add one more row to those K and V matrices, and then compute self attention from K and V. And so now  we continue auto regressing until some kind of stopping condition. And fresh output tokens are included as part of the "output" token sequence.


