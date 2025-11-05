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


## Also enter here , “To Explain or to Predict?”
(Shmueli, 2011), a paper I had read a long time ago, which came to mind recently, but I realized I remembered only half of the punchline. Originally, I remembered the idea that if you don't have a predictive model, and you can only explain some kind of phenomenon retrospectively, then do you really understand what is going on? Science, is a kind of technology we have developed, that helps us find patterns in data, for the purpose of learning something meaningful, but that can be used practically for the future as well. 

The part I did not remember is that predicting successfully without being able to explain is a perhaps very costly conundrum. 

The question becomes perhaps, if you use machine learning to mine out a pattern, using, say a deep neural net, you have a black box that makes predictions and if you area a business, perhaps you can run A/B tests and prove you are making money from your ML. (And the [booking.com paper from 2019](https://blog.kevinhu.me/2021/04/25/25-Paper-Reading-Booking.com-Experiences/bernardi2019.pdf) contains the super interesting lesson that just because your model is good doesn't mean that it provides business value.)

A fun realization or epiphany I have also , now, is that in applied ML, the idea of drift and retraining is a very hot topic but that maybe this is literally not just a side effect of distributions changing around you , but of perhaps you not quite building the right model in the first place. So maybe the really highly general models do not require constant refitting because they are not using proxy features that are as affected by drift.


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


## engineering and science 
ultimately, the inspiration for me thinking about this, is, what am I doing? what is the industry doing? perhaps  there really is a need to give names because it reminds me of the old joke, 
> if you talk to candidates, its machine learning , investors , its AI, but in reality youre using logistic regression in Excel  😂




### Shmueli...
It is also interesting though, what does Shmueli mean by explaining ? So she defines "explaining as causal explanation and explanatory modeling as the use of statistical models for testing causal explanations." In her paper she gives the Netflix Prize as an example where the predictive approach shined. That is, the winning model, was chosen by the performance on the held out dataset simply because that is an objective way to choose a winner. But also, the winning team, happened to lean heavily into a collaborative filtering model (nearest neighbor) and therefore the model was more focused on the person doing the rating and whose ratings they are most similar to, but the model doesn't need to know any kind of philosophically deep knowledge about what people like about the movies themselves. In fact the winning team's paper noted that adding metadata about the movies themselves was not additive. Shmueli point out that although the model was an ensemble of several abstract models, we did perhaps learn that the movies being rated as opposed to not rated were more important than the ratings themselves. And that in itself is perhaps a kind of insight.


## epiphany reading the google swe culture book


ok I found it , https://abseil.io/resources/swe-book/html/ch05.html the chapter on tech leads and engineering managers.

ok I kind of had this intuition about the way my current company runs projects is spineless and reading a bit of this online book, I think I'm on the right track.

In my past companies , the way of getting work done is that each person would basically be part of small execution teams (2 or 3 people) and each team would just work on basically one project several days at a time. The mini teams just organically divide up the work and just collaborate super organically. And you just talk to your boss basically whenever you got super excited about something you want to show or when if you held off too long , your boss would tap on your shoulder to see what's up haha.

Yea and instead my current team does Scrum and it is shoved down everyones throats from the top of the company. It is terrible. It is like "leadership by backlog" . My team has a so called Product Owner but this person literally is not a team player, very judgemental, extremmely insecure to criticism, always sounds condescending , never contributes any insights or opinions into a conversation unless it is to sound as if speaking from some high mountain top of authority.

All they know how to do is just hide behind their backlog and just sound very agitated whenever people dont acknowlege items that have been placed into each sprint backlog. But this person never asks for feedback. ever . And boy do they love the PI Planning . We did the pi planning thing , everyone participated hoping it would finally be a team effort, and then at the end this product owner person they just rearranged everything , putting their own preferred projects at the top but they were actually doing it while sharing their screen haha so we had a kind of embarrassing moment and we said hey what are you doing , we literally just spent two days doing this team thing and now you are just deciding everything; what the heck was the point of all that if you wre just going to change everything last minute.

Terrible human. Anyway, actually I suppose I shouldn't blame this person, instead I suppose Scrum and SAFe gave them this weird mission of lead-by-backlog and that is kind of what they are spinelessly doing. And I really love reading this Google SWE culture document because it reminds me of the good old days of working projects at past companies .

