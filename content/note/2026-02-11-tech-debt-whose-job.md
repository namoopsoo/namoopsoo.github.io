---
title: "Whose Responsibility is Tech Debt"
date: 2026-02-11T19:56:26-05:00
draft: false
---


Starting a small note here, around discussions myself and others have been having on my team about whether addressing tech debt should be prioritized explicitly or is it something you just address like you might with local refactors with the so-called boy-scout-rule [1].

Realizing after having several converstions about this lately that there are many diverging opinions on this. I have some teammates who see this as the responsibility of the product team, and others who will tackle it head on like an obstacle in their way of the main task at hand. And a more nuanced middle-ground of colleague who is a fan of The Goal, is that you should not have tech debt in the first place if you "pay it down" in stride as part of your role of implementing whatever the company envisions.

That is an oversimplification of course. In context, every view really does make sense. For instance, it really depends on, how much tech debt are we talking here? My colleagues who tries more to surface the tech debt to the product team, is doing this because time and time again whenever he tries doing literally anything, he will stumble against systemic tech debt that either balloons his initial research to understand how to implement a feature, or deploying a feature pulls down the rest of the system kind of like if you were using the table cloth as your bib and getting up pulled the contents of the meal onto the floor, with all the dinner guests agape! 

The problem, however, has been that historically, attempting to influence tech debt into the product team's road map has been nearly impossible. But the exception to this was, without cause. That is, although it is possible to explain how tech debt can theoretically cause a problem, it is easy when you get dinner on the floor, because you used the table cloth as your bib. And this pattern of tripping into some kind of problem, ranging from disaster to meltdown, is how our team has tended to address tech debt 98% of the time. In other words, the product team doesn't tend to get involved until the risk is no longer a risk but a reality.

I suspect that this above approach is not only how most teams deal with tech debt, but also how virtually anyone anywhere deals with any theoretical problem. 

Maybe a more accurate way to state this is, most problems are actually obvious, but the risk is not. So, you might see a laptop cable being a trip wire, but not a trip hazard. It is obvious a cord on the floor is not a good thing, but you are highly confident you will never trip on it! Until you do, and that is when you start being more proactive, by just using the battery and not really charging as much 😅 .

## whose responsibility is it: short answer
So maybe it is the universe's responsibility to handle tech debt in most cases!?

## motivation
It might also help to explain why I'm writing about this topic now. More recently, we had a deployment which did bring down a few production batch jobs and this was noticed by manager's manager. And politely, he offered to help, but to me this was a polite way of saying, IMHO, *"hey you folks should test your code better."* 

To me this was an opportunity to try surfacing tech debt as a risk again with our product team. Our product team has traditionally said, when asked about tech debt, that they cannot blend it into the road map because it is not a priority from the management. Well in this case, 🤣, the management literally implied it is something they do care about. And so now we have an opportunity to cash in and harden the ship a bit more. Maybe this opportunity will not last long!



# references
1. boy scout rule

2. The Goal