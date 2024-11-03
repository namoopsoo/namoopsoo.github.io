---
title: langchain_pgvector bug
date: 2024-11-02
---

I had a issue where ,  using the langchain_pgvector library, with the vectorstore.add_documents function call, which has worked for me before for a while but somehow, for a new collection, I’m  trying to add thousands of documents, but only a handful get added, and without errors. Very weird . 

I didn't see any useful patterns in the 4 out of 1022 documents that did get added, and pdb tracing through the code did not reveal any silent errors. 

The answer ended up being, that the Python library I was using, langchain_pgvector , instead of adding records into the collection I specified, was updating records that already existed with the same id’s in a different collection on my database. What a crazy bug that ate many of my hours.

When i think about it in  retrospect, it makes  perfect sense, because that's just the uniqueness constraint of the table, langchain_embeddings , but since i was referring to a different collection name at the Python wrapper level, i would have expected this to raise an error.

😅this ate a lot of my time yesterday. But glad i found the issue.