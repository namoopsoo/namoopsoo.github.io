---
date: 2025-10-13
title: The Data Mercenary
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
What if you are squeezing every bit of entropy out of a dataset and achieving an amazing magic trick.

### on the philosophy of science and engineering
I also saw it recently in this article about rocketry and Elon. 

> "Every time I see Musk, I think of Sagan--because Musk is his opposite. He is a creature not of science but of engineering. He owes his fortune to the brute force of his rockets, and the awe they inspire. There's nothing humble about his manner. Rather than celebrate the fragile, improvised nature of human existence, Musk seeks to optimize or overwrite it- in the name of evolution, in pursuit of profit, in the vainglorious fulfillment of his adolescent fantasies. Where Sagan envisioned cooperation, Musk embodies the triumph of the individual. Where Sagan cautioned against the unintended consequences of technology, Musk charges headlong into the next disruption."


## Also enter here , “To Explain or to Predict?”
(Shmueli, 2011), a paper I had read a long time ago, which came to mind recently, but I realized I remembered only half of the punchline. Originally, I remembered the idea that if you don't have a predictive model, and you can only explain some kind of phenomenon retrospectively, then do you really understand what is going on? Science, is a kind of technology we have developed, that helps us find patterns in data, for the purpose of learning something meaningful, but that can be used practically for the future as well. 

The part I did not remember is that predicting successfully without being able to explain is a perhaps very costly conundrum. 

The question becomes perhaps, if you use machine learning to mine out a pattern, using, say a deep neural net, you have a black box that makes predictions and if you area a business, perhaps you can run A/B tests and prove you are making money from your ML. (And the [booking.com paper from 2019](https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf) contains the super interesting lesson that just because your model is good doesn't mean that it provides business value.)

### Does drift maybe imply your model is not generalizing

A fun realization or epiphany I have also , now, is that in applied ML, the idea of drift and retraining is a very hot topic but that maybe this is literally not just a side effect of distributions changing around you , but of perhaps you not quite building the right model in the first place. So maybe the really highly general models do not require constant refitting because they are not using proxy features that are as affected by drift.

What if alternately, instead of being a correlation machine (correlation learning?), you built a model that was based on something that stood the test of time (rule of thumb learning or common sense learning?) Would we find by extension that most ML is kind of a BS industry , and keeping black box opaque box models around is just the ingenuity by obscurity we didnt notice?

(Of course we know that yes perhaps some systems like our brains are so complex that the behind the eyes reasoning can never be chain-of-thoughted).


### Different kinds of explainability 
Explain or predict or describe
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






## engineering and science 
ultimately, the inspiration for me thinking about this, is, what am I doing? what is the industry doing? perhaps  there really is a need to give names because it reminds me of the old joke, 
> if you talk to candidates, its machine learning , investors , its AI, but in reality youre using logistic regression in Excel  😂




### Shmueli...
It is also interesting though, what does Shmueli mean by explaining ? So she defines "explaining as causal explanation and explanatory modeling as the use of statistical models for testing causal explanations." In her paper she gives the Netflix Prize as an example where the predictive approach shined. That is, the winning model, was chosen by the performance on the held out dataset simply because that is an objective way to choose a winner. But also, the winning team, happened to lean heavily into a collaborative filtering model (nearest neighbor) and therefore the model was more focused on the person doing the rating and whose ratings they are most similar to, but the model doesn't need to know any kind of philosophically deep knowledge about what people like about the movies themselves. In fact the winning team's paper noted that adding metadata about the movies themselves was not additive. Shmueli point out that although the model was an ensemble of several abstract models, we did perhaps learn that the movies being rated as opposed to not rated were more important than the ratings themselves. And that in itself is perhaps a kind of insight.


