---
title: "Cognitive Steps"
# slug: "2026-08-01-cognitive-steps"
date: 2026-08-01T13:45:00-04:00
# draft: true

# optional thumbnail
images:
  - "THUMBNAIL_PLACEHOLDER"
cover:
  image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->
I had a coworker who left our team less than a year in because we would not cut down our development loops. By development loop, here I mean, if you want to write some new feature in a code base, can you test it locally, deploy it somewhere, test it closer to its real running conditions, and then make it live. This is also the itch of the Continuous Delivery [1] author, Jez Humble. I recall when my coworker was there, most of our code base was scattered across code islands, water gapped, through ship captains who could island hop you from one island to another. Testing was often impossible because of various databricks dependencies. Deploying to staging was sludgy, you know, slow and kludgy; you had to know about undocumented steps. Jiggle the keys in your ignition to start your car just right without shearing them off, after hearing your starter struggle-rattling. She's still seaworthy, after a few attempts, you hear the car starts. My coworker's frustration came to a head when he started his first and possibly last support rotation. When things failed and he found much of the team was perfectly fine with the inadequate pace to Jez-Humble a patch to a bug through to production, that led him to discuss this with the team. He had a few good approaches to help get some of our systems to be more, turnkey. But there was too much resistance to change and he left. Maybe I am more masochistic when it comes to tolerating slow and painful change. 

I agree with Will Larson [2] that limiting work in progress is very helpful, but I think the Everything Everywhere All at Once [3] reality is more pervasive. That is, typically you often cannot drop everything to refactor the painful test-deploy loop. You often can only tweak incrementally. This is also the practical tip I encountered in Shane De La Moore's refactoring [4] anecdotes. Shane discussed a kind of long term, alternative to boy-scout-rule, after-hours methodical style of refactoring.

Although I totally agree,--*and have written extensively about*--, that paying off tech debt is one of the hardest problems in any team, never quite being able to do it on an organization's dollar even though it is in everyone's best long term interest, I 


## References 
1. Jez Humble, Continuous Delivery
2. Will Larson, https://lethain.com/limiting-wip/
3.  Everything Everywhere All at Once
4. Shane De La Moore, on refactoring (TODO find youtube link)
