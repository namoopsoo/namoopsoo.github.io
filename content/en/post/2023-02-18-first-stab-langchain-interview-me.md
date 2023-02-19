---
title: Using langchain to interview myself about my skills
date: 2023-02-18
tags:
  - openai
  - langchain
---


### Premise
Ok, got this half baked idea , combine my #brag-document with the available [[langchain]] QA chains into a proof of concept maybe I can call [[langchain interview me 2023-feb]]

So I'm going to throw a bunch of my source material together, language based, accessible as plain text doc, and then I will run the  [Link](https://langchain.readthedocs.io/en/latest/modules/chains/combine_docs_examples/qa_with_sources.html) examples that provide references, citations,

### Ok, so for accumulating my information, 
	  
	  ```python
	  import yaml
	  import tempfile
	  from pathlib import Path
	  from datetime import datetime
	  import pytz
	  
	  def utc_now():
	      return datetime.utcnow().replace(tzinfo=pytz.UTC)
	  
	  def utc_ts(dt):
	      return dt.strftime("%Y-%m-%dT%H%M%S")
	  
	  def read_yaml(loc):
	      with open(loc) as fd:
	          return yaml.safe_load(fd)
	  
	  from pathlib import Path
	  import os
	  repos_dir = Path(os.getenv("REPOS_DIR"))
	  assert repos_dir.is_dir()      
	  experience_loc = repos_dir / "my-challenges-and-accomplishments/experience.yaml"
	  
	  experiences_dict = read_yaml(experience_loc)["Descriptions"]
	  
	  sections = []
	  for project, detail in experiences_dict.items():
	      section = ""
	      if detail.get("company"):
	          company = detail.get("company")
	          section = (f"When I worked at {company}, "
	                    f"there was a project in {detail['year']}, {project}.")
	      elif detail.get("project"):
	          project = detail.get("project")
	          section = f"In {detail['year']}, I had a side project, {project}. "
	      section += ". ".join([x for x in detail.get("one-liners", [])])
	      section += ". ".join([x for x in detail.get("stories", [])])
	      sections.append(section)
	  
	  
	  workdir = repos_dir / "2023-interview-me"    
	  path = workdir / f"{utc_ts(utc_now())}-the-story-blurb.txt" 
	      
	  path.write_text("\n\n\n".join(sections))
	  
	  ```

### Ok let me run now some of the basic question answer chains 
Use my environment from before, 

	  ```sh
	  source ~/.python_venvs/langchainz/bin/activate

	  ```

