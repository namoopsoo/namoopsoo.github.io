---
title: The kanban cage 
date: 2025-10-21
draft: true
---

I have for a while now learned about how the mainstream deals with knowledge work glut. I was a big fan of David Allen's Getting Sh\*t Done--just kidding ;D it was Getting Things Done<sup>[1](#references)</sup>. And I forget where, but I also came across the notion that all the  pre-digital ideas to getting your sh\*t together don't apply since papercuts are nothing compared to a digital sh\*t storm. Ok enough of that bullsh\*t. 

While reading about these civilian  approaches to knowledgework glut, I  have also lived the parallel life of experiencing how the software world has been struggling with it . Most people don't know much about "Agile" but it has been slowly spilling into the mainstream. Cal Newport sits sort of close enough to the software world that he has written, in Slow Productivity<sup>[2](#references)</sup>, sort of borrowing some of the good parts of *Agile*, to help modern knowledge workers with their woes. I have not yet sad down with Cal's book but I have heard him characterize the idea of the infinite work queue quite well, in his podcast. He describes that knowledge work is unlike physical work, where you do precisely what is in front of you, if you are a barista tending to customers at a coffee shop of an auto worker on the classic Ford assembly line working on cars.

Knowledge work is a special kind of hell, where if you are not careful, you will receive an endless inbox of actionable things which are only visible to you. There can be emails to respond to, reports to write and in software an endless list of issues and bugs to triage. Cal thoughtfully borrows the concept of the sprint from "Scrum" which is a flavor of "Agile", where you make your work visible on a "sprint board", because then you can theoretically gate your time, pointing to what you are currently doing in your "sprint" and that anything additional would need to go into a future "sprint" or otherwise would have to "bump" an in transit task, leading to a kind of messy context switch that is the killer of flow and classic waste. In principle, this sounds like a fair improvement upon the knowledge worker status quo, however it comes with a price, in that you may lose all control of your time.

## Surveillance Productivity
If you are not careful, your Scrum / Agile / sprint system becomes your Kanban Cage. In principle, your time looks protected, but this constraint means that everything you do is scrutinized. The problem here is that although in theory your only job is to do what is on your "sprint board", this is actually far from the truth. You are still spending most of your day simultaneously collaborating with your coworkers because "Scrum" is a "team sport" as they say. Depending on how senior you are, you may spend at least half of your time helping to unblock your teammates as well as your customers within your organization or outside of it, dealing with bugfixes that crop up and impact user experience. 

In fact all of the responsibility of "sharpening the saw"--*making your product more resilient so your users report fewer bugs or improving the quality of your internal documentation so your teammates can self-resolve their issues*--falls on your back, and you basically cannot put any of this extra work into your actual "sprint board" because in practice the business will do their best to "help you prioritize" your work, which is to say "their short term work" versus your long term stability resiliency work. 

Much more to say on what I see as a kind of light at the end of the tunnel. I think it starts with negotiation.

## Fisticuffs or alignment?
 Martin Fowler's blog on negotiation, Product vs Engineering, https://martinfowler.com/articles/bottlenecks-of-scaleups/03-product-v-engineering.html

my notes: "2025-10-23_0837--0400"

Wow this is written well, says what I didnt really realize what I wanted to say, that there are basically two backlogs, product backlog and engineering backlog.

But on our team problem is deeper that our product backlog isn't even  for customers its for the devops team. some  referring to an adjacent concept of buckets also.

My thing has been, Im realizing, our Product Team is not accurately representing the product interests , not engineering interests either, so its no taxation without representation I think  . You cant have a PI planning meeting if it doesnt accurately represent all the interests at play.

That , lack of representation has been a problem in our OKR meetings too, wrt, top down and bottom up OKRs.

And whqt ends up happening, people in a PI planning meeting are coerced , under duress, even recorded ,--to sign with blood as we joked-- , agree, commit , without a full review of phoenix, technical backlog, tech debt, etc.

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

Yea and instead my current team does Scrum and it is shoved down everyones throats from the top of the company. It is terrible. It is like "leadership by backlog" . My team has a so called Product Owner but this person literally is not a team player, very judgemental, extremmely insecure to criticism, always sounds condescending , never contributes any insights or opinions into a conversation unless it is to sound as if speaking from some high mountain top of authority.

All they know how to do is just hide behind their backlog and just sound very agitated whenever people dont acknowlege items that have been placed into each sprint backlog. But this person never asks for feedback. ever . And boy do they love the PI Planning . We did the pi planning thing , everyone participated hoping it would finally be a team effort, and then at the end this product owner person they just rearranged everything , putting their own preferred projects at the top but they were actually doing it while sharing their screen haha so we had a kind of embarrassing moment and we said hey what are you doing , we literally just spent two days doing this team thing and now you are just deciding everything; what the heck was the point of all that if you wre just going to change everything last minute.

Arguably pointless. Anyway, actually I suppose I shouldn't blame this person, instead I suppose Scrum and SAFe gave them this weird mission of lead-by-backlog and that is kind of what they are spinelessly doing. And I really love reading this Google SWE culture document because it reminds me of the good old days of working projects at past companies .

## BYOA
bring your own agile. if someone offers you a SAFe space, jyst say thanks but no thanks 😂

## flip predictability on its head


why not commit to a cadence and get good at cutting slicing splitting. 
this is A LA No Estimates.

And instead of one sprint goal per sprint tied in , into a PI, just do OKR, which is order invariant, communicable, specific measurable and gives you room for stretch and moon too.

PI planning is like a shitty OKR. 


funny in this video<sup>[4](#references)</sup>, at the end the guest says PI planning is like OKRs but with everyone involved, discussing it. I think, ok well, that would be cool but why not just have the OKRs plus negotiation? PI planning has all other weirdness to it. 

law of raspberry jam. further it spreads, thinner it gets 😂


## kant
Kant explained morality systemically, his theory, "categorical imperative". He gave examples, one involving debt repayment. Not repaying debt out of avoiding consequence of no more loans is too self interested to be moral for Kant. He said, broadly, if no one repaid their debt, no one kept their promises, then there could be no trust. 

And from the Kantian perspective I understand why PI Planning is a kind of attempt at a social agreement in company projects. There is a huge desire for certainty. 

Kant did also say that humanity cannot know the true nature of reality .


## multithreaded, locks vs distributed map reduce 

locking is bad. Golang avoids. best use distributed, concurrent. and limit dependencies. 

reduce, shuffle, are expensive 


# References
1. Getting Things Done, David Allen
2. Slow Productivity
3. Martin Fowler's blog https://martinfowler.com/articles/bottlenecks-of-scaleups/03-product-v-engineering.html
4. https://youtu.be/jHRsBDC5E9Q , Yuval Yeret and Ryan Ripley, "Breaking the SAFe: Deconstructing PI Planning"

5. Extreme Gohorse

6.  Cal Newport and Adam Grant, https://link.chtbl.com/4HaHYkSm

7. https://michal.piekarczyk.xyz/post/2025-06-04-fragile/ 