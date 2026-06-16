---

title: Whisperware   
date: 2026-06-01
---

Trying to see have I wfitten about this before, but weve had data scuence for a while , where given domain knowledge, programming knowledge, and some maths, you can iterate towards data science (just kiddijg thats a blog). You can iterate towards a model that fits your data and generalizes modestly on unseen data. Then we entered  ML  engineering, where  you lean into the formal aspects of rigorous testing and more into the repeatable, so less trial and error perhaps. 

In both of the above cases it is data in , code out. This was meant figuritively, as runnable code but not readable code. You cant read a billions of neural net weights any more than you can read a binary compiled program.

Next, AI engineering tries to keep it formal but perhaps widen , to buildijg with foundation models perhaps. 

And now we have entered into something like agentic engineering, where theoretically the work output is still code, but this time it is readable and the input is no longer clean data but just text, or prose. But it is still highly iterative like the OG data science.

I was initially confused about spec driven development until I saw it was still basically prompted, but with the air of declarative programming ; just say what you want and you will get it. Except of course you cant precisely say what you want in English, and so spe. driven development lets you provide tests that need to pass. 

Others also (grill me?) go the route of get more detailed with the prose. And others double into the bqck and forth Uswr Acceptance Testing like somw flavors of Claude.

So a few approaches  . Ah maybe I did touch on this in another blog post wrt the similarities to halting problem. And to the no free lunch theorem . Right. I think essentially unless you can "distill" fully , a problem domain, cheating at being "declarative", you will be iterative. Smoke and mirrors fade away. You are no longer doing engineering and we are bqck to science qnr trial and error. A Software Science if you will. Quite soft . maybe lower your voice. How about Whisper Science. Whispware Science? Whisperware ?

 
But what are tests that are provided through the spec ? Thats what you can call the training data. Cool, but we want to generalize, so whats the test data?

Hmm maybe that could be an interesting idea, you leave some tests out ? Test for generalization that way?

Why not one shot the work  ? Sure YOLO , Im feeling lucky, do it live. Hold out generalizability is 
 a false sense of a guard rail right? Though in god we trust all else bring dqta. Where did thqt go?

I totally agree, like Richard Hickey said in that Simple Made Easy talk, your guard rails are not where your bugs lie, the ones you dont know about cannot be predicted and tested for by definition. (this is the metaphor where you see a person looking for their car keys next to the street left because that is where they are able to look because there is light) (Not to mention real life kicks your butt too). 


## Code Mouth Feel: Readability?
One small update here I mentioned earlier above that with Whisperware  you have code that is readable, but is it though? there has been a growing number of people who call the new code that is generated more like neural code because you cannot really understand what is going on. sometimes it's more like the RLVR will control for a code that is working but not yet for code that has a nice mouth feel.

maybe there is room to optimize also for readability. That may be measured using something like cycloMatic complexity.

### Why is readability important? 
Because 80/20 rule, you dont need to look at the code, well, until you do. Discussion of this also here, [1], [2].

## references 
1. https://youtu.be/dicToifZBxw?t=950 Mo Bitar 
2. https://x.com/mitchellh/status/2066657032938442833 , Mitchell Hashimoto 




