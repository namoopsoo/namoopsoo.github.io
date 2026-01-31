---
title: "Hook Up Cloudflare Rag Search"
date: 2026-01-31
draft: false
---

Here are some of my notes on adding Cloudflare AI search as the endpoint for my hugo site's search.

# Summary
The other weekend, I randomly looked into some minimal ways to set up RAG search on my hugo site. A year prior, I had tried out TypeSense as a hosted vector embedding store for a several million row many gigabyte dataset but a hugo text site is pretty small so I was wondering what the price might be for this. Cloudflare AI Search came up, incidentally as not only a vector store alternative but a self contained store with indexing and a small RAG layer on top. 

I was able to set up the auto indexing in one day and then the next weekend, in maybe half a day, I setup my hugo to talk to the AI Search endpoint.

The effort was so minimal because actually the cloudflare documentation was really excellent and also I leaned heavily on ChatGPT codex to override the Hugo standard built in fuse search javascript to talk my new worker instead.

# Bird's eye view
Briefly, the setup involved the following steps:
- Move my DNS over from my registrar to cloudflare, because that was a prerequisite for cloudflare to automatically embed and index a website.
- Use the excellent cloudflare docs<sup>[2](#references)</sup> to spin up AI search against the domain I'm now managing through cloudflare. (Initially I tried using the UI but this kept attempting to use my main domain as opposed to my subdomain)
- With just some button clicks on the dashboard, activate a worker to proxy traffic to the AI search service (I did try doing this by the API as well, but I could not find great documentation for that part actually).
- Override my hugo search page and search javascript to hit my cloudflare worker endpoint. (I Used ChatGPT Codex here for the heavy lifting and I played the role of QA, adjusting incrementally the pr prompt based on what I saw).


# References 
1. https://developers.cloudflare.com/ai-search/how-to/brower-rendering-autorag-tutorial/
2. https://developers.cloudflare.com/ai-search/get-started/api/