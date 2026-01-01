---
title: The kanban cage 
date: 2025-10-21
draft: false
---

*DRAFTING*

I have for a while now learned about how the mainstream deals with knowledge work glut. I was a big fan of David Allen's Getting Sh\*t Done--just kidding ;D it was Getting Things Done<sup>[1](#references)</sup>. And I forget where, but I also came across the notion that all the  pre-digital-era ideas to getting your sh\*t together don't apply since paper cuts are nothing compared to a digital sh\*t storm. Ok enough of that bullsh\*t. 

While reading about these civilian  approaches to knowledge work glut, I  have also lived the parallel life of experiencing how the software world has been struggling with it . Most people don't know much about "Agile" but it has been slowly spilling into the mainstream. Cal Newport sits sort of close enough to the software world that he has written, in Slow Productivity<sup>[2](#references)</sup>, sort of borrowing some of the good parts of *Agile*, to help modern knowledge workers with their woes. I have not yet sat down with Cal's book but I have heard him characterize the idea of the infinite work queue quite well, in his podcast. He describes that knowledge work is unlike physical work, where you do precisely what is in front of you, if you are a barista tending to customers at a coffee shop of an auto worker on the classic Ford assembly line working on cars.

Knowledge work is a special kind of hell, where if you are not careful, you will receive an endless inbox of actionable things which are only visible to you. There can be emails to respond to, reports to write and in software an endless list of issues and bugs to triage. Cal thoughtfully borrows the concept of the sprint from "Scrum" which is a flavor of "Agile", where you make your work visible on a "sprint board", because then you can theoretically gate your time, pointing to what you are currently doing in your "sprint" and that anything additional would need to go into a future "sprint" or otherwise would have to "bump" an in transit task, leading to a kind of messy context switch that is the killer of flow and classic waste. In principle, this sounds like a fair improvement upon the knowledge worker status quo, however it comes with a price, in that you may lose all control of your time.

## Surveillance Productivity
If you are not careful, your Scrum / Agile / sprint system becomes your Kanban Cage. In principle, your time looks protected, but this constraint means that everything you do is scrutinized. The problem here is that although in theory your only job is to do what is on your "sprint board", this is actually far from the truth. You are still spending most of your day simultaneously collaborating with your coworkers because "Scrum" is a "team sport" as they say. Depending on how senior you are, you may spend at least half of your time helping to unblock your teammates as well as your customers within your organization or outside of it, dealing with bugfixes that crop up and impact user experience. 

In fact all of the responsibility of "sharpening the saw"--*making your product more resilient so your users report fewer bugs or improving the quality of your internal documentation so your teammates can self-resolve their issues*--falls on your back, and you basically cannot put any of this extra work into your actual "sprint board" because in practice the business will do their best to "help you prioritize" your work, which is to say "their short term work" versus your long term stability resiliency work. 

Much more to say on what I see as a kind of light at the end of the tunnel. I think it starts with negotiation.

###  You might be in a Kanban Cage if...
If you are being asked to give a T Shirt Size to ypur Task, you might be under surveillance. 

Predictability is this intriguing part of some scrum ceremonies .

You know complex tasks are not tractable yet this concept of estimation creeps in. My favorite quote on the topic, 

> If I knew how long this took it means I already did it so I could just give it to you.

( e.g. NP Hard Problem)

And the book No Estimates cleanly states, the simple alternative is just get good at cutting scope. Again , it is negotiation. 

And the cutting skill invalidates Sunk Cost Fallacy if you do everything quickly.

So if you are doing planning and it works , it probably means youre doing widget work, which yes you have to do every once in a while, but hopefully thsts not your life otherwise exploit and no explore . (exploitative by definition ) .


### The Tacit Dimension 
How did we get into this mess where light hearted terms like "planning poker" are used to engage with topics around the future that we really cannot know much about. 

In the realm of the unknown of what may take place in a non-widget-work project, you might really not know and thinking forwards , you can spend enough time on the hypothetical to merit actually doing the work. 

