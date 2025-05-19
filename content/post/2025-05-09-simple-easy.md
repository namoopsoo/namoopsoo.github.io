---
title: simple made easy
date: 2025-05-09
---

drafting...

2025-05-10 Simple Made Easy, Richard Hickey talk, take aways, 

Listening to this presentation, from the frame of why do codebases get difficult to change , but also how you plan changes you want to make on the scale of a "story" or "bug" and also just a "day" and even a single block of time you have for a particular story. The definition of simple as simplex as one interleave and less simplex as more "concepts" that are taken tofjgether to be more "complex".  

So ultimately your "workijg memory" or "cognitive load" in dealing with thing is at stake here. The complexity will determine how much time it takes to get into "flow". And it may even directly answer Scrum questions like "how many story points is this?" Though I am more curious about whether  you  can prove "story-pointing" is actually a useful exercise . But maybe depending on the "number of concepts that need to be taken in at once," can help steer whether "estimation" is more or less accurate.

Additionally, fighting the good fight against entropy , letting code sprawl or complect , swallowing many areas of concern, complecting the "how" and "what" and "when" feels like a LLM "context window" question too. When will the Chat GPTs, the Cursors, the Windsurfs, Codeiums , be able to help disentangle your code, and help you with a refactor? 

While going through this, I had been also watching the Ken Burns story about Mark Twain, who produced thoughts so coherently, so simply, it helps me aim for simpler words in all writing, code or verse. 

Hickey has a poijt about jugglers. How many pins or balls can a really good juggler juggle? He argues, probably most people are working with similar limitations. And I wonder what would Michael Stevens of Vsauce , who created a very thought provoking , very Zipfian video on entropy and combinatorics, say on such shared limitations of language itself. And here Gary Marcus, Stephen Pinker, Noam Chomsky, see language as a "instinct" yes and that we have some machinery we have evolved to be born with. But yea, is the limitation in what you are conveying, in code or in spoken words, or written words, tied to intrinsic mathematical limitations. 

All this also of course made me try to understand writing style too, wondering say, is it better to write as "Breadth First" or "depth first"? Conversations are neither interestingly. Conversations are like walking a Graph, meandering , in a non-tree algorithm. Technical articles are probably best as BFS, laying out the stage first, tgen diving down one layer at a time, perhaps covering subtrees as well.


Didnt get to yet the Freakenomics Sludge epieodes yet either. I feel like I have to just lay out all the related concepts first. Then try to attack chunks.

Maybe most intriguing aspect, is the relationship between how you feel and the number of items you attempt to juggle. A moment can be chaotic when you are weighing multiple concepts of consequence. I remember I had a friend in college who said to me she would write down her work in solving a problem, writing out loud, and I recall being and at first confused, dont you want to be clever and try to keep the steps in your head. But I think trying to hold too many details only leads to frustration, especially if this is unnecessary. 

Holding more ideas in your head than necessary is no more clever than attempting to use esoteric words with the aim of sounding smart. Both result in confusion. One on your part, other on the part of your audience. Maybe thats why jokes are so useful, because they allow you to hack another's brain into revealing the owners emotional state to you.

Ultimately I hear Hickey's point about this and I think that less is more applies here.
I was just riding my bike today and realizing how at peace I felt. And it was because I only had what was in front of me to negotiate. 

...

## Modulariztion and Simplicity
More to Hickey's technical points on complecting. So he says, 

> "dont be fooled by code organization", 

in you can have this neat class code layout, but complecting comes down to ,

> "what are they allowed to think about?"

Classes may appear separate but they may not separate concerns and are coupled (aka complected) by what one class knows about another class's internals.