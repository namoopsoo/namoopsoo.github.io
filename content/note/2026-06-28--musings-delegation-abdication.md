---
title: "Musings Delegation Abdication"
# slug: "2026-06-28--musings-delegation-abdication"
date: 2026-06-26T13:39:01-04:00
draft: false

images:
  - "https://s3.amazonaws.com/my-blog-content/2026-06-28--musings-delegation-abdication/2026-06-28-unlock-car-complexity--2c817300-4f22-44c9-9692-3addc8981be1.png"
cover:
  image: "https://s3.amazonaws.com/my-blog-content/2026-06-28--musings-delegation-abdication/2026-06-28-unlock-car-complexity--2c817300-4f22-44c9-9692-3addc8981be1.png"
---

<!-- Write your intro paragraph here. -->
Replying to a coworker's comments about code generation, how it is a necessary trade off between delegation and abdication.


I like that he uses the phrase, for abdicating vs. delegating, that "prompts with explicit intent, drastically improve claud code's  chances at producing quality code," emphasis on "chances".
This is to me  why it's not quite assembly since, compilation is deterministic. More on that later, but begs do question, are you in control?

### Architect and Builder
I also like the architect/builder comparison, because I'm comparing that in my mind with the architect/engineer/contractor relationships in constructing buildings. Architects create design documents, but there are many details they omit like plumbing and wiring that civil engineers typically add when  translating designs into construction documents.  My mom is an architect so funny thing is I have  learned from her how the lines  between those roles are really blurry. When stuff starts to get built there are real world constraints that bubble up. Subtle surprises in the physical elevation can require redesigns. Also money plays a big role, so maybe cheaper materials get used, and structural engineers need to maybe widen beams or add more columns, so architect gets asked to update the design docs too.

All of this I think is to state the obvious that any high level design will miss details by definition, otherwise it would be exhaustive. And this is where actually _"prompts with explicit intent"_ ends up being a contradiction, because when touching bare metal, details get filled in by the model, by playing the lottery.

For example I had this recent example [4] among many where I ask Codex to write a simple function that really can just be a regex and the result is fifty line nested while loop. In some side projects I have attempted to look at the code very infrequently, but when I do, the result is piles of spaghetti code that works just fine.

### Enjoyment
But to the point of defending the "fun part" a bit . Maybe call it the enjoyable part. Dax Raad, creator of the open source answer to claude code, open code, has said that he wants to make the whole developer experience more enjoyable by letting you automate the boring stuff. The productivity gains are high, but isolated to the easy bits. Writing code was never the bottle neck, it was more design, coordination and glue work that coding harnesses don't help with. In other words he says it is easy too  fool yourself that the productivity gains are high, but they are more modest. In an interview [5] he says before code generation he would spend 95% of his time thinking and 5% of his time writing code and after code generation he went to spending 96% of his time on thinking and just 4% on writing code. He sees a hopeful universe is where productivity gains are marginal but people are less stressed out. You can finally refactor your code, keeping tech debt low and even add tests quickly; living the dream!

### That vibe balance?
But going back to not looking at your code, but only when you already know what to expect? Are people really going follow this rule? It can be really tempting to just get the answer really quick because it feels like a nice dopamine hit. Many people self report to not looking at the code anymore. But maybe there is happy medium, enforcable by code harnesses, where you really pair program 50/50, to avoid atrophy to your knowledge? We will have to wrestle with this and people just starting out learning might find it really hard to learn to code from scratch.


### Subtopics also
*Didnt cover yet*
- abstractions and modules are close to what I think code gen might bring us to. 
- Hasn't it all been done before? Why isn't software a "solved problem"? We keep doing it again and again. Is it becausee the devil is in the details?
- compression and gpt as a search engine 
- exectuive teams in companies as an analogy and any kind of management .


## References

1. https://www.pelayoarbues.com/literature-notes/Articles/Dax-Raad-Just-Dropped-the-Most-Honest-Take-on-AI-Productivity
2. https://newsletter.pragmaticengineer.com/p/opencode
3. https://blog.codacy.com/the-creator-of-opencode-thinks-youre-fooling-yourself-about-ai-productivity
4. https://michal.piekarczyk.xyz/note/2026-06-28--a-code-gen-complexity-example/
5. https://youtu.be/1VqKUrxR2C8?t=2736 , Rad Daax on productivity gains
6. Rise of Expert Beginner, https://daedtech.com/how-developers-stop-learning-rise-of-the-expert-beginner/
