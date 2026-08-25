---
title: Req Hunting
date: 2026-08-25
draft: true
---


Maybe Matt Pocock https://github.com/mattpocock/skills , (along with Dax Raad and Peter Steinberger), is someone who sits kind of in the middle of the debate about just how useful agents are for the software development lifecycle.

One one extreme is Steve yegge who is kind of declaring orchestration is here, and you need not, ever look at code again, just express your intent and the swarms will manifest it. There ore many others on this camp. I would like to understand them better.

The other extreme, is total purism, Dont use any A. I. For writing code. Or any part of S.D.L.C. 

In the middle, I think we have people who have tried agentic engineering and realize, as Matt Rocock, has laid out,

(1) you don’t know what you want. You wean what isneeded as you build it. Requirements aren’t gathered, they are hunted. 

(2)  the fog of war is real. Corollary to (1), not only is the design not possible to initially prompt/spec , known unknowns, but there  are also unknown unknowns, not part of the design, but other weird challenges along the way, including low level implementation details that cannot always be looked up but need to be explored. This includes details of the languages and frameworks and databases and APIs and protocols you are using that get in the way. Especially also the data, so data science is about exploring and understanding the dirty data and this is part of that. I would call this the FOIA effect. There are lots of weird nuances that you can often not  know to ask for but if you stumble and trip over them, then you can ask an agent about them and more can be revealed . This includes all the weird bugs and edge cases You must explore that suck up your time.  (There be dragons). 

(3) context engineering is messy. You learn a lot in the process, but you cannot simply just write it into context markdown files into your repository, or at least not once. Just like with any software endeavor, the documentation evolves. This is refactoring. Dax rad points out that agentic engineering is a really good opportunity to keep your code uniform and refactored, to make sure any updates are also clean and uniform. Otherwise an agent may pick up mixed signals, from a mixture of old and new patterns in your code. Before agentic engineering, experienced programmers needed to keep this context in their heads. And task switching of course makes it difficult because you often need to get back to a problem if you had stepped away. So now yes an agent can help you get up to speed faster, letting you ask questions, interrogatively dig into the code, to hope fully get up to speed again if you had to step away, but the context engineering is essentially a new problem that now must be solved that didn’t exist before. 


(4) multi tasking is expensive. Just to pull out the last bit from (3), if you are juggling, it comes at a price . Task switching is expensive both in cache updates in computing, cache misses etc, and in humans too. 

(5) you can’t skip understanding the problem space. This point kind of combines a few of the above points. This is like an analogy I heard from Eric Morrison of YouTube, someone said to him at a meet up, we use technology we don’t understand all the time why not same for software. He said , well it’s true as a user most people  might not understand say a car they  drive but you probably don't want to drive a car but by people who Dont understand cars. Similarly for any domain, you want to understand what is going on to know how to proceed. You can’t offload that. And that’s why you have to be involved not just in prompting and reading or blindly approving PRs . You have to get your hands dirty. You are not only in the drivers seat, you are under the hood of the car, you know what the fan belt sounds like, you con reverse engineer problems you Dont understand! You can figure out problems that ore not described yet. (Fundamentals). 

So in the end it should be asked, I wonder does Matt Pocock discuss how much time has he saved? Does he declare himself a 100x or 1000x engineer like Steve Yegge or is he more measured like Dax raad, who I think basically says you can be a 1.5x or 2x engineer, and reinvest the benefits into a clean refactored code base and good documentation and more Time to deeply understand the problem space and morrr deeply think on  the design you are shaping , which doesn’t necessarily translate into more productivity but just leveraging agentic engineering to get higher quality that you had before and possibly reinvest some of that into less stress for yourself (which Steve Yegge also says actually) . 

## references
1. https://github.com/mattpocock/skills
2. https://youtube-distilled.com/watch/-QFHIoCo-Ko



