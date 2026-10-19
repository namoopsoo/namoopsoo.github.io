---
title: Code Read Burnout Thing?
type: blog-post
date: 2026-10-14
slug: 2026-10-14-thought-on-the-code-read-burnout
sources:
  - "[[2026-06-19 medium article code read burnout]]"
  - "[[Interview pragmatic programmer Charity Majors and Gergely Orosz]]"
  - "[[2026-09-25 Shopify Lütke slop grenades]]"
related:
  - "[[skin in the game]]"
  - "[[Nassim Taleb]]"
  - "[[blameless post mortem]]"
  - "[[Tobias Lütke]]"
  - "[[Dax Raad]]"
---
  
  
<!-- 
splitting , original [[2026-06-19 medium article code read burnout ]]
-->

I was reading [5], this kind of click-baity article, "My Best Senior Engineer Quit Last Month. Her Exit Interview Was Scheduled for Forty Minutes. The Last Five Changed How I Run My Team." But found myself with a few thoughts, so writing them here.  

## On production fires
The author asked the question,
> If AI wrote every line of code you produced tomorrow, would you still be the person people call when production is on fire?

I think my answer is  there's two  more dimensions to consider. But yes all three are important. Who authored the code and who is on call? Maybe let’s just make a distinction that authorship is who put  their name on the git commit which can still be you whether you copy pasted an idea you read from stack overflow or whether a coding harness typed it for you . So if you took the credit for the code on git, 😅 presumably you understand it. And if you deployed this and the person who is on call will likely ask you to help if something goes wrong.

I think my ability to respond to production fires is related to practice from both debugging code locally but also from responding to production fires in general while on call. Regardless of whose code it was, I'll learn something but if I had caused an issue, I feel I get to close a personal feedback loop. And skin in the game as Nassim Taleb puts it is very relevant here. So if I wrote the code, I have more skin in that game. If the code I wrote fails on my laptop terminal,  then I all of a sudden care deeply about wanting to understand why 🤔. And figuring out the problem gives me satisfaction. If I wrote the code and it fails in production, then honestly, whoever is on call, I ask them to please loop me in. I want to be able to fix my mistakes since I wrote the code. And I then therefore get to feel a bit of redemption for debugging a
production issue that I caused. Of course that means everyone is okay with blameless postmortems!

