---
title: Argumentum Computem ad Infinitum
date: 2025-08-16
---

About a year ago, 2024-08-22, I was reading Leopold Aschenbrenner's post<sup>[1](#references)</sup> on AGI and I had jotted down a  musing about a scaling law observations, but I forgot to write about it. I found my note today.

So I get that it is possible to look at charts comparing compute and performance and many conclude scaling laws mean AGI is inevitable.

I like Yann Lecun's perspective here that if transformer models are giant lookup tables, then making them bigger will make them appear more impressive, but this is not sustainable. 

>  "The problem is that there is a long tail, this is an issue that a lot of people have realized in social networks and stuff like that, which is there’s a very, very long tail of things that people will ask and you can fine tune the system for the 80% or whatever of the things that most people will ask. And then this long tail is so large that you’re not going to be able to fine tune the system for all the conditions. And in the end, the system ends up being a giant lookup table essentially, which is not really what you want, you want systems that can reason, certainly that can plan."<sup>[2](#references)</sup> 

Massive compute is the opposite of we have in our 20 watt brains.

I know Leopold addresses the categorical shifts we will need apart from the order-of-magnitude oom shifts, as "unhobbling"<sup>[3](#references)</sup>.

But I wonder if in the end the biggest categorical shift will be that we cannot download kung fu as Neo learned from Morpheus in The Matrix, but that actual learning can only be slow. Maybe this is like a reverse scaling law. That, for example, anyone who has crammed for an exam the night before, knows they can indeed access a kind of lookup table in some kind of short term memory and use that to rally during the exam. But that will be all gone the next day. Like Barbara Oakley describes in her Learning How to Learn<sup>[4](#references)</sup> course, for some reason humans learn best by chunking and attaching those chunks associatively but then also pruning the unneeded bits during sleep. It is a kind of "how do you eat an elephant? well you eat an elephant by cutting up an elephant into very small pieces and eating one piece at a time as long as that takes."

Attention mechanisms are also just the right amount of associative. And that then begs the question, then are Transformer models essentially are a kind of cramming for an exam the night before? They are not, as many people have written in general street smart, they are book smart. 

But if with engineered silicon anatomy, we if can come up with learning algorithms the likes of which surpass human learning, then great though.

But we know that these days, in the physical realm, this is exactly the shift that has occurred, as I recall reading in the new yorker<sup>[5](#references)</sup>, with the likes of imitation learning at Google Deep Mind, where at least in the physical realm of folding shirts or taking clothes out of a washing machine. Operators, like puppeteers, use robot hands to perform the tasks and they will press foot pedals marked Success or Failure depending on the outcome. This is a very slow kind of learning. It is learning of a policy, as in a mapping from states to actions with a deterministic or probabilistic function. I don't know if this has been applied to language modeling or reasoning yet, but that would be super interesting. That would literally be like a kind of teaching as in school . (And side note I think I recall teaching AI is another kind of learning too. )

Another interesting note, from a different Lex Fridman interview, from 2022-10-29<sup>[6](#references)</sup>, was from Andrej Karpathy. On how just reinforcement learning on its own, was not good enough, at least back in 2015. He described a project called World of Bits where a RL system had access to keyboard and mouse and a browser and was being trained to do like airline bookings. But he was saying it was very inefficient with very sparse rewards. And in retrospect, the hybrid approach of pretraining plus RLHF is a better idea. His point was that the initial World of Bits system was not really built with a language model, it was just kind of randomly attempting to mess around with a keyboard and mouse to book flights. But yea we know that human flavored RL is very much not like this. Humans are really good at building predictive models of the universe and we most certainly will take an informed approach to booking a flight. 

You must learn to crawl before you can walk as they say haha.

Incidentally, perhaps Doom programmer can have a different outcome ? I understand that this year 2025, John Carmack and his team have started talking about<sup>[7](#references)</sup>  their stab at the Atari game set, using their own flavor of an RL approach. And yea similarly, they are attempting not to enhance what a model experiences, instead using simply a camera that looks at a screen and a robot hand that steers a joystick.  Maybe in Andrej Karpathy's case with World of Bits, perhaps their system had access to the DOM too and they were using maybe a kind of selenium and scripted mouse keyboard control as opposed to the Carmack outside of the computer approach.

Their experiences feel kind of opposite ends of the problem? Karpathy ended up talking about how we are in a position to now create webpages that are more LLM friendly. And Carmack was saying that augmenting, annotating, sort of spoon feeding the experience for a system, is a kind of cheating and might also not even yield optimal results. This argument is very similar to what was problematic with any kind of image processing feature engineering we can do to get gains from image recognition algorithms, and we learned from the deep learning revolution of the 2010s (image net, cat paper etc), that deep learning will perform its own feature engineering, one hidden layer at a time. And the results will be better.

But yea going back to the RL question, we know that after all, even Deep Mind, the pioneers of Atari RL and AlphaGo, eventually went on to very much embrace  Transformers and end up winning the Nobel Prize with Alpha Fold. 

So back to that note about learning to crawl before you can walk and by extension learning to walk before learning to run, maybe there is something to this. I know during my entry into tensorflow during my aviation physiological classification project<sup>[8](#references)</sup>, I was fascinated to learn about epochal learning, that is how with deep learning libraries, learning on your data multiple times was simply a hyperparameter. And the idea is that behind the scenes, perhaps your network was doing its own kind of boosting but not as explicitly focusing on errors as with xgboost say.

So yea it's not to say that training foundation models does not already take a long time, but if we are doing it with gigawatts as opposed to kilowatts or 20 watts, are we just banking on the likes of those moores law gains and not those differences in kind. So yea does intelligence have a speed limit. Otherwise you're just overclocking.

### Editors note
Retrospectively thinking I got interested in picking up this scribble from a year ago I think because I was listening to Andrew Huberman talking with Michael Easter , and they were talking about armchair writing and writing from experience. Michael has taken a lot of inspiration from 35 days in the arctic, amoung many other crazy trips and just many road trips and trail trips, and just being in nature. And personally this makes me reflect on how somehow not only real world experiential knowledge is special but also just the getting out of your own head is too, and spinning some brain cycles alongside looking at some waves (as I happen to be doing while tapping these words on my phone screen this moment 😆).  

{{< figure src="https://s3.amazonaws.com/my-blog-content/2025-08-16-argumentum-computem-ad-infinitum/IMG_7156.jpeg" width="50%">}}

# References
1. https://situational-awareness.ai/from-gpt-4-to-agi/ 
2. https://lexfridman.com/yann-lecun-3-transcript
3. https://situational-awareness.ai/from-gpt-4-to-agi/#Unhobbling
4. https://www.coursera.org/learn/learning-how-to-learn
5. https://www.newyorker.com/magazine/2024/12/02/a-revolution-in-how-robots-learn
6. https://lexfridman.com/andrej-karpathy/
7. John Carmack speaks on new Atari RL work https://www.youtube.com/watch?v=iz9lUMSQBfY 
8. https://michal.piekarczyk.xyz/project/2020-04-05-aviation-kaggle-low-level/
9. https://podcasts.apple.com/us/podcast/huberman-lab/id1545953110?i=1000713063630
