---
title: Crowded Wisdom
date: 2026-03-10
---

At a recent team meeting , we discussed the merits of voting on story pointing efforts for story cards. Already yawning! A colleague shared a recent study looking back on jarring counting, and the Wisdom of the Crowds phenomenon. You know, the one where a bunch of people stare at an ox and  influence each others votes about how the ox is heavier than it really is. 

At least thats what this royal society paper studied. That if you are given information about your peers assessmwnts of the ox's weight, you are more likely to discount smaller guesses than larger ones. And they captured a correction factor , which might be handy the next time you are in a situation where you and other people around you are counting gumballs in a jar or group shaming chunky four legged herbivores.

## But LLMs though 
I thought this was oddly loosely related to the smudging, smoothing, blurring effect from GPTs. Through [3], looking yhrough [2], the authors point out that  "mode collapse" observed, from LLMs, getting sort of the middle of the road response when asked for a joke about coffee say, can be countered by asking for enumeration directly. 

I often ask ChatGPT to enumerate trying too, say, for movie or food  recommendations , though I have not tried asking for probabilities, which they suggest directly,

>  “generate 5 responses with their probabilities”

They do go into more detail on the claim that post training alignment (RLHF perhaps) is what contributes to "narrow responses".

But I think the other interesting point in there is not just that you can unfurl the less generic responses but more to the point that LLMs are like governments operating by FOIA. That is, you can get apparently a very large chunk of the text of some of the Harry Potter books to high recall if you just know how to ask your Freedom of Information Act question. The wisdom is crowded.

Lastly, more to the technique around how to inject diversity, this also just reminds me of what I was recently learning in the AI Snake Oil book [4] on weather forecasting. I still remember back in the early oughts (2004, 2008,) when 538 [5] was known for accurately using simulations to forecast elections. So they defined a few knobs , I think this was perhaps the error bars around polling data they aggregated, and they ran tens of thousands of scenarios, of combinations, of where the 50 states swung. Then they used the aggregate of where the electoral vote sums landed to define their presidential outcome likelihoods. The odds. Simulations.

That being a wide epicycloid I realize, --not a tangent right since we are coming back--, that I learned in the AI Snake Oil book that modern weather forecasting uses simulations too . And they noted that the accuracy these days of 6 days, is 1 day better than it was roughly 10 years ago. And more or less they generalize that this has been a per decade trend in improvement. Are they Monte Carlo simulations? I'm not sure, they didnt specify. 




# references
1. the royal society study on numerosity
2. https://arxiv.org/abs/2510.01171
3. https://medium.com/generative-ai/stanford-just-killed-prompt-engineering-with-8-words-and-i-cant-believe-it-worked-8349d6524d2b

4. AI Snake Oil book
5. 538 website , Nate Silver 
 