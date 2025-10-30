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

## Cal Newport 

Adam Grant, https://link.chtbl.com/4HaHYkSm

and Slow Productivity, surveillance productivity, Kanban Cage


## also, Martin Fowler
Product vs Engineering, https://martinfowler.com/articles/bottlenecks-of-scaleups/03-product-v-engineering.html

my notes: "2025-10-23_0837--0400"

Wow this is written well, says what I didnt really realize what I wanted to say, that there are basically two backlogs, product backlog and engineering backlog.

But on our team problem is deeper that our product backlog isn't even  for customers its for the devops team. some  referring to an adjacent concept of buckets also.

My thing has been, Im realizing, our Product Team is not accurately representing the product interests , not engineering interests either, so its no taxation without representation I think  . You cant have a PI planning meeting if it doesnt accurately represent all the interests at play.

That , lack of representation has been a problem in our OKR meetings too, wrt, top down and bottom up OKRs.

And whqt ends up happening, people in a PI planning meeting are coerced , under duress, even recorded , to sign with blood as we joked , agree, commit , without a full review of phoenix, technical backlog, tech debt, etc.

Only mentions in Pi planning are the MLP Support, which is bullshit because then you just only have time to fix broken shit without preventing , making stuff more resilient. 

quote, 
> "Us vs them", and product leaders throwing requirements over the wall, treating engineering team as a feature factory. 


quote
> When product and engineering organizations aren't communicating or collaborating effectively during product planning, we tend to see an imbalanced investment mix. This can mean the product backlog leans more heavily towards new feature development and not enough attention is directed toward paying down technical debt.

Hmm though yea im leaning more towards Shane De La Moore that this is got to be internal , precisely why PI Planning is not the fit for our team. Basically, here are the two choices: (1) either we have a fully unified team where everyone is fully represented. And perhaps we can have a board we share with product, because it is just our product. No us vs them 

(2) us vs them isolation, so engineering team has its own lead and its own board and negotiates the various deliverables , and handles its own tech debt decisions etc, balancing.


### Product is cool
This article goes into depth about cool ways to unify the team, get excited about product. 

We are sorely missing this . Again, just mainly doing random garbage work inherited from Devops .

Outcome oriented team, vs our activity separate. 

### Backlog negotiation 

The PI planning thing totally missed this mark. that we forgot to negotiate 





