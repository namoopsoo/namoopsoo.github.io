---
date: 2025-10-13
title: The Data Mercenary
draft: false
images:
  - "https://s3.amazonaws.com/my-blog-content/2025-10-13-mercenaries/IMG_6381.jpg"
cover:
  image: "https://s3.amazonaws.com/my-blog-content/2025-10-13-mercenaries/IMG_6381.jpg"
---

What is science? Does it imply putting knowledge into the public domain? How about learning something? Did you need to learn something? Do you need to prove what you find?

These are some of the questions going through my head a few months back. Given the corporate nature of data science, is true to its name, or is more hype to attract candidates?

And I don't even mean that the majority of your time might be spent on data plumbing, ad hoc data munging or other kinds of analytics that can only be described as story telling with data. 

I mean that if you solve problems using machine learning, regardless of whether the end model affects some internal process or an external one that is customer facing, if you are not contributing to the public domain, maybe these are more like local optimizations that don't generalize rather than "science".

A similar conversation has been taking place around the topic of the GPT scaling law papers from Open AI. Does the discovery and novel application of scaling laws mean science was done, is what has been discussed<sup>[1](#references)</sup> for the past few years. That topic likely is a better candidate for the label of science since at least there is a Nobel Prize<sup>[2](#references)</sup> in chemistry that came from this research. And this is while the theory side is still fuzzy. 

But for the topic I'm after here, I'm thinking of work done for a company that doesn't make it into the research space.

### Lets look this interesting recent call to action I saw when using Duck Duck Go.

{{< figure src="https://s3.amazonaws.com/my-blog-content/2025-10-13-mercenaries/image_1760802043881_0.png" width="50%">}}

Here we have the option of either using "search only" or using "search and Duck.ai". Kind of brilliant, because someone has to choose and therefore the resources of an expensive model can be allocated only when needed and you can learn which results have better click through, to perhaps try to measure the value of using Duck.ai. 

I only just recently saw this option come up after probably a year of Duck.ai being available by default and now that I think about it, it was probably being A/B tested at that point. So I would assume that if an A/B test showed that using Duck.ai did not produce a solid justification for increased click through, then presenting it as a choice rather than the default would be a way smarter more cost effective path.

#### But if we are not doing any testing really and we are just cranking out a model?
What if you are squeezing every bit of entropy out of a dataset and achieving an amazing magic trick.

### what does science do to answer questions

#### Thank you for not smoking
The hazard ratio and smoking :
How did science convince the world that smoking is bad?

Back in 2001, the case of United States v. Phillip Morris began around a charge of conspiracy to hide health risks about lung cancer and second hand smoke, hiding them from the public. The statute under which conspiracy was argued was the so called RICO, Racketeer Influenced and Corrupt Organizations Act. The prosecution had to demonstrate that Phillip Morris knew about the risks, and publicly denied them and manipulated marketing, claiming that light cigarettes were low tar and were lower risk. This was fraud, by the definition that they knew the risks but they were still applying marketing saying the product was fine. By 2006, the case was won and appeals to the supreme court were declined. The injunction required Phillip Morris to clarify the harms in the marketing and packaging.

But in order to prove the fraud, we needed the initial evidence that the harm was present. By 2001, the harm was already well established. Actually, by 1964, the Surgeon General already formally reported that smoking causes lung cancer. There were two major epidemiological studies in the 1950s that contributed the evidence. One was the British Doctors study where 34,439 british physicians had a 20x higher lung cancer mortality than non smokers (Doll & Hill 1951). 

The hazard ratio of 20x here is not strictly evidence of causality, meaning that, we are not looking at the bodies or lung tissue and we are not monitoring what the smoke is doing. This study does not know for sure what is the biological pathway that causes the outcome. Also the first 1954 set of numbers published was just an early indicator, since aftre the first 29 months, out of 34,439 doctors, there were only 36 lung cancer deaths, though the ratio was high, 34 smokers to 2 non smokers. 

At this point you might also think, but why would there even be any non-smokers in the lung cancer death group? But the thing is, there can also be confounders such as second hand smoking as well. Also environmental factors can contribute, such as say air pollution. But interestingly, we don't look at any of this in the published studies. The assertion is that the relative ratios of prevalence is strong enough of an association to be submitted as proof.

There were also follow ups after 20, 40 and 50 years. 

By year for the 20, 34,439 men, there was a somewhat stable per-year relative risk of lung cancer death of 17 to 1, with 170 to 10 smoker to non smoker lung cancer deaths. And the quantities were also stratified across several buckets of 1-14 cigarettes per day, 15-24, and 25+ and the 25+ group had the largest relative risk of 21.0.

A 91 year old Doll actually published the 50-year study in 2024 and the numbers were consistent at ~20x in smokers. However, these were more modern times, and this longitudinal study also tracked men who had quit smoking in their 30s and all their excess risk was gone. And those who quit in their 50s halved their risk.

So there were no lung autopsies as part of these longitudinal studies, but the numbers were what was presented. And by being a longitudinal study, the rate of lung cancer death per year per 100,000 is what was compared between the smoking and non smoking groups and that rate remained fairly consistent in the 170-210 range throughout the 50 years. 

So one might also say that no not all of the smoker cohort died with lung cancer but also, there were still 9,000 men alive at year 50 and there were also many other kinds of mortalities that were not lung cancer but related, such as COPD and heart disease, but these are precursors to lung cancer and therefore one might say that had they survived longer they would have faced lung cancer as well and that the hazard was therefore likely underestimated.

Still all that being said, we know that hazard ratios are not the gold standard when it comes to science. That honor goes to randomized controlled trials.

#### What does a RCT look like


The reason I became interested in some of these topics was because of diet science. But is it science? Food studies are overwhelmingly animal based but they are RCT. Human ones are survey based. But as Doctor House knows , everybody lies. 

The ad libidum feeding study with processed foods. actual people. Actual science? Sample size? 

This study was indeed an RCT and over a multi week period , ad libidum calorie consumption was compared and measured as 500 greater in the processed food group.



#### Reprodicibility? 
The area of social science has lately had a blow to confidence with some (a) reproducibility problems around the Extra Sensory perception thijg, (b) p value 5% , gotten questions past decade, (while Higgs boson more precise , God Particle), (c) and Harvard studies , hmm tampering? (Atlantic article). 

So the Harvard one, Franchesca Gino , 
https://www.theatlantic.com/magazine/archive/2025/01/business-school-fraud-research/680669/ , this professor doing research into honesty,  but four papers published and data anomalies were described. 

The Atlantic article author took one of the studies in question and inspected the data to better understand what the perceived data tampering might be about. The study was called “Don’t Stop Believing: Rituals Improve Performance by Decreasing Anxiety,” and was trying to show that performing rituals could help reduce anxiety prior to doing something that provokes the anxiety. This could be something like public speaking and the rituals can be just anything arbitrary that you (I think I heard Wayne Gretzkey was known to wear a lucky pair of underwear or something like that). And the anxiety was measured using a pulse oximeter to check heart rate. The problem was that , as the Atlantic author shows, although the heart rate data looks normal for the first two readings recorded, it looks very weird and suspicious for the third one. 

The paper had 7 authors and Gina was listed as number 4. Without yet going into the culpability, just first thinking about this study, you just want to know , what happened? If someone looked at the data they would be able to wonder was it fudged. But was the point of view just naivetei like no one will notice? And that this was right before a submission deadline? And maybe some of the original results were perhaps lost and itwas too late to redo all of the data collection, so lets just put some numbers in that kind of fake it?

As a personal anecdote, I want to recollect a story I remember very well from when I was in 5th grade. I had a teacher who taught me a lesson I keep very close to my heart. I had been moving around schools a handful of times and at one point I had an assignment to hand draw the animal cell and all of its parts, including the cell membrane, the mitochondria and all of the vacuoules that clean up unwanted particles in the cytoplasm. I remember I got a really good grade. I always liked drawing so I was pretty proud of this. A year later, I moved schools and I happened to get the same assignment from a different teacher. I don't know what was going through my 10 year old brain but I decided to pencil erase the date and fill in the current date and hand in the drawing I had made prior. My teacher Ms Geary confronted me about this and asked me I think to redo the assignment. This shame, I somehow still remember so many decades later but I am ever thankful for her lesson because I realize writing this, it has shaped my belief in high integrity and quality to this day. So I think that reproducibility is a very important topic and any kind of tampering, even to harmlessly save time if the result would have been the same so you suspect, is not ethical and should be explicitly written out. 

The case is made best by Balaji Srinivasan. A point of view I think is easy to get behind and might help to avoid the various levels of junk science out there.


#### job market

Economists trying to interpret job data, https://www.stlouisfed.org/on-the-economy/2025/aug/is-ai-contributing-unemployment-evidence-occupational-variation

Contrast with Big Short , Christian Bale real life speculator, put your money where your mouth is? What would the Edge Institute hedge hogs and foxes guy say? What would Nate Silver , 538 guy say? The model that didnt predict Trump but was good up until then?

#### hmm
So the label science doesnt always mean the same thing.

### on the philosophy of science and engineering
I also saw it recently in this article about rocketry and Elon. 

> "Every time I see Musk, I think of Sagan--because Musk is his opposite. He is a creature not of science but of engineering. He owes his fortune to the brute force of his rockets, and the awe they inspire. There's nothing humble about his manner. Rather than celebrate the fragile, improvised nature of human existence, Musk seeks to optimize or overwrite it- in the name of evolution, in pursuit of profit, in the vainglorious fulfillment of his adolescent fantasies. Where Sagan envisioned cooperation, Musk embodies the triumph of the individual. Where Sagan cautioned against the unintended consequences of technology, Musk charges headlong into the next disruption."

#### Data science has been a pain in my neck
Disclosure, this topic has given me some imposter syndrome over time. And so I have a personal stake in thinking through these questions.

On this side personally I come back to how Charles Isbell phrases this. And he brings us back to Computer Science that predates Data Science. Halting Problem, Turing completeness, P v NP. 

#### Hot dog not hot dog
Deep learning , cats , Google, Casey's Genius Makers book. We have a Turing Award  . What are the contributions and what does it add to science?

#### That diagram , about all of knowledge, and the Phd, 
is this tiny finger poke, protrusion, the frontier.

But how about the Francois Chollette , exponential growth publications and linear progress still? Quantity , Quality?


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


## Engineering and science 
Ultimately, the inspiration for me thinking about this was personal. That is, what am I doing? what is the industry doing? perhaps  there really is a need to give names because it reminds me of the old joke, 
> if you talk to candidates, its machine learning , investors , its AI, but in reality youre using logistic regression in Excel  😂


### Shmueli...
It is also interesting though, what does Shmueli mean by explaining ? So she defines "explaining as causal explanation and explanatory modeling as the use of statistical models for testing causal explanations." In her paper she gives the Netflix Prize as an example where the predictive approach shined. That is, the winning model, was chosen by the performance on the held out dataset simply because that is an objective way to choose a winner. But also, the winning team, happened to lean heavily into a collaborative filtering model (nearest neighbor) and therefore the model was more focused on the person doing the rating and whose ratings they are most similar to, but the model doesn't need to know any kind of philosophically deep knowledge about what people like about the movies themselves. In fact the winning team's paper noted that adding metadata about the movies themselves was not additive. Shmueli point out that although the model was an ensemble of several abstract models, we did perhaps learn that the movies being rated as opposed to not rated were more important than the ratings themselves. And that in itself is perhaps a kind of insight.

## AI told me to do thqt

The algorithm is tearing us apart? Influencing elections and not just Explqin Predict Describe, but Influence? (The Social Dilema Tristan Harris?)

## Explain like Im 5
Is The explanation and rational thought is mysterious or is it.. rational? I remember there was this fun podcast series called Reply All, where in a segment  yes yes no , (https://en.wikipedia.org/wiki/Reply_All_(podcast)), PJ Vogt and Alex Goldman explain to , Alex Blumberg, internet trivia memes.

Explaining what happened , explain a meaning of something. You can also have something like a proof in math. And some proofs take a very long time, Fermat Last Theorem. ( incidentally someone I know recently telling me they knew and met Andrew Wiles ... ). 

Is the bar for a good explanation, more or less causality? Do we all intuitively know correlation is not good enough? (smellt it dealt it), is this Occam's Razor? 

Going back to court, we also have the legal system where a guilt model is constructed using your peers, sampled from the jury pool. Different crimes require different burden of proof, where sometimes, witness testimony works, but DNA evidence didn't exist before and murder was still taking convictions. But juries are not statisticians though they are instructed to think critically and use only the evidence presented. And not what was "wiped". Witness tampering can result in new jurors or even a mistrial.

We don't know what happens in the jury deliberation room, we don't know if each jury member is required to explain in their own words their understanding of what happened. They are not asked to take a test to verify they understand the facts. Probably because those charged have a right to a "speedy" trial.

Yet tests are one thing close to what we use to validate a model and we do to humans too, to students, specifically. Yet, many can *testify* that book smarts and street smarts are not quite the same. (in the practice in theory are the same, but not in practice, as they say).

and when models drift, we just retrain with new data, and move on. 

Of course even a really good explanation can turn out to be a trick, as often a illusionist will demonstrate with a slight of hand or a ventriloquist with their various illusions. We all love a good detective story in a film, where twists and turns in a who done it cause you to keep changing your mind about the rank order of suspects. (Netflix had a good series like this recently. Also the Knives one). You keep changing your mind but thats what makes the illusion so delicious!

In the end we call it a fair trial. 



## Surely you're joking mr Feynman
I remember when I was in college, one time I sat at a public lecture by Brian Green about quantum mechanics, where I learned that although it is a field with the highest ability to predict phenomenon with accuracy, it is still not clear what is actually happening. Afterwards I went on to listen to Feynman's lectures. He 

> “I think I can safely say that nobody understands quantum mechanics.”
so basically you think you understand QM, you probably don't understand QM. And I suppose if available, would his reasoning be simply that it is not like the physics of gravity or springs or other classical phenomenon that are easier to relate to. and so the absence of an analog means you can only approach QM mathematically and perhaps metaphorically. For example, how could you possibly understand intuitively the double split experiment .

Although a few months ago, I was digging into the Many Worlds Interpretation of QM lectures of the Mindscape guy. I think MWI does does sort of nicely explain that a photon will be following the universe's hilbert space and wen will see its wave pattern on the opposite wall of the double slit but when it decoheres, it is simply entangling with our branch and that there is another branch of the universe where a different photon is entangled with of a different slit pathway and that perhaps does have some mystery resolution .

But still it is not a classical explanation. And another Feynmanism apparently was, "shut up and calculate." 

And so I think ultimately back to deep learning and similarly Feynman would have been perfectly fine just calculating. Maybe it is fine that there are no amazing interpetations of black box models. Trying to make them interpretable can be a distraction. 

Of course that doesnt mean black box ML should be used unfairly. It is argued by Cynthia Rudin, in particular<sup>[3](#references)</sup>, that only interpretable models will help us to avoid the ethical conundrums that plague our society--*also famously discussed by Cathy Oneil of Weapons of Math Destruction<sup>[4](#references)</sup> fame*.

## A descriptive example: Aphantasia

After starting to read a New Yorker article recently, Phantasia, on the study into the spectrum of how much or how little, different people are able to view imagery in their minds, I also on the side, read a bit more of the intro to the Gregory Hays Meditations translation<sup>[5](#references)</sup> . Hays helps the reader understand more of Marcus Aurelius's world before they dive into the text. And he discusses the three stoic disciplines of perception, action and will, and that perception is how you accurately or inaccurately interpret what you observe. And what you observe, in its raw state, is the "phantasia".  And then the next day, I went back to reading the New Yorker article, where I read about the Scotish neurologist, Adam Zeman, who (later on) coined the term "aphantasia", related to what he learned about a patient, Jim Campbell, who apparently lost his ability to visualize in his mind, after a cardiac procedure, while in his sixties. Zeman goes on to publish on a brain imaging study he runs, comparing Campbell with a control group of other men of close age, who can generate images in their minds. He publishes this in the journal Neuropsychologia in 2010. And after studying a total of 21 subjects, he published again, this time in Cortex, in 2015.

A while back, around 2014, I picture a memory I had, of carefully walking the stairs in a Bushwick apartment I had moved into, while I was thinking about just learning about the benefits of epedemiology. Before, I had assumed it was more or less just faux science, but I was having the kind of epiphany that it is the beginnings of an understanding. My context, was in learning about how most diet studies in humans are very much retrospective and obesrvational. I thought earlier that, they are not very useful because they are not the gold standard of the so called randomized controlled trials. I thought to myself, a humbling thought then. What  I had read was that epedemiology is required in order to start seeing the direction of some kind of relationship, before you can later get the funding in order to perform a RCT.

What contributed to Campbell's aphantasia? Was it his cardiac procedure or something related to his age? Maybe we will not know, but after Zeman published his second paper, there was an article about it in the New York Times and seventeen thousand more people emailed him. Zeman started learning about people who were born with this condition, more also who developed it after inury and he also learned about a kind of hyperphantasia, of people with extreme ability to visualize, who can sometimes confuse their imaginings with reality. One hyperphantasic reported walking into many walls, imagining there were doorways present.

I suppose one of Shmuli's points in writing her paper was not that purely explanatory modeling is not useful without being predictive and not that highly predictive black box models don't reveal enough about the world in which they interact, but that perhaps you need both as you are making sense of the world around you. 

And maybe while you are only able to build a correlation machine that helps to solve a business problem, but only for perhaps a few months or only a year until it starts suffering from covariate drift or concept drift, perhaps that's fine if say, this helped you, say, make or save money that you can hopefully later use to invest in better understanding the actual underlying phenomenon.

But also perhaps sometimes it is also fine to do as Feynman says and just *shut up and calculate*!


# References
1. https://www.reddit.com/r/MachineLearning/comments/r76igz/discussion_rant_most_of_us_just_pretend_to/
2. https://www.nobelprize.org/prizes/chemistry/2024/press-release/

3. Cynthia Rudin, https://arxiv.org/abs/1811.10154 , Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use Interpretable Models Instead
4. Cathy Oneil weapons of math destruction

5. https://store.dailystoic.com/products/meditations
