---
title: Requirement Hunting
date: 2026-08-25
draft: false
---


I suspect Matt Pocock [1] , (along with Dax Raad and Peter Steinberger), is someone who sits kind of in the middle of the debate about just how much more productive coding agents can make you wrt  the software development lifecycle.

On one extreme is Steve yegge who is kind of declaring orchestration is here, and you need not, ever look at code again, just express your intent and the swarms[4] will manifest it. Or something [5]. Chaos theory be damned. 100x to 1000x productivity is claimed. (Holding my breath?) There are many others in this camp. I would like to understand them better. 

On the other extreme, is total purism. Dont use any A. I. for writing code. Or any part of S.D.L.C. This brought us the internet, the iphone, the ipad, instagram, instacart, indeed, icloud, imac, imagenet, irobot, Intel, IBM, intuit, icelandair, all with individual contributors. Not bad ehh.

In the middle, I think we have people who have tried agentic engineering and realize, as Matt  Pocock and others have laid out, reality presents    a lot of challenges you cant escape.

## Agentic Challenges
My framing of what agentic engineering cannot magically solve , at least for now, borrowing from [1] and other places.

### (1) You don’t know what you want.
You learn what is needed as you build it. Requirements aren’t gathered, they are hunted. 

### (2) The fog of war is real.
Corollary to (1), not only is the design not possible to initially prompt/spec , known unknowns, but there  are also unknown unknowns, not part of the design, but other weird challenges along the way, including low level implementation details that cannot always be looked up but need to be explored. This includes details of the languages and frameworks and databases and APIs and protocols you are using that get in the way. Especially also the data, so data science is about exploring and understanding the dirty data and this is part of that. I would call this the FOIA effect. There are lots of weird nuances that you can often not  know to ask for but if you stumble and trip over them, then you can ask an agent about them and more can be revealed . This includes all the weird bugs and edge cases You must explore that suck up your time.  (There be dragons). 

### (3) Context engineering is messy. 
You learn a lot in the process, but you cannot simply just write it into context markdown files into your repository, or at least not once. Just like with any software endeavor, the documentation evolves. This is refactoring. Dax rad points out that agentic engineering is a really good opportunity to keep your code uniform and refactored, to make sure any updates are also clean and uniform. Otherwise an agent may pick up mixed signals, from a mixture of old and new patterns in your code. Before agentic engineering, experienced programmers needed to keep this context in their heads. And task switching of course makes it difficult because you often need to get back to a problem if you had stepped away. So now yes an agent can help you get up to speed faster, letting you ask questions, interrogatively dig into the code, to hope fully get up to speed again if you had to step away, but the context engineering is essentially a new problem that now must be solved that didn’t exist before. 

### (4) Multi tasking is expensive. 
Just to pull out the last bit from (3), if you are juggling, it comes at a price . Task switching is expensive both in cache updates in computing, cache misses etc, and in humans too. 

### (5) You can’t skip understanding the problem space. 
This point kind of combines a few of the above points. This is like an analogy I heard from Eric Morrison of YouTube, someone said to him at a meet up, we use technology we don’t understand all the time why not same for software. He said , well it’s true as a user most people  might not understand say a car they  drive but you probably don't want to drive a car but by people who Dont understand cars. Similarly for any domain, you want to understand what is going on to know how to proceed. You can’t offload that. And that’s why you have to be involved not just in prompting and reading or blindly approving PRs . You have to get your hands dirty. You are not only in the drivers seat, you are under the hood of the car, you know what the fan belt sounds like, you con reverse engineer problems you Dont understand! You can figure out problems that ore not described yet. (Fundamentals). 

## And?
Im not sure if  Matt Pocock discusses how much time has he saved with his skills. I wonder if  he talks about productivity in multiplier language  like Steve Yegge. I appreciate how Dax is more measured , I think basically saying you can be a 1.5x or 2x engineer, and reinvest the benefits into a clean refactored code base and good documentation and more Time to deeply understand the problem space and more deeply think on  the design you are shaping , which doesn’t necessarily translate into more productivity but just leveraging agentic engineering to get higher quality that you had before and possibly reinvest some of that into less stress for yourself (which Steve Yegge also says actually) . 

