---
date: 2026-01-19
title: how-to-make-cake
---

Started reading, preview, AI Snake Oil. Reading retelling of what a developer Thomad Ptacek received from ChatGPT about how a biblical verse would explain removing a peanut buttee sandwich from a VCR.

The below  makes me think of the Russel Peters standup routine where he demonstrates how a particular man would stereotype explain how to bake a cake. 

> "Fear not, my child, for I shall guide thy hand and show thee the way. Take thy butter knife, and carefully insert it between the sandwich and the VCR, and gently pry them apart. And with patience and perseverance, the sandwich shall be removed, and thy VCR
shall be saved."

In other words, mildly entertaining?  , highly confident? useless? sure let's pick all three 😂.

But in this case, as far as the societal implications suggested, we're talking biblical proportions!

Also what comes to mind was this bus I noticed, during covid times, 

{{< vimeo 785843804 >}}


## crisis of replicability
p 23 Preach! Several examples of flaws in ML models and attempts to address them in research falling on deaf ears. hmm "self-correction" is the preference? 

Reading many examples, including a "next music hit" predictor that failed to separate train test split validation. And a "has covid" predictor where positive and negative examples were split evenly as children and adults so models just learned "is child" insteaf of "has covid". Wow

## lack of AI product audits
p24 hiring: 
Pymetrics, HireVue, in the dog house: no public audits for "does it work?" only for "are the models biased w.r.t. demographics. 
  
p25
Sounds like FTC has stepped up in 2023, noticing unjustified claims on AI products. Cool, that is their wheelhouse.

p26 Social Sentinel: student ptotest surveillance disguised as threat detection, oops.

## Retention models
p36 , crazy story about University Mount St Mary's, using a retention model, not to help people succeed but to identify students likely to drop out and get them out early before they hurt the school's statistics.

But wouldn't it at this point be more fair to say clearly any technology can be used for good or evil,  before we even understand if this model was accurate or not.

And going even deeper, the fact that university retention rates get tracked like this might not be great either and end up creating the perverse incentives we see.

## Misleading predictive power
p44 Crazy example of a model helping to predict complications risk after having pneumonia, in releasing patients after treatment. The authors worked with other researchers and noticed that although the model, was predictive, it was also associating asthma with a lower risk of complication. And they discovered the reason was the training data was not representative of a typical population. In fact, patients with asthma, part of this dataset, had received additional ICU care, reducing their risk for complications.  I suppose we still don't really know what was it about their increased care helped actually lower their risk to below the non-asthma population, but perhaps their stay was even extended so they had longer observation time to understand and treat any additional problems prior to their release. 

In any case, that was a dramatic example, which could have been prevented by inspecting drift of feature distributions of the training data and fresh data. And that would have thrown this model right out.

I wonder how often are the examples in this book about skewed training data. And just after writing that, I noticed the next example was another such bad training data example. This was a model predicting hypertension. However, I'm reading that having existing drug treatment for hypertension ended up being a strong model input and the evaluation set used was with people already being treated. And so it sounds like yet again, there would be a big distribution difference if you were to compare with live data, because clearly not everyone is already being treated for hypertension. If anything you might want to see how this model performs on evaluation data made up of people who have not been treated yet, to evaluate its performance strictly for new cases.



## gamable systems
p47, people research, showing like with resume keyword stuffing of the past, video interview analysis are similarly gamable. they tested glasses, backgrounds , etc, and unclear what sample size and stats were but they say these appeared to influence outcomes.

## Netherlands, welfare fraud detection
p49 the authors given an example where the Dutch government deployed an algorithm to detect welfare fraud, but apparently some nationalities were associated in the output with higher fraud predictions.

at this point, it's pretty common to use things like statistical parody, and other more ground truth based methods to see very simple is the proportion of positive outcomes matching the proportion of positive in the ground truth demographics, and this is called bias analysis. I am not seeing that the authors of this book referred to that, but I wonder if that is a good enough tool to make sure at the very least that your model is not biased.

also, the welfare detection fraud model that they mentioned was deployed in 2013 and I wonder when was the GDPR regulation produced which allowed or whether it made it required for many algorithms to explain their outcomes which would make it more straightforward for people to challenge the result of models.

But wow, sohnds like the prime minister resigned so likely proper bias assessments were not performed?


## End od Experts
Noticing interesting parallel between Julian Whatley's "end of experts" [5] and the "AI Snake Oil" book's disappointment in predictive models , in that both  offer generalized "advice" .  Classical ML goal is literally to generalize well. It is good in principle, to reduce error overall but yes by definition predictions attempt to   avoid using features that are too tailored. Rule of thumb preferred.

## limits of prediction
p64 interesting trend, weather forecqst accuracy 6 day today, as accurate as 5 day a decade ago, so 1 day a decade. Using simulations. 

p66 their opinion that spam classifiers are in the "good ML" category, attributing to mountains of data. 

p67 but highly specific outcomes about people, are less reliable. Depends on the example. Depends on how chaotic the system. 

Generalization being made is, macro is more reliable than macro. But hmm I  dont think thats always true. They cite p68, earthquakes yes, we know a lot about prevalence geographically . ( Recalling Nate Silvers book points to earthquake prevalence following power laws) . 

But we didnt do a good job of predicting the 2000 dot com bubble, the 2008 mortgage crisis  , the 2019 COVID19 pandemic of course, and people are having a hard time agreeing when will the gen AI bubble  burst (2026 probably ).

Im reminded by the Nassim Taleb graphic of a Turkey forecasting everything is great, right before ThanksGiving! 


# Risk though
The AI Snake Oil discusses one side of predictions and risk management and market making [6] is the flip side. I think Ray Dalio would take the other side as well along with Lloyd Blankfein I suspect . 
  

# references

1. https://press.princeton.edu/books/hardcover/9780691249131/ai-snake-oil#preview
2. Russel Peters routine
3. https://vimeo.com/785843804
4. aueomation bias, noted elsewhere, https://youtu.be/P5HxTdkitmA , Julian Whatley 
5. expert advice, as general adviCe, https://youtu.be/o2S2w9RiNtI , Julian Whatley 


6. risk management point of view, Lloyd Blankfein, and market making, inteeurview Sam Harris episode, 473 Making Sense





