---
title: Looking Forwards
date: 2026-02-07
draft: true
---

# Email forwarding mystery solved
Feeling several facepalms now that my `michal@piekarczyk.xyz` email finally forwards to my regular email inbox. After several sessions of tweaking, the answer was low tech!

# Registrar forwarding
Originally, I setup mail forwarding on my domain registrar. Only $5 a year, okay why not. After proving to my registrar I owned my hey email, I was all set, but tests yielded silence.

I spent several chat sessions with a support engineer at my registrar. 



Hmm so if forwarding from hover and cloudflare didnt work, then maybe hey.com is the common denominator here. 

## Check Anti Spoofing
If my DNS records show cloudflare is allowed to forward my mail, then does hey.com have some special rules I could ask them about ?

DKIM
SPF
DMARC


## hey.com uses ARC
For its own forwarding, [1], hey.com says they use ARC [2], 

so maybe that is what I should setup on Cloudflare DNS if possible?

# References 
1. https://www.hey.com/forwarding/
2. https://en.wikipedia.org/wiki/Authenticated_Received_Chain

3. https://community.cloudflare.com/t/email-routing-where-sender-has-strict-dmarc-lands-in-spam/348211
4. https://help.hey.com/article/809-forwarding-from-other-email-addresses

