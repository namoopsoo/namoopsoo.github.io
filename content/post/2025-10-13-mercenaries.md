---
date: 2025-10-13
title: Data Mercenarialism
draft: true
---

What is science? Does it imply putting knowledge into the public domain? 

A few months back I was thinking to myself about the corporate nature of data science and whether it is true to its name.

And I don't even mean that the majority of your time might be spent on data plumbing, ad hoc data munging or other kinds of analytics that can only be described as story telling with data. 

I mean that if you solve problems using machine learning, regardless of whether the end model affects some internal process or an external one that is customer facing, if you are not contributing to the public domain, maybe these are more like local optimizations? 

A similar conversation has been taking place around the topic of the GPT papers from Open AI. Does the discovery and novel application of scaling laws mean science was done, is what has been discussed for the past few years. That topic likely is a better candidate for the label of science since lots of research has benefited from it and we even have a Nobel Prize in chemistry that came from this research.

But for the topic I'm after here, I'm thinking of work done for a company that doesn't make it into the research space.

### Lets look this interesting recent call to action I saw when using Duck Duck Go.

{{< figure src="https://s3.amazonaws.com/my-blog-content/2025-10-13-mercenaries/image_1760802043881_0.png" width="50%">}}

Here we have the option of either using "search only" or using "search and Duck.ai". Kind of brilliant, because someone has to choose and therefore the resources of an expensive model can be allocated only when needed and you can learn which results have better click through, to perhaps try to measure the value of using Duck.ai. 

I only just recently saw this option come up after probably a year of Duck.ai being available by default and now that I think about it, it was probably being A/B tested at that point. So I would assume that if an A/B test showed that using Duck.ai did not produce a solid justification for increased click through, then presenting it as a choice rather than the default would be a way smarter more cost effective path.

#### But if we are not doing any testing really and we are just cranking out a model?
What if you are squeezing every bit of entropy out of a datast and achieving an amazing magic trick.

### on the philosophy of science and engineering
I also saw it recently in this article about rocketry and Elon. 

> "Every time I see Musk, I think of Sagan--because Musk is his opposite. He is a creature not of science but of engineering. He owes his fortune to the brute force of his rockets, and the awe they inspire. There's nothing humble about his manner. Rather than celebrate the fragile, improvised nature of human existence, Musk seeks to optimize or overwrite it- in the name of evolution, in pursuit of profit, in the vainglorious fulfillment of his adolescent fantasies. Where Sagan envisioned cooperation, Musk embodies the triumph of the individual. Where Sagan cautioned against the unintended consequences of technology, Musk charges headlong into the next disruption."

#### Explain or predict or describe
...


Guess im misinterpreting but in the social determinants of wealth example , how does age, address, race, background occupation contribute to annual income, that still sounds predictive not explanatory. Just because its a regression model you build doesnt mean it cant be used to predict income and be evaluated by say RMSE. 

I suspect that yes we dont need to know why beta blockers work, that is, theory not required, then im using the word "explain" in a lay way and it probably has a formal technical meaning i dont know . Just like "theory" has both a lay and technical definition. 
....
I found this line from Shmueli's paper that in explaining online auction final price prediction models, the authors used R^2, the coefficient of determination , "determine explanatory power", but that s kind of sillg because that's literally correlation and not causation 😂😂😂. 

I dont understand why Shmueli didnt criticize this.

Then again, I dont really know yet what is a proper way to prove causality 
...
Oops, i think i figured it out. R^2 is used for a different kind of explainability, kind of like I suspected. 

R^2, shows a model has "explanatory power" not if is interpretable , but if "the model can explain most of the variance in the data". 


