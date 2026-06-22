---
title: "Logseq Search"
# slug: "2026-06-21-logseq-search"
date: 2026-06-21T20:16:54-04:00
# draft: true

# optional thumbnail
images:
  - "THUMBNAIL_PLACEHOLDER"
cover:
  image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->

Just hit a mini milestone today w.r.t. a small project I have been working on, to implement cosine similarity search on my logseq<sup>[4](#references)</sup>  notes. I have embedded a few months worth of my notes with `Qwen/Qwen3-Embedding-0.6B`<sup>[1](#references)</sup> into chromadb and I have a small flask fastapi server<sup>[2,3](#references)</sup>  around this, for querying. I have chunked up my notes before embedding them and therefore results show those chunks. I am serving this on ec2 using tailscale<sup>[5](#references)</sup>, so I can even hit the endpoint from my phone without really exposing it publicly. 

The embedding was too slow to be feasible on my old laptop, so I would probably need to do the full embedding on aws, or perhaps switch to a smaller embedding model like `all-MiniLM-L6-v2`. But before doing this I would like to more robustly consider which model is better. I went with the Qwen model because that is what was used in the out of the box cloudflare AI search I setup for this public blog<sup>[6](#references)</sup> . There has also been a weird issue so far that often very small irrelevant chunks seem to creep up toward the top.

With regard to the observation of tiny chunks floating at the top, let me add a new interesting wrinkle. I was noticing yes that  small utterly irrelevant chunks I often saw in results to my pure cosine similarity  ranked results. So ok maybe maybe small chunks have like nothing embeddings. This kind of would mean small weird chunks get embedded noisily, meaning, not that all small chunks have the some exact embedding but that they have almost some noise penalty that causes them to point into a noisy embedding which is why we see the false positive cosine similarities. But the wrinkle is that queries can be short too! Why wouldn't short queries also be similarly noise-penalized? So if any of this holds water then not only do small chunks need to disappear or be avoided, but queries must also be either rejected if they are too small or somehow otherwise expanded, maybe doubled.


## References
1. https://huggingface.co/Qwen/Qwen3-Embedding-0.6B
2. https://github.com/namoopsoo/logseq-semantic-search
3. https://fastapi.tiangolo.com/
4. https://logseq.com/
5. https://tailscale.com/
6. https://michal.piekarczyk.xyz/note/2026-01-25-hook-up-cloudflare-rag-search/
