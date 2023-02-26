---
title: Quick lang chain test drive
date: 2023-01-29
---


# okay let me try that lang chain demo
- 19:23 ok yea looking at https://beta.openai.com/account/api-keys I did not have an api key yet, so lets try that out.
- how can one use https://github.com/hwchase17/langchain  for [[question-answer-task]] over documentation ?
    - https://langchain.readthedocs.io/en/latest/use_cases/question_answering.html
        - 19:33 wow really cool so https://langchain.readthedocs.io/en/latest/use_cases/question_answering.html#adding-in-sources this says this can provide the sources used in answering a question ! nice

## 19:37 ok so first per 
https://langchain.readthedocs.io/en/latest/getting_started/getting_started.html here, installing this stuff,

#### creating a new environment on my laptop


```python
pip install langchain
pip install openai
pip install faiss-cpu # adding this here after the fact after getting below error 
```

#### 20:11 got one error, 

```python
ValueError: Could not import faiss python package. Please it install it with `pip install faiss` or `pip install faiss-cpu` (depending on Python version).

```

### Ok let me query
the [[New yorker]] #article I added . I recently read [[The American Beast New Yorker]] this article by [[person Jill Lepore]] about the #report that was commissioned about the #[[January 6th Insurrection]] . I used my #iphone #scan-to-text feature to pull in the first page and a half to a text file, `article.txt` to try this out . Let's see how this works.
  

Raw data is here 
https://github.com/namoopsoo/namoopsoo.github.io/blob/hugo-main/data/2022-01-29-lang-chain-quick-look__files/article.txt


```python
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI


with open('article.txt') as f:
  article = f.read()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_text(article)

embeddings = OpenAIEmbeddings()
docsearch = FAISS.from_texts(texts, embeddings)

chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")

query = "What did William Barr do?"
docs = docsearch.similarity_search(query)
```

```python
In [16]: chain.run(input_documents=docs, question=query)
  ...: 
Out[16]: ' William Barr referred to Trump\'s legal team as the "clown car."'
```

#### indeed



{{< figure align=center src="https://s3.amazonaws.com/my-blog-content/2022-01-29-lang-chain-quick-look/IMG_1033_1675042706821_0.jpg" width="50%" >}}


20:24 amazing haha ! Let me try another. 

```python
In [19]: query = "Did Cheney get reelected?"
  ...: docs = docsearch.similarity_search(query)
  ...: chain.run(input_documents=docs, question=query)
  ...: 
Out[19]: ' No, Cheney lost her bid for reelection.'
```

wow !

<img src="https://s3.amazonaws.com/my-blog-content/2022-01-29-lang-chain-quick-look/IMG_1034_1675042979259_0.jpg" width="50%">

#### okay one more 

```python
query = "Was there election fraud?"
docs = docsearch.similarity_search(query)
chain.run(input_documents=docs, question=query)

Out[20]: ' No, the January 6th Report found no evidence of election fraud.'

```

Wow this is really cool! I'm not sure which section was used for this answer. I wonder if it was this one? 

<img src="https://s3.amazonaws.com/my-blog-content/2022-01-29-lang-chain-quick-look/IMG_1035_1675043012989_0.jpg" width="50%">

#### I want to check out the section
here which says you can get a precise link to how the answer to your question was constructed, with the evidence basically.