But when trying to use this just like per the qa with sources example in that [here](https://langchain.readthedocs.io/en/latest/modules/chains/combine_docs_examples/qa_with_sources.html),  

	  ```python
	  
	  from langchain.embeddings.openai import OpenAIEmbeddings
	  from langchain.embeddings.cohere import CohereEmbeddings
	  from langchain.text_splitter import CharacterTextSplitter
	  from langchain.vectorstores.elastic_vector_search import ElasticVectorSearch
	  from langchain.vectorstores import Chroma
	  from langchain.docstore.document import Document
	  from langchain.prompts import PromptTemplate
	  
	  from pathlib import Path
	  
	  workdir = str(repos_dir / "2023-interview-me"  )  
	  story_path = repos_dir / "2023-interview-me" / "2023-02-19T011846-the-story-blurb.txt"
	  
	  my_story = story_path.read_text()
	  
	  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
	  texts = text_splitter.split_text(my_story)
	  
	  embeddings = OpenAIEmbeddings()
	  
	  docsearch = Chroma.from_texts(
	      texts, 
	      embeddings, 
	      metadatas=[{"source": str(i)} for i in range(len(texts))])
	  
	  
	  from langchain.chains.qa_with_sources import load_qa_with_sources_chain
	  from langchain.llms import OpenAI
	  
	  
	  query = "What kind of projects have I worked on with tensor flow?"
	  docs = docsearch.similarity_search(query)
	  chain = load_qa_with_sources_chain(OpenAI(temperature=0), chain_type="stuff")
	  chain({"input_documents": docs, "question": query}, return_only_outputs=True)
	  
	  
	  ```

this line,

	  ```python
	  docsearch = Chroma.from_texts(texts, embeddings, metadatas=[{"source": str(i)} for i in range(len(texts))])
	  
	  ```

yielded a new install request, so that's what I did, 

	  ```
	  ValueError: Could not import chromadb python package. Please it install it with `pip install chromadb`.
	  
	  In [4]: !pip install chromadb
	  ```

Ok wow, so I reran that again and I am getting, 

	  ```python
	  Created a chunk of size 1474, which is longer than the specified 1000
	  Created a chunk of size 2846, which is longer than the specified 1000
	  Created a chunk of size 2348, which is longer than the specified 1000
	  Running Chroma using direct local API.
	  Using DuckDB in-memory for database. Data will be transient.
	  Out[1]: {'output_text': " I have worked on projects with Tensor Flow that involve predicting pilot's states of awareness, predicting bike share rider's destinations, and using Tensor Flow LSTM to answer questions about a CDC Covid dataset.\nSOURCES: 14, 15, 0"}
	  
	  ```

which is not bad

#### So , also I realized the really cool part about the approach here, is that the numbers, correspond simply to the indices of the texts, and the texts split, actually intuitively haha by a double new line, `\n\n` because at least that is how I split them just naturally. 
	  
	  ```python
	  In [2]: len(texts)
	  Out[2]: 16
	  In [6]: text_splitter._separator
	  Out[6]: '\n\n'
	  
	  ```

So since the above output says `14, 15, 0`, I think also this is somewhat sorted by relevance, so let me see what is in those, 

	  ```python
	  In [9]: for i in [14, 15, 0]:
	     ...:     print("i", i, texts[i], "\n===================================================\n\n")
	     ...: 
	  
	        
	  ```

Okay when I looked at that ^^ I noticed actually some texts were getting actually smushed together? There was a lot of information. Going to create my text corpus one more time but this time separating by three newlines . 
	  
Ok let's see , I now created `/Users/michal/Dropbox/Code/repo/2023-interview-me/2023-02-19T015128-the-story-blurb.txt` , lets see if there are more than 16 texts? 

	  ```python

	  story_path = repos_dir / "2023-interview-me" / "2023-02-19T015128-the-story-blurb.txt"
	  
	  my_story = Path(loc).read_text()
	  
	  text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
	  texts = text_splitter.split_text(my_story)
	  
	  In [11]: len(texts)
	  Out[11]: 16
	  ```

Ah ok still 16 texts, but actually maybe this is based on the `chunk_size` ?

### Ok I want to try the chain which gives the intermediate results, 
Also needed one more package, here for the below, 

	  ```
	  ValueError: Could not import tiktoken python package. This is needed in order to calculate get_num_tokens. Please it install it with `pip install tiktoken`.
	  ```

	  ```python
	  
	  query = "What kind of projects have I worked on with tensor flow?"
	  docs = docsearch.similarity_search(query)
	  chain = load_qa_with_sources_chain(OpenAI(temperature=0), 
	                                     chain_type="map_reduce", 
	                                     return_intermediate_steps=True)
	  chain({"input_documents": docs, "question": query}, return_only_outputs=True)
	  ```

Ok this looks like it only returns the relevant statements, nice. 

	  ```python
	  {'intermediate_steps': [" In 2019, I had a side project, Reducing Commercial Aviation Fatalities (kaggle). Designed and built a Tensor Flow LSTM based model to predict pilot's states of awareness, given time series physiological data.",
	    ' None.',
	    ' None',
	    ' None.'],
	   'output_text': " I have worked on a Tensor Flow LSTM based model to predict pilot's states of awareness, given time series physiological data.\nSOURCES: 14"}
	  
	  ```

And the important thing is that this code preserves the original text so I can nicely look for myself exactly at the primary source !

### Let me try another query, 

	  ```python
	  
	  query = "What is my  experience with Docker?"
	  docs = docsearch.similarity_search(query)
	  chain = load_qa_with_sources_chain(OpenAI(temperature=0), 
	                                     chain_type="map_reduce", 
	                                     return_intermediate_steps=True)
	  chain({"input_documents": docs, "question": query}, return_only_outputs=True)
	  
	  {'intermediate_steps': [' "Dockerized our production underwriting stack and split from the main company git repo to give us the flexibility to deploy both scikit learn and XGBoost models with AWS SageMaker."',
	    ' "Helped make better underwriting decisions on returning customers, by optimizing /re-engineering /versioning our SQL based logistic regression model, with a python + Docker + SQL pipeline, cutting runtime from 6+ hours to under an hour."',
	    ' None.',
	    ' None'],
	   'output_text': ' I have no experience with Docker.\nSOURCES: 0, 14'}
	  
	  ```

Hah I feel like I need to do some kind of tuning here? But it is cool to see the intermediate step here even though it is not reflected in the final output.