## I forgot to talk about Matt's skills 
I think I originally started writing this because the youtube algorithm showed me Matt's video about his wayfinder skill [7]. I was inspired by his framing fog of the of war. 7 have not tried any of his skill files yet, but I suspect his grill me concept is close to what you get from pair programming or poormans pair programming otherwise known as duck programming, or well, Rubber_duck_debugging [8]. 

And i want to learn a bit more about his way finder concept, because i suspect this con be the beginning  of saying bye bye to static planning tods like well, j.i.r.a., and SAFe pi planning . We can rant on the pitfalls of the todo list, but anyway it is about time we continue to evolve it. we started that with the might do list i think. but we can be even more dynamic than that.

## Also, Dexter Horthy's take
Todo, [6], Dexter discusses new thought on Research plan implement, and he also opines productivity gains, can be modest, like 2-3x. 

## And DHH take 
I think DHH take [9] is intriguing. Well any try it was really making lex Fridman laugh out loud quite a lot. Like when DHH said that okay right now the cloude output is so good now, you can trust it and lex says okay so   you just say "i want the code to be secure "and that's all need? DHH saysyes. And lex chuckles. This is a important question because DHH has been developing omarchy, on arch linux fork, with a friend and he hasnt looked at the code. DHH opinion is that these days programming knowledge is a handicap rather than an advantage. Although he does also recount a story of how they at Base Camp recently let loose their product developers on the code to sort of do more releases without the typical product plus programmer combo and after that there was a bit of o mess they needed to clean up. And he also said he is aware if you set the agents go for too long without checking, you get, 01:02:00 ball of mud code.  

So i think DHH raises a lot of good points, but he is still on the fence about the extent of the correctness of the output. But for sure he agrees that planning is bullshit. And in fact he finds the exact same parallels of agentic planning to the  ambitions of software project management that i have been writing about this year. That is refreshing to see!   And he also sees  the  rise of agile in 2000s, as the same parallel to instead the only way he uses agentic harnesses, which is again, like Peter Steinberger, that you can only do this iteratively. Kind of paraphrasing , "No one knows what they want until they play with it. In process of using you discover what you wqnt, whats important, not important " (00:58:00). Completely agree there, but the nuonce is that DHH has also stopped reading the code and he sees the iteration purely as a user experience testing thing. Like Peter too i think. 

And for that last point, thats i think the main difference of opinion, where say Dexter Horthy had that talk [6] literally to walk back earlier statement about only reading plans. He flipped saying no no no please read  the code, the plans are useless. However he also had a new interesting approach as well, kind of alternative to RPI.




## References
1. https://github.com/mattpocock/skills
2. https://youtube-distilled.com/watch/-QFHIoCo-Ko
3. https://github.com/war851/SDLC/blob/main/_foundation/transcripts/2026-06-30-full-walkthrough-workflow-for-ai-coding-matt-pocock/transcript.txt
4. https://michal.piekarczyk.xyz/note/2026-08-15--swarms/
5. https://michal.piekarczyk.xyz/note/2026-07-04-ralph/
6. Dexter Horthy, on, Research plan implement, https://youtu.be/YwZR6tc7qYg
7. Matt Pocock on wayfinder skill, https://youtu.be/F3lL98Pj90o 
8. https://en.wikipedia.org/wiki/Rubber_duck_debugging
 
9. David Heinemeier Hansson hot take, Lex interview, https://youtu.be/NYFGCESmikA 

10. Nate B Jones, on prompt0, doing your thinking before prompting  , https://promptkit.natebjones.com/20260225_hfy_promptkit_1?utm_source=chatgpt.com
11. Lars Faye , "agentic coding is a trap", https://youtu.be/0Kas27lxen4

