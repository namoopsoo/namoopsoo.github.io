---
title: "2 Weeks Claude at Work"
# slug: "2026-08-08--2-weeks-claude-at-work"
date: 2026-08-08T12:20:54-04:00
# draft: true

# optional thumbnail
# images:
#   - "THUMBNAIL_PLACEHOLDER"
# cover:
#   image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->


I have had access to claude at work now for maybe two weeks now.  Incidentally, I had already been using open code at home for a few weeks now at this point, so I'm wary of slot machining. I notice myself leaning into lift coding. So in data science speak, lift is the benefit above a baseline. So this can be using claude to rewrite a small piece of code based on a colleague's PR feedback almost on the spot as opposed to perhaps waiting for some down time when I might get around to it. And I was iterating on a function, replacing it with a new one, and I found myself using claude to update the unit tests. That was really nice. Maybe I would have put off writing the unit test until later.

Lift tasks I am observing in myself, are often mini side quests I would have never otherwise had the spare time for. A week ago, my company's python package proxy, which blocks downloads loosely based on new CVEs, blocked a deploy of mine as per usual with some fresh 403. But this time, instead of rummaging around in the effectively broken UI, which often shows lagging 🟢 clean packages that disagree with the 🛑 403 when downloading, I asked claude to build a table of a package's version specs under CVE sorting by date. I did find this helpful for choosing a package version the first time I used it. However, because our package proxy really is trash, other CVE-free version choices I make using official CVE lists unfortunately don't agree with the 403s I end up with. So then I ended up with trial and error and fighting the proxy web gui again. 

Side note, in an ideal world, a package proxy UI and API should agree with each other and with opencve [1], nist nvd [2] and osv [3].

I also had a self review task due, where I ended up creating a script for pulling in my code pull requests I could use as the work history and a web ui I could use to help me more easily filter and annotate the more relevant work. The self review stuff can be a bit of a slog and a kind ui can be the spoonful of sugar to make the medicine go down.


## References
1. https://app.opencve.io/cve/
2. https://nvd.nist.gov/
3. https://osv.dev/list
