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

(2)  the fog of war is real. Corollary to (1), not only is the design not possible to initially prompt/spec , known unknowns, but there  are also unknown unknowns, not part of the design, but other weird challenges along the way, including low level implementation details that cannot always be looked up but need to be explored. This includes details of the languages and frameworks and databases and APIs and protocols you are using that get in the way. Especially also the data, so data science is about exploring and understanding the dirty data and this is part of that. I would call this the FOIA effect. There are lots of weird nuances that you can often not  know to ask for but if you stumble and trip over them, then you can ask an agent about them and more can be revealed . 

(3) context engineering is messy. 