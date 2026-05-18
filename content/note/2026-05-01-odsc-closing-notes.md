---
title: "ODSC Notes"
# slug: "2026-05-01-odsc-closing-notes"
date: 2026-05-01
draft: false

# optional thumbnail
images:
  - "https://s3.amazonaws.com/my-blog-content/2026-05-01-odsc-closing-notes/boston-IMG_0977.jpg"
cover:
  image: "https://s3.amazonaws.com/my-blog-content/2026-05-01-odsc-closing-notes/boston-IMG_0977.jpg"
---



I just finished a trip to attend the ODSC conference in Boston, leaving without really understanding where we are on the hype cycle of Agentic AI . But on the flight back, I read on article<sup>[2](#references)</sup>  where Rogé Karma was walking back the stance he had about the AI bubble given new revenue data. The conference gave me a lot of confidence that regardless of what benefit agent AI will ultimately have, there was now no doubt that companies and individuals who do not upskill will fall behind in one way or another. But the article put down some numbers about the new revenue that Anthropic, open AI cursor and the  data center companies they rely on, Microsoft, Google, Amazon, Core weave, were now recently experiencing, taking them perhaps, out of bubble territory.

Ok but jumping back, so what did I learn at the conference before getting back on that return flight?

# At the Conference
At the conference, one of the first talks I went to was about private LLMs, and during this talk the speaker<sup>[1](#references)</sup> said that the adoption of AI found a cheat code, agentic AI. He pointed out that, in  crossing the chasm terms,  stats were showing only 15% of knowledge workers adopted chat organixally, but  when tools now added agents interfaces into themselves into the existing mediums people already use, like the ubiquitous Microsoft Copilot which is in the Windows taskbar, in all Office applications , in the Edge browser sidebar, so then adoption magically went to 100%. 

He called this the "opt out" vs "opt in" strategy. I asked, since his talk's focus was about encrouching LLM cost , wouldnt it be better to allow organic adoption to continue to play out? He countered that sometimes you dont know what you're missing and this shift is a useful nudge. In hindsight I would call this the 401k opt out trick many economists have recommended. I wonder what those economists would say about this LLM approach.

Perhaps unironically, as I was at my gate  waiting for departure, I also saw a post from a friend about https://copy.fail, the newly discovered Linux privilege escalation vulnerability, where a user mode process can su to root. So I keep this in mind while I learn about people excitedly giving anthropic access to rumage around executing on their lap tops. 

Back to the speaker's presentation, his point was that indeed the risk of opening up your company to   Anthropic or other companies, giving them a front row seat to your company's data, can be avoided with the open weight models that are now becoming as good as their SaaS counterparts, and with the per token cost coming up, along with surge pricing, also perhaps even a cost benefit too.

Datasaur is not the only company discussing open wwight models. In parallel, Cloudflqre had Agents Week and released serving Kimi K2.6 on WorkersAI. [18].

Between talks, I spoke with colleagues about the future of code. One was inspired by  a conversation I had with one speaker on program static analysis<sup>[11](#references)</sup>, Armando Solar-Lezama, potentially making a come back. Or at least his research team was identifying that there was a gap in code evaluation, bug evaluation in particular. He noted that even Mythos --*which he said he did not have access to*--, would not find  all the bugs, but for the sake of reliability, we do need to find all the bugs. So after his talk, I asked him what was his vision? I wondered, hey, python was so popular for data science, because it was so effortless to start learning, but also come with ease to create bugs that static type  and  memory safe languages do not run into like Golang. And it sounded like yes he sees there is definitely now more room for strongly typed memory safe languages like Rust, though that will still not be enough to make sure new code that is generated is reliable. I think one of my take aways from his talk was that the code generation is producing an unprecedented volume of code that needs to be reviewed and we desparately need better ways of vetting it for reliability. And hopefully code gen now frees us up to focus on bringing back precisely that kind of code analysis that was very popular in the early 2000s but then faded away. 


One colleague I spoke with was in the audience for this talk as well . They had transitioned to our ml platform team from date science and, self analyzed that their coding skills did not have time to catch up because AI coding  arrived just in time and they have been leaning into code gen since it was starting to be a thing a few years ago, and so they have not developed past their coding plateau, however at this point, and perhaps with this conference in particular, they are not yet convinced there is a benefit to get better at writing code. That this skill is less in demand now. 

Personally, I'm of the thought that most code I have generated, has had a low signal to slop ratio. And so I found the main benefit in one off POCs or where I intentionally was building a non-production capability that I otherwise would not have had the time for.  But I don't see myself using code gen in place of real learning opportunities . And building without understanding what I'm building never came naturally to me. Or at least there's a goldilocks sweet spot of understanding where I like to hang out.

Roge Karma points out<sup>[4](#references)</sup> in his article, citing a SemiAnalysis piece<sup>[5](#references)</sup>, deconstructing knowledge work as chunks of Read, Think, Write and Verify. And that makes it a good candidate for building blocks in agentic flows, that can be learned, as long as the criteria are well defined. I pick things up I put things down. In other words, can knowledge work be cut up into units of work that are commoditized. I would flag here that this sounds remarkably similar to the vision of the waterfall software planning model that the agile manifesto<sup>[6](#references)</sup> of 2001 responded too, as well as the Data Science as Pin Factory article<sup>[7,8](#references)</sup> from 2019 written in response to the desire to assembly-line-ify data science. The agile software movement pointed out that software projects are messy and customers cannot accurately describe what they want. And Eric Colson extended this to the messiness of extracting signal from data. In fact his description of the ideal data science pin factory echoes that SemiAnalysis article:
> “one person sources the data, another models it, a third implements it, a fourth measures it”

During the conference, I was chatting with another colleague who was excitedly plotting how she can carve out some EDA time soon--Exploratory Data Analysis time--with an unstructured dataset she has been sitting on, using some new techniques the conference inspired her to try. She believes she would need at least a good 6 months, of, finding time in the cracks of her day job, to determine if there is enough there there in her dataset, before even proposing an improvement that her customer can consider. 

In an interview<sup>[9](#references)</sup> with Peter Steinberger--creator of OpenClaw, an open source agent--, I listened to, he described his niche as  "difficult but not too interesting". This is precisely the opposite of low hanging fruit, the problems that are right there in front of you, easy to understand, easy to describe quick wins. He responds to people who attempt to preplan a backlog of units of work, orchestrating a team of agents to coordinate and execute on the plan:

> *"I don't believe this works. Like, this is the waterfall model of software building. This we learned long ago that this doesn't work. Like, yes, people work differently and maybe it does work for some. I just don't see how this could work for me. Like, I have to start with an idea and often I purposefully under-prompt the agent so it would do something that would give me new ideas. You like maybe like 80% of the things I assumed were like crap, but like there were like two things like, 'oh, I didn't think about that way.'*

> *"And then I iterate and shape the project. And I have to click it. I have to, like, I have to feel it. I feel, to make good software, you know one thing those things often lack is taste. I have to feel like, how does this feature feel? And the beauty now is that features are so easy, I can just, like, throw it away or, like, re-prompt it. My building model is usually very much forward. It's very rarely that I actually revert and have to go back. It's just, like, 'okay, no, then let's change this. No, let's do this.' It's like it's like shaping. I love how this, like, you start with a rock and then you, like, chisel away at it and, like, pick different areas, and then slowly like this statue emerges out of out of marble. That's how I see, that's how I see building something."*

That is a reflection on the creative process. I think if anyone would, Steinberger would be a good judge of how agentic programming can massively speed up your experimentation loop, but it nevertheless is a loop you cannot reduce into a clearly defined deterministic sequence of units you can assign over to your army of agents.

I hear Steinberger's take, more than anything as, that agentic programming is the final nail in the coffin of using product planned roadmaps to derisk quarter long software development efforts. 

Perhaps we can acknowledge though that there are still then two kinds of work in the themes of explore and exploit: spikes that are open ended that produce research artifacts and repetitive tasks that are more well defined because you have done them many times already. And agentic work can perhaps make the first kind easier to bound box.

## An Internet for AI Agents
The first talk I attended was practical. It reminded me of a more fleshed out moltbook.com. Ramesh Raskar laid out a vision<sup>[10](#references)</sup> for how agents can communicate in the future. He pointed out that currently agents are clients and they do not have URI endpoints. And NANDA proposes a DNS for agents among other aspects. 

He also made an intriguing prediction, that in the future, he expects every person will have multiple agents working on their behalf, in agent marketplaces. He had presented this vision for residents of India first, since in India, everyone now already has an Aadhaar card a new identity infrastructure. And a proposal can be for agents to asynchronously in a decentralized way work on the ONDC and UPI. So this makes India very unique. Your agent can represent you in case people want to ask you questions and perform tasks on your behalf. But also he sees a kind of democratization. The agent is called a doot, which is a local word, meaning a messenger. This reminds me of the Shell Game season 1<sup>[12](#references)</sup> actually, where the host attempted to give his agent access to everything about him and used more or less RAG and some agentic loops to handle various tasks for himself. 

I think Ramesh's vision assumes a lot, including the lynchpin that everyone will be an entrepreneur. 

I like the part about freeing up ourselves to not deal with busy work. But yea I have my doubts about everyone managing their own agents. But intriguing nonetheless.

## MCP Travel agency workshop
Cool workshop of mcp-toolbox . This session by Wenxin Du helped make a few concepts on building agent apps click for me.

This along with Sara Zanzoterra session on RAG to Agents as well.

## But then I did some more research on MCP 

This field is clearly being heavily discussed this year. I was trying to track down one article on MCP's demise I had lost the link to and found a lot of activity on this topic!

| Date           | Title                                                                             | Author                                      | Link                                                                                                                                        |
| -------------- | --------------------------------------------------------------------------------- | ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-21     | “MCP is dead, long live CLI”                                                      | Michiel Horstman                            | [medium.com](https://michielh.medium.com/mcp-is-dead-long-live-cli-0fdeba7e7fbf)                                                            |
| 2026-04-21     | “MCP Is Not Dead, It Is Becoming Plumbing”                                        | Predict Publication                         | [medium.com](https://medium.com/predict/mcp-is-not-dead-it-is-becoming-plumbing-0d954794f13a)                                               |
| 2026-04-09     | “The Resurgence of CLI in the Era of AI Agents: Why MCP Is Dead, CLI Is Immortal” | Johnny Chan                                 | [medium.com](https://tsjohnnychan.medium.com/the-resurgence-of-cli-in-the-era-of-ai-agents-why-mcp-is-dead-cli-is-immortal-b90786d99e65)    |
| 2026-04-06     | “MCP is Dead”                                                                     | Nick Babich                                 | [medium.com](https://uxplanet.org/mcp-is-dead-cf16b667ba6d)                                                                                 |
| 2026-03-21     | “MCP is dead or MCP vs Skills — revisited”                                        | Alon Nisser                                 | [medium.com](https://medium.com/%40alonisser/mcp-is-dead-or-mcp-vs-skills-revisited-daaa51b9a519)                                           |
| 2026-03-17     | “MCP Isn’t dead. You’re just using it wrong.”                                     | Theo McCabe                                 | [medium.com](https://medium.com/%40tedisaacs/mcp-isnt-dead-you-re-just-using-it-wrong-cc4f6a162c8f)                                         |
| 2026-03-16     | “MCP Isn't Dead. But It's Not the Default Answer Anymore.”                        | Micheal Lanham                              | [medium.com](https://medium.com/%40Micheal-Lanham/mcp-isnt-dead-but-it-s-not-the-default-answer-anymore-8b88f4ce3224)                       |
| 2026-03-15     | “MCP is dead; long live MCP”                                                      | Hacker News discussion                      | [news.ycombinator.com](https://news.ycombinator.com/item?id=47380270)                                                                       |
| 2026-03-14     | “Is MCP Dead? I Don't Know, But Protocol Will Live Forever”                       | Changshan                                   | [medium.com](https://medium.com/%40changshan/is-mcp-dead-i-dont-know-but-protocol-will-live-forever-9e3cd79c9079)                           |
| 2026 (unknown) | “MCP Is Broken and Anthropic Just Admitted It”                                    | cdcore                                      | [medium.com](https://medium.com/%40cdcore/mcp-is-broken-and-anthropic-just-admitted-it-7eeb8ee41933)                                        |
| 2026 (unknown) | “MCP Is Dead & Here's What's Actually Killing It”                                 | Towards Artificial Intelligence publication | [medium.com](https://medium.com/towards-artificial-intelligence/mcp-is-dead-ece45c1f80bb)                                                   |
| 2025-10-08     | “Is MCP the Wrong Abstraction? (Is that True or Another Clickbait Hype)”          | Level Up / GitConnected publication         | [medium.com](https://levelup.gitconnected.com/is-mcp-the-wrong-abstraction-is-that-true-or-another-clickbait-hype-88a4376dc935)             |
| 2025-06-12     | “Building AI Agents That Actually Do Things: The MCP Revolution”                  | Micheal Lanham                              | [medium.com](https://medium.com/%40Micheal-Lanham/building-ai-agents-that-actually-do-things-the-mcp-revolution-01404de84464)               |
| 2025 (unknown) | “The Great AI Protocol War: How MCP and A2A Are Reshaping the Agent Landscape”    | Micheal Lanham                              | [medium.com](https://medium.com/%40Micheal-Lanham/the-great-ai-protocol-war-how-mcp-and-a2a-are-reshaping-the-agent-landscape-c602a8dde9ca) |


## Back to why planning is hard
Sfould refer back to also Cal Newport multi step automation article<sup>[13](#references)</sup> . Yea . Agent Harnesses and verifiability for each step. 

## Vibing  Abstractions 
Abstractions and modularity are a  useful  principle in software, helping to know the right level of information at any point in time. These days if you want to deploy a website, you dont need to know that the internet is built on TCP/IP, OSPF/RIP/BGP, HTTP, SSL/TLS, DNS and the rest of the alphabet  ocean of protocols. 

#### What would Rich Hickey say here w.r.t. Simple Made Easy and locality of knowledge?
I would wager he would identify Vibe Coding as the ultimate Easy Button , leading to all kinds of    under-the-hood complexities , which allow you to go fast initially, but then slow down dramatically as your tech debt accumulates.

#### slow is smooth smooth is fast
I suspect you can incorporate LLMs into your workflow , jumping up and down to the right level of abstraction as needed, without pretending to be Neo from The Matrix , downloading experience. 

#### What do you need to know
Hearing also 
here<sup>[29](#references)</sup> , similarly , "oh I learned DSA in school but rarely used it on the job". And arguments about how, well just because it is not being used doesn't mean it was not part of the journey, the learning journey. These are kind of the intangible effects I have heard a lot of other people go into as well. 

I might have written this elsewhere already, but going super deep on whatever it is that you do instead of shallow, is perhaps more important than what it is . Because there are so many topics and so many technologies you start and change. But also people say there are those fundamentals.  And skill transfer. 

This connects to the no code topic too.

#### The enjoyment aspect
Can shallow work also can pick away at your soul or your ego? There will be many opinions on whether enjoying what one does is a form of entitlement and that some would say work is called work for a reason of course. However, if you do get a chance to go deep on what you do, it can lead to mastery and that is a big aspect of fulfillment. And technology has changed an endless number of times over the millenia. People have been developing their craft and constantly reinventing themselves over and over again. I come back here also to this book, Range, that is also on this topic. 

## The bitter lesson for software science? 
But ML says hand wiring neural nets  is a kind of artisanal joinery which will never outperform an algorithm like SGD . So is all software engineering just going to software science? 

## AI Skill Flip
I was at the conference founders talk too, Sheamus McGovern, about his book AI Skill Flip.

Hes like yea theres AI  job washing, that there are Amazon layoffs he pointed to where you learn peiple remaijing are picking up the slack. (And side note Amazon was in the news for AI code related outages. ) And yea its a hive mind. He was joking how everyone's conference slides looked like they were generated by Claude. 

But he also noted neverthelesse you  need to read the room. If your company is not doubling down and not helping you reinvent yourself , they will fall behind and take you with them. And reinventing is how he lived his whole life, flipping his career between tech and finance and then finance to data science and then investing. Pivot I guess I realize  was the word perhaps he did not use but sounds right here. 

## And the Productivity Paradox
And Dawn Choo gave a talk about how you appear to be more productive with new tools and therefore you thought that gives you more breathing room. But instead you find more on your plate. She notes instead you are on the wrong part of the pyramid and should use the new AI space everyobe is uncertain about to gain more influence to do less work. Reading Her substack article on this topic too [25], reminds me the why. Because yes everyone is trying to catch up and especially knowledge gaps that  leadership has at your company and you can help be the translation layer which data science has always played anyway as she underlines. 

As well as the same non deterministic probabilistic output I hweard others point out too. Sort of a contradiction. That now you can dump out a loe of plumbing code but it can be subtly wrong so now you have to fix it. The "eval gap" she identifies. 

Since I do see this bug introduction duscussion all throughout this conference I dont know why people arent giving the alternative, dont use this to generate your code necessarily since that is riddled with subtle bugs. Use it to speed up the reviews say instead . ( some companies like Code Rabbit do offer this actually ).

## jack of all trades?
So then what should you know? People talk about T shaped or π shaped knowledge, where you have broad knowledge in many diverse realms and more specialized knowledge in one or two areas.

Does the Vibe era create an incentive to keep everything at a shallow level?

The ultimate generalist jack of all trades? 

The other analogy is that of someone who leans into tech team  management. In that role you shift your time from designing and executing on technical projects, to coordinating projects that a tech team is working on, tracking projects, finding and measuring gaps in execution, coordinating with adjacent teams and with executives. You can share your experience as an IC to level up your IC colleagues and you may try to keep your skills fresh from time to time, rolling up your sleeves, but ypur brain will  proportionally emphasize your glue skills, and your execution muscle memory will become shallow. 

To be fair of course anyone who plays an IC role , is still only hands on with a subset of technology and that subset also shifts as tech itself drifts. 

So the open question then is code gen merely another such shift in kind. Just shifting execution to a  different layer of abstraction, as with compilers say.

Or infrastructure as a service with terraform or aws cdk say. You now dont need to setup your own racks of servers and networks. You just provision compute .  Maybe the answer is about compression. it it lossy or lossless?

Deterministic or non deterministic? 

Makes me consider when corporations started to outsource work internationally in the 2010s. Teams spread across the US are with close time zones but across continents, the overlap is less and coordination tax goes up. But with Agentic outsourcing, there is no time zone difference. 

## Block box ? Explainable?
we have been using deep learning blqck box models a-la-the bitter lesson for a while now, agreeing an algorithm can create a better model than by hand tuned feature engineering. And we have acceptef the black box nature therefore. As long as SHAPley can at least explain/interpret. Same for compiled code. How about code code? It is technically still readable. There is theoretically no reason why code code at least can be readable and minimal without being minified.

## Precision
one of the things Armando said that also stuck, about stochastic nature of code. So hmm were producing all these fun bags of code but wouldnt it be nice if we can be more preciss about vibing, yea sure spec driven development. Oh wait thats what code code was. Deterministic. Nice.

## Mythos and the Halting Problem 
On security now[16] , interesting comparison of Mythos to Y2K. However, host calls code as math, yet, my response would be thst we have such a thing as the halting problem, where we know we cannot predict statically if a program will finish and so by extension, likely we cannot prove bugs are true or actionable statically (my hypothesis ).  

## Worse Than No Code
UML? No Code? That was crap. Here is no code take two.

Actually, vibe coded projects, have precursors, similar in incomprehensibility and or black-box-ness. That is, closed-source or DRM projects.

I believe Armando also made a perl joke during his talk as well; vibe code or code gen as write only code, is not only buggy but also high entropy, low signal to noise. Though verifiable. DRM, closed source, already has threatened open source , with Https://malus.sh , a la Evil Corp, potentially as a joke but maybe not.

But neural code next.js cloudflare vnext is already an example. [21] [22]. Though, to Mo Bitar point on  nature vibe coding hands, with DNA being the neural code, and life being the unit test suite  , yes but the robotics analogy is apt w.r.t. RL, since evolution has no simulation. And thats why it takes millions of years to add a opposable thumb. RL , interacting with the real worl, is the tricky part

A consultant. Create a passable demo then say bye. 

Why is this relevant? Building greenfield is easy. Changing is hard. All the no code low code projects Ive worked on have this theme in common. The initial abstraction works during the demo. But then you want to add more data, change your data model, add another integration. All that is now gated behind your no code solution. Code code is powerful and infinitely extensible, and simply doesnt have this lock in problem. This is discussed in [29] too.

## Hiring advice 
The last talk I attended, by Arturo Natella [17] was about how most job postings cause the right people to self filter in their ambiguity. Lines like "Other duties" are read like "we havent figured out this role yet" . And that often there is a skill wall a "Big List" you are not actually interviewed against. This was less about AI than AI hiring because he was showing a few real job descriptions and then how he would change them. He called this 
"Key Performance Objectives" or KPOs, like an analog to KPIs. 

# References
1. Ivan @ datasaur.ai
2. https://www.theatlantic.com/app/webview/687022/
4. https://www.theatlantic.com/app/webview/687022/?app-privacy=apple-att&articleAudioPlaying=false&color-scheme=auto&fontScale=1#:~:text=As%20a%20group,the%20field%20unique.
5. https://newsletter.semianalysis.com/p/claude-code-is-the-inflection-point
6. agile manifesto
7. https://multithreaded.stitchfix.com/blog/2019/03/11/FullStackDS-Generalists/
8. https://hbr.org/2019/03/why-data-science-teams-need-generalists-not-specialists

9. https://youtu.be/8lF7HmQ_RgY&t=4180

10. Ramesh Raskar, https://nanda.media.mit.edu
11. Armando Solar-Lezama, "Open Challenges for the Next Generation of Programming Agents" , https://x.com/_odsc/status/2047815353967780118 
12. Shell Game podcast, season 1
13. Cal Newport 2026 Feb New Yorker article about automation

14. Rich Hickey  , "Simple Made Easy" 

15. adversarial coding https://github.com/sepiariver/GAN-coding
16. security now, mythos, https://podcasts.apple.com/us/podcast/security-now-audio/id79016499

17. Arturo Natella https://www.goamaru.com

18. https://developers.cloudflare.com/changelog/post/2026-04-20-kimi-k2-6-workers-ai/
19. https://www.youtube.com/watch?v=Yxlb0-zTURo , RAmesh Raskar 
21. Https://malus.sh
22. https://youtu.be/ateDMU5EGeg , Mo Bitar on next.js and cloudflare 
23. Two Bubbles, the token costs and tokrn inflation Anthropic April 2026 https://open.substack.com/pub/techtrenches/p/the-ai-industrial-transformation?r=d7b46&utm_medium=ios

25. Dawn Choo , https://open.substack.com/pub/askdatadawn/p/the-data-career-is-evolving?r=d7b46&utm_medium=ios

26. OpenCode founder on productivity with AI code tools, https://blog.codacy.com/the-creator-of-opencode-thinks-youre-fooling-yourself-about-ai-productivity
27. interesting augmentation radiology example, 11:03 , https://youtu.be/eSABedBwZjQ 

28. https://uxplanet.org/mcp-is-dead-cf16b667ba6d 
29.  "I don't like Programming" | Prime Reacts, https://youtube.com/watch?v=r6EXZcTJyaA

30. Book, Range

<sup>[x](#references)</sup> 

