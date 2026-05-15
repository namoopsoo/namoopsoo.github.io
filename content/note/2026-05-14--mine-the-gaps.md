---
title: Perception Gaps
date: 2026-05-14
draft: true
---

Why are  the AI capabilities discussions  so polarizing? People either see current AI as a net negative or net positive. But the gap is a chasm. Well ok maybe there are people who are uncertain too. Okay maybe it is task specific. But the edges are quite extremely different! Why?

I suspect the split aligns, along whether believe in planning. 

On the one hand, yes there are many AI aided workflows that produce very stable reliable outcomes. And that side is growing. But some people see the billion dollar single person start up around the corner.

# Some capabilities 
RAG search is great. Its a great pattern that can be a good boost beyond just BM25. Plus yoou can better contextualize the result in English, say.

Then you can also use this concept for routing questions, tie them to tasks or skills, and boom you have an agent. The possibilities here can be endless perhaps. A solid genefal purpose paradigm shift to building software. You still need to build the skills. If you want them to be reliable and deterministic you should hand code them. 

Code stack trace debugging .  This one can be hit or miss depending on if the model has been fine tuned on the relevant issues . Maybe cosine similarity search helps too with RAG. Unclear.

Learning. Yes can really help.

Code Gen? Here is our datacenter of geniuses? Or not. This feels very hit or miss!

Parallelizing everything with an army of agents? Maybe if the same task, like map reduce. But tasks with unknowns, this seeems to break down withoue humans in the loop.  

# Reality is the Bottleneck 
I am sure someone has already written abouy this in complexity theory, or chaos theory, but I think humans are at a theoretical upper bound for intelligence and impqct as constrained by the real world. Got reminded of this through the recursive self improvement topic [2] Carl discusses.

Back to the addage that information is not enough for success else everyone would be a six pack ab wielding millionaire, reality is the bottleneck. Defining  intelligence is squishy but I threw in impact there too becauss no matter how good a model is , your brain or a statistical model, it will be wrong. 

> All models are wrong. Some are useful.

### Not really reasoning 
There are not enough atoms in the universe to build compute to predict the correct path through a complex problem. And  path is the operative word here. Reasoning models have a very strange name because they dont "think", they do.  They one shot write plans then run them<sup>[7](#references)</sup>. They will course correct too of cours but they are doing it in reality not in a self contained logic center. 

They should really be called while -looped models, though code-harnessed , another recent term, is   more fitting.  

### The Age of Reason
What is a better definition of reasoning? It is using logic and thought experiments and armchair testing ideas. It is thinking out loud. Actually that's probably why reasoning models got their name. Because of the chain of thought. And maybe I should go back to the previous paragraph and distinguish between an active agentic,--*touch and smell the world*--,   and chain of thought. 

So thinking out loud helps people I think in a different way than  the mimickry of what we see in LLM use. We have seen CoT not nedessarily having a benefit<sup>[8,9](#references)</sup>. 

# P vs NP Problem 
Everything may change if the P vs NP Problem is solved. If a problem can be easily verified, is there a way to solve it in general?

As an aside , LLMs feign solving P vs NP because they clearly produce answers in linear time, a consistent token rate. And thqts why jokingly Yann Lecun has called LLMs as giant lookup tables. But yes the look up table cheat code is a cheat code .

1. https://open.substack.com/pub/matthewpikar/p/stop-adopting-ai-start-transforming?r=d7b46&utm_medium=ios

2. https://youtu.be/AkadGXzDqBw Carl on recursive self improvement 
3. https://michal.piekarczyk.xyz/note/2026-05-01-odsc-closing-notes/
4. https://en.wikipedia.org/wiki/P_versus_NP_problem
5. halting problem
6. no free lunch
7. https://michal.piekarczyk.xyz/note/2026-03-04-prompt-driven-development/#reasoning

8. https://arxiv.org/pdf/2504.00294v1 inference time scaling

9. https://youtu.be/ShusuVq32hc , George Montañez , on reasoning 


