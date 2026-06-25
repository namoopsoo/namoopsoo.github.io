---
date: 2026-06-24
title: Working title
draft: true
---

Doing a new planning increment. Measuring 62~ % as our predictability. But we have raised many times why our platform is not predictable even to our customers , imagine how so. 

Our management refuses to clarify why they have not championed UX.

I had pitched a UX improvement last quarted . nopw no one cares. My colleague built a POC to measure time to deploy. no one cares.

so what is it that our leadership team are prioritizing instead ? The vision that they have sold, is lets make our product conform to company standards of security. but literally as I am writing this, my colleague who is trying to wrap up his own support is announcing that he cannot deploy a production fix.
and the reason why is because we are  quote unquote, conform to companies standards of package management. these standards have been breaking our ability to deploy for the last month and a half. The reason why is that? They have decided to react very aggressively, to some of the recent supply-chain attacks, by throwing out the entire model of using the severity of a package as a way to trust it. instead, they have decided to stop downloading new packages altogether and instead allowing packages that are new in a sort of a trickle. but in the process, they have inadvertently broken the deployment for lots of different teams, that's because deployment were using new packages, but because  they also managed to remove lots of packages that were already part of our company loczl package repositories. so to me, this is proof that they don't actually know what they are doing.

I totally get that the rise of  supply chain attacks  is a good reason, not to accept new packages immediately, even if they are patches to  packages that have high    C.V.E. . but the new ones should be at not every environment has a good reason for this level of CVE scrutiny, because our environment, for instance, is a sandbox environment.


The subtle point is that 

# References 
1. https://youtu.be/Z9ftpRhRiJE 