This is also  why I also appreciate the Gergely Orosz and Charity Majors interview [7],  where Charity saying there are those who are on call and those not haha… I honestly never worked on a team where I was not responsible for the code that I wrote. (*Side note, in that interview, Charity also says production is the best place to test code -- hashtag I don't often test my code but when I do it's in production-- and this has been my philosophy as well albeit with canary and or blue-green, kind of like pics or it didn't happen and maybe the world is catching up to this now*).  Okay but now the world has suddenly changed and people are using coding harnesses as their ghost writers a lot more, still placing their own name on the work, myself included. This is just where we are at the moment, so let's address that.

So now what about authorship without being the writer? Like a ghostwriter? This gives you clearly much less skin in the game. When I debug problems on my laptop in code written by Claude or some other coding harness, honestly I found myself just not really caring as much and I will just submit to the pattern of copy-pasting stack traces back to the agent if I have to be in the loop and preferably the agent can run tests too, to close the loop faster.

And increasingly, when there are problems in production, and if you are on call and it is a weekend, you will want to use every tool at your disposal to get back to your weekend. There are also tools popping up these days which attempt to diagnose and create patch pull requests. But I think no matter how much context is available to agents say in markdown files in repositories, in incident root cause analyses and post Mortens from the past, it may still be incomplete and you will still have to be in the loop.

I think this is because of yes lots of stale documentation and stale comments and lots of code that is going through refactors. But also this phenomenon Martin Fowler described about now no matter how many architecture diagrams people draw, there will still be so much that is left unsaid and exists in the conversations people have informally. So this hidden context is available only to the people which makes them better positioned to troubleshoot weird cooky productions fires too. [1,2,3]. 

So both of the above are true these days, that people are starting to have a more shallow, surface level relationship with the code that exists in prod. People  are maybe spending proportionally more time writing English, thinking, designing and less time chiseling as DHH puts it not so charitably, haha. And yes all that time in the armchair makes us definitely more beholden to the same tools to fix prod fires. These are quite the trade-offs eh?  

Hopefully this is an interlude and people can evolve away from these superficial interactions with systems soon. But for now at least, what does all of that do to the roles themselves as they are?

## Necessarily more reviewing, less building?
Reading the main quote that motivated the author to write his blogpost. 
> She said: “I haven’t built anything in eight months. I’ve spent eight months reading things a machine wrote, trying to find the bug it was too confident to see. I’m not an engineer here anymore. I’m a verification layer for an agent. I didn’t spend ten years getting good at this to become the thing that stands between a model and the incident it’s about to cause. I’m tired in a way that has nothing to do with hours.”

The author is saying agents are generating lots of tech debt. Yea, but that doesn’t mean we have to merge it. Maybe the advice is, don’t give the agent control of git, even. It’s up to you what to commit and what to publish in your PR. I think back to this comment [9] from the creator of Pi , Mario Zechner, -- a Peter Steinberger contemporary, -- about how his public git repo was getting flooded with bots, which he was calling clunkers. This is also echoes a pre-agentic concept of what people say online when behind pseudonyms versus behind their actual names. They will troll more when they are pseudonymous, that is and similarly, when colleagues submit pull requests to each other, they likely feel a different way about it. Charity also had a good point on this matter. She was saying if it takes someone more time to read it than it took you to write it (ghost write it, that is), then that's bad . Rude maybe she said. And yea I think when we look our colleagues in their faces, we can help avoid the moral hazard of the slop grenades  as Tobias Lütke has called them. 

And also powerfully, Dax Raad has said many times, and Charity also said actually in that above interview, that more features should not be the default. Charity put it kind of like, constantly changing the UI because you can do it faster now is likely not what your users want. And Dax's point was a bit deeper that we have more time now and we should invest it into making what we have of higher quality and also we can put in more time to do things like add better documentation and spend more time on refactoring. None of these are new ideas and I remember reading about them so long ago in the Google Software Engineering best practices guide that has taken many forms, that software being a liability, ought to have a short half life. This was so true when it was written maybe a decade before vibe coding and it is even more true now. The nice thing about refactoring, also, is that this is literally the kind of pull request where human reviews are not necessary, because everything should satisfy regression testing. The functionality is expected to be equivalent. So this is a good opportunity to add those nice tests to be able to verify functionality has been maintained programmatically.

And the other important principle, speaking of those Google practices, the section about small pull requests [10] is likely more relevant now and will likely get additional etiquette updates if it has not already. PRs should still be quick and easy to review, and I think given  that the stakes are getting higher these days, with more high profile outages in the news, there ought to be a muxh higher onus on the  person *authoring* -- and not necessarily writing-- the code, to do more upfront QA testing, to make it extremely easy for a reviewer to give their vote of confidence. 


And anyway we are just in the middle of this sea change and we will likely be shifting closer to something like Peter Steinberger's idea of "Prompt Reviews" where you focus more on the intent, zooming out, as another way to reduce the reviewer's burden.

### Throughput, productivity is misleading 
> I am not telling you the dashboards are lying. They are telling the truth about throughput

And again, throughput is not necessarily better if higher. So far I'm seeing the author just writes about this throughput as productivity and not necessarily as an opportunity for the quality improvements mentioned above.


<!-- 

Another quote,

> There is a thing in your head and you are making it real, and there is a quiet satisfaction in watching it take shape, and at the end there is something that is yours. The work is generative and it gives something back.

Yes this is so rewarding!!

----

> You carry all of the responsibility and none of the creation.

Yea. This begs an inversion of this antipattern 

-->

## Freedom and responsibility
To borrow the Netflix No Rules Rules phrase, the agentic assist, might provide a different spin on this whole discussion. So their "freedom and responsibility" concept can be borrowed in that, you have the freedom to use these tools to make your life easier, but in principle, that doesn't mean you should walk away from the responsibility of understanding what you're proposing. 

(*Oh right and it does sound like that Spiderman quote too about power and responsibility.*)

And reading the author's follow up article too [6], saying Priya positioned herself as the reviewer of agent output rather than high level designer, does feel disingenuous, because the fastest way to understand that code is to get your hands dirty and mess around with it. 

<!--
Just reading the code casually might be too shallow an activity to know what it is doing, unless you have experimented with this before. -->

It is unclear if shallow interaction with systems can yield deep understanding. All we do know is that deep interaction can yield deep understanding. 

This notion of understanding comes up in this Carlos Kelkboom [8] interview too. I like how he underlines that if your goal is to learn something, then you can only really do this by hand. But he concedes that in the workplace, your goal might be to just execute and then coding harnesses really help. So haha, nervous laughter, this probably means as per usual, your free time just doesn't exist because you are basically using it to learn the things you might not have time for at work. 

<!--  

> She did not complain in one-on-ones, because “I am tired in a way that has nothing to do with hours” is not a sentence that fits in a status update, and because senior engineers are, almost by definition, people who absorb load quietly until they cannot.

Also I think it might be possible to invert like, humans do writing if they’re new. Only rely on harness if you understand already. And use Claude or rabbit thing for the reviews. Win win. 

-->

<!--

So think,Street Smart versus book smart armchair philosopher versus tactical operator

[[autonomous operator]], [[get shit done]] -->

<!-- 
Also I think pull requests and code review is really changing. Need maybe the design doc review or intent review. Need some [[ProofOfWork]] though. Someones  shows effort, this interview with a Carlos Kelkboom [8] . 

And more to that discussion also is that writing and debugging and experimenting is how people learn. So what happens to learning. 
-->

## References

1. Harmel-Law, Andrew (2021). [Scaling the Practice of Architecture, Conversationally](https://martinfowler.com/articles/scaling-architecture-conversationally.html). MartinFowler.com, December 15, 2021.
2. Fowler, Martin (1997). [The Almighty Thud](https://martinfowler.com/distributedComputing/thud.html). Distributed Computing, November/December 1997. Republished on MartinFowler.com.
3. Fowler, Martin (2004). [Is Design Dead?](https://martinfowler.com/articles/designDead.html). MartinFowler.com, May 2004. Originally presented at XP 2000 and published in the conference proceedings.
4. Hmm, https://www.youtube.com/watch?v=VjKYO6DP3fo Fowler and Molly Dishman, 2010s… 
5. Initial seed article, Devrim Ozcay,  https://blog.stackademic.com/my-best-senior-engineer-quit-last-month-her-exit-interview-was-scheduled-for-forty-minutes-5f2e1d29180d
6. Follow up , also Devrim Ozcay, https://blog.stackademic.com/priya-was-wrong-and-thats-the-uncomfortable-part-nobody-in-the-comments-wants-to-say-408bf731e4ff
7. Gergely Orosz and Charity Majors, https://youtu.be/HC8T1OlgYi0?t=1270&is=fFkHvo0Te_3gFv0I
8. Carlos Kelkboom, https://youtu.be/mkN4uRZYPfs
9. Mario Zechner, https://www.youtube.com/watch?v=n5f51gtuGHE 
10. https://google.github.io/eng-practices/review/developer/small-cls.html


….