But you might also enter the realm of the tacit dimension, where you may know something but you just cannot describe it well . This is also the realm of "show don't tell" . 
 (requote from  Cal on email [10](#references)  ), Cal quotes a known line from a michael polanyi book,  The Tacit Dimension, 

> “I shall reconsider human knowledge by starting from the fact that we can know more than we can tell."

My coworker summarized this brilliantly also as, *"planning is planning and working is working."* This also reminds me of the handy "driver" analogy I heard in this interview<sup>[11,12](#references)</sup>   between Barbara Oakley and Daphne Gray Grant, about her advice on how writing is like driving a car and between your writer and editor, only one can drive the car at a time, otherwise it gets messy. And I realize similarly, Planning and working are also similarly very different and it's almost like attempting to plan in the level of detail recommended in my first experience of PI Planning felt like attempting to mix these two. You simply can't achieve that level of detail while you are planning and if you try, well you might  as well have spent that time working.

The answer I usually get is the Eisenhower quote about about how, 
> "plans are worthless, but planning is everything"

but this quote feels grossly out of context because software projects are way more flexible than battle plans, but also Eisenhower's quote literally also acknowledges that plans are worthless and yet a lot of software planning language espouses language like "commitment" and "capacity planning" and "estimates" which enter a territory of certainty that is not knowable and not necessary to know (hence "agility").

To answer the question, I think we are here out of a very strong desire for certainty and a discomfort around not having the certainty, that maybe is difficult to shake for many.

## Fisticuffs or alignment?
 Martin Fowler's blog on negotiation, Product vs Engineering, https://martinfowler.com/articles/bottlenecks-of-scaleups/03-product-v-engineering.html

my notes: "2025-10-23_0837--0400"

Wow this is written well, says what I didnt really realize what I wanted to say, that there are basically two backlogs, product backlog and engineering backlog.

But on our team, the problem is deeper that our product backlog isn't even  for customers; it's for the devops team. some  referring to an adjacent concept of buckets also.

Our Product Team is not accurately representing the product interests , not engineering interests either. It has been no taxation without representation . As I read about PI planning, the distinction with OKR planning is that "everyone is in the room" so that the meeting represents all the interests at play.

That , lack of representation has been a problem in our OKR meetings too, wrt, top down and bottom up OKRs.

But the theory and execution of pi planning can be different.

As an example of our recent experience, 
 what ended up happening, our plan was kind of oddly pre-populated and there was no connection to the various exploratory working sessions we were doing over the last several months. We spent time in a bit of asynchronous work, writing out sort of plans across the stories. Then people added a kind of confidence. Then under a bit of  coersion  and duress, even recorded ,--to sign with blood as we joked-- , agree, commit , without a full review of phoenix, technical backlog, tech debt, etc.

Only "ad hoc" lip service  in Pi planning might be  the on-call work , which is not "tackling" tech debt at all, it is  making minimum monthly payments,      just fixing what broken without making it more resilient for the future.

quote, 
> "Us vs them", and product leaders throwing requirements over the wall, treating engineering team as a feature factory. 


quote
> When product and engineering organizations aren't communicating or collaborating effectively during product planning, we tend to see an imbalanced investment mix. This can mean the product backlog leans more heavily towards new feature development and not enough attention is directed toward paying down technical debt.

Hmm though yea im leaning more towards Shane De La Moore that this is got to be internal , precisely why PI Planning is not the fit for our team. Basically, here are the two choices: (1) either we have a fully unified team where everyone is fully represented. And perhaps we can have a board we share with product, because it is just our product. No us vs them 

(2) us vs them isolation, so engineering team has its own lead and its own board and negotiates the various deliverables , and handles its own tech debt decisions etc, balancing.


### Product is cool
This article goes into depth about cool ways to unify the team, get excited about product. 

We are sorely missing this .This year , just mainly bending to will of  the   Devops dictatorship in our company , showing fealty to asks without demonstrated utility.

Outcome oriented team, vs our activity separate. 

### Backlog negotiation 

The PI planning thing totally missed this mark. that we forgot to negotiate 

## epiphany reading the google swe culture book


ok I found it , https://abseil.io/resources/swe-book/html/ch05.html the chapter on tech leads and engineering managers.

ok I kind of had this intuition about the way my current company runs projects is spineless and reading a bit of this online book, I think I'm on the right track.

In my past companies , the way of getting work done is that each person would basically be part of small execution teams (2 or 3 people) and each team would just work on basically one project several days at a time. The mini teams just organically divide up the work and just collaborate super organically. And you just talk to your boss basically whenever you got super excited about something you want to show or when if you held off too long , your boss would tap on your shoulder to see what's up haha.


### Leadership by Backlog
Instead my current team does Scrum     but without the negotiation. The product arm of the team is mainly  a mouthpiece  to the company's Devops agenda, which our customers dont really know about and affects our ability to produce good improvements.  

And without a healthy back and forth, our product arm  just uses   their backlog like a shield and any resistance is met with agitation . 

Passive agressive is the operative word here w.r.t. the sprint backlog. 

#### First PI Planning experience 

Everyone participated hoping it would finally be a team effort, and then at the end the  product arm of the team rearranges the results , sorting projects by  their own preferrence. 

That final moment wqs quite eye opening and the PI planning arguably pointless.

I suppose the PI Planning process enables this kind of scenario , but I understand from this video, recently, the theory and practice, can diverge a lot. 

The quote was, it is like Strawberry Jam, the further it spreads, the thinner it gets.


And lead-by-backlog was not the originalintent.

 And I really love reading this Google SWE culture document because it reminds me of the good old days of working projects at past companies .

## BYOA
bring your own agile. if someone offers you a SAFe space, jyst say thanks but no thanks 😂

## flip predictability on its head


why not commit to a cadence and get good at cutting slicing splitting. 
this is A LA No Estimates.

And instead of one sprint goal per sprint tied in , into a PI, just do OKR, which is order invariant, communicable, specific measurable and gives you room for stretch and moon too.

PI planning is like a shitty OKR. 


funny in this video<sup>[4](#references)</sup>, at the end the guest says PI planning is like OKRs but with everyone involved, discussing it. I think, ok well, that would be cool but why not just have the OKRs plus negotiation? PI planning has all other weirdness to it. 

law of raspberry jam. further it spreads, thinner it gets 😂


## Kant
Kant explained morality systemically, his theory, "categorical imperative". He gave examples, one involving debt repayment. Not repaying debt out of avoiding consequence of no more loans is too self interested to be moral for Kant. He said, broadly, if no one repaid their debt, no one kept their promises, then there could be no trust. 

And from the Kantian perspective I understand why PI Planning is a kind of attempt at a social agreement in company projects. There is a huge desire for certainty. 

Kant did also say that humanity cannot know the true nature of reality .


## multithreaded, locks vs distributed map reduce 

locking is bad. Golang avoids. best use distributed, concurrent. and limit dependencies. 

reduce, shuffle, are expensive 

## Measure what Matters not what is easy
Measuring predictability is so predictable . it is also the   
McNamara_fallacy: 
> "the first step is to measure whatever can be easily measured. The second step is to disregard that which can't easily be measured or given a quantitative value. The third step is to presume that what can't be measured easily really isn't important. The fourth step is to say that what can't be easily measured really doesn't exist."

It's also Goodhart's Law, but this corollary, offers a motivation too. 

Like in this https://michal.piekarczyk.xyz/post/2025-11-08--innovation/ innovation note, the hard stuff is just not within your grasp, but you need to offer something to your overseers. 

This is also Cal's notion of "proxy productivity" , busyness is visible, so that is what you reward.

At my place of work, folks share words of wisdom on their anniversaries and I didnt prepare this time recently, was kind of stuck, I said. Will prepare later I said. but funny opportunity came up, I was randomly mentioned that I had most commits out of others or something like that 5,000 or whatever.   I responded like, umm this is not impact and that what you measure fails to become a good metric. we went to another topic. At the end I realized my wisdom if you can call it that, is dont fzll into the trap of proxy productivity, pseudo Productivity, because the good stuff typically is not noticeable but without putting your head down, you will just be busy. waving your arms around. Funny , my skip level   interpret what I said as "big picyure thinking " which is important too but kind of missed the point, being, big picture doing ! 

That being said, "building in public" is great too, blasting out legit artifacts , but not just git commits haha 😆. Someone else was saying she wants a prize for the number of meetings she attends. Indeed.   



## the way things were

Before pi planning hit our shores, inviting itself in, we planned by everyone putting what theu were excited about into a big group writable table and everyone with equal votes , voted. then we ranked. thats what ir was . that was great

## Dont Defer thinking
You shouldnt   defer thinking about what problems to solve to your product team any more than you should defer design choices to your AI LLM tool of choice. 

(Last bit inspired by https://youtu.be/eIoohUmYpGI ) 


# Summary of my points

- As the Martin Fowler blog puts it, a team Backlog is a mix of product and engineering priorities. Product looks at the user perspective, and Engineering looks at stability, reliability, maintainability and all the other -ilities. 
- All the team members will wear the Product and Engineering hats , some might lean one way more than the other. 
- There might be other external pressures other than Product or Engineering that put thumbs on the scale as well, call it Corporate. Corporate doesnt represent either user interests or engineering interests. But they are the HIPPO so you will hear them
- The Corporate opinion for example: lets measure proxy productivity, in lieu of value because is hard to measure 
- Predictability is a typical measure of proxy productivity 
- The process of PI planning is a negotiation, where all parties state their positions and bid for the time of the individual contributors 
- At the end of the day , there is room to be excited about whqt the team is up to and can unify behind.


# References
1. Getting Things Done, David Allen
2. Slow Productivity
3. Martin Fowler's blog https://martinfowler.com/articles/bottlenecks-of-scaleups/03-product-v-engineering.html
4. https://youtu.be/jHRsBDC5E9Q , Yuval Yeret and Ryan Ripley, "Breaking the SAFe: Deconstructing PI Planning"

5. Extreme Gohorse

6.  Cal Newport and Adam Grant, https://link.chtbl.com/4HaHYkSm

7. https://michal.piekarczyk.xyz/post/2025-06-04-fragile/ 

x. https://en.wikipedia.org/wiki/McNamara_fallacy


8. https://www.seangoedecke.com/how-to-ship/
 
9. .... north star concept

10. why can't ai manage my email , Cal Newport , New Yorker

11. my description about writing brain , https://michal.piekarczyk.xyz/post/2023-09-10-summary-learning-how-to-learn-coursera/#if-your-inner-writing-brain-and-editing-brain-are-in-the-same-car-only-one-can-drive-at-any-one-time- 
12. learning how to learn , https://www.coursera.org/learn/learning-how-to-learn 