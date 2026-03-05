---
date: 2026-03-04
title: prompt-driven-development
draft: false
---

lack of clarity what to do next? write it out as if you were to prompt a LLM tool like ChatGPT , but instead the prompt is for you .

Prompting seems to have rewired my brain  , over the past three years, to focus into words, into highly descriptive narrative, what I want , knowing my words need to be free of noise.

This is to the point now Ill often start writing a prompt in a Chat window or a message to a friend or colleague at work, and Ill stop, realize that writing helped me organize my thoughts and I no longer need to even ask the question.

Mzybe Prompt Driven Debelopment, much like blog post driven development or Documentation Driven Development, is just another way to   load your very own meat key value cache that allows you to realize what is next.

Same like setting up a problem right before going to sleep, for a shower, etc.

Duck programming and pair programming. yet another way to access our thoughts.

# Reasoning 
But it is funny how there is so much back and forth borrowing between humans and LLMs and the techniques are not guaranteed to help.

So [1] discusses how different inference time scaling approaches have mixed benefits for different problem domains. I am sort of understanding that "inference time scaling" is literally what is meant by "reasoning", and these are a handful of ways of saying more to answer the same prompt --aka using more tokens, hence the "scaling"--but is it really what "reasoning" is? 

The techniques are, (1) chain-of-thought --which is literally just prompting to think out loud without any code written to make that happen other than RLHF to reinforce it--, (2) parallel scaling with aggrrgation , and (3) and sequential scaling .

In parallel scaling, I suppose some code has to be wrtten, to run a model multiple times from the same state, at high temperature, and the somehow vote for the best response. The model can also be its own critic or the average can be taken. And sequential scaling requires feedback at each step. I think tooling can also be used to provide the critical feedback. For writing a program, a unit test is a perfect example, but there can be other heuristics.

The authors indicate different problem domains benefit from these additional tokens differently. Coding, I think can definitely benefit if maybe the tooling critic is a linter or a terminal to check if the code runs or produces n epected outcome. But I see other domains dont have the benefit of verifiabiliyy like I dont know, writing an email.

Side note, realizing (2) parallel and (3) sequential, are kind of like Random Forests vs Gradient Boosted Trees. Voting vs iteratively attacking errors.

## Back to is this really reasoning and does it help humans

Well, how do humans reason? we can often just stare at a wall and an answer will arrive, but oddly enough, going for a walk or taking a shower famously, activates some kind of unconscious processing or pruning. I think Barbara Oakley [2] has emphasized that free association with what you already know is kind of the magical step. And [3] James Clear and Huberman kind of describe--or admit really--that you have no output without input. That is, your insights are sort of dependent on what you have loaded into your mindspace more or less recently, like last few days or weeks or months. 

## Rumination 
But it doesnt always help. I think George Montañez [4] has pointed out that chain of thought doesnt necessarily yield to better outcomes for LLMs and I think if humans ruminate, we can get stuck as well. 

So interestingly, unplugging yields better results for peraps both humans ans LLMs? Sometimes we just need a reset, to clear that cache and try again later :). 




# references
1. https://arxiv.org/pdf/2504.00294v1 inference time scaling 
2. learning how to learn 
3. Huberman and James clear interview
4. https://youtu.be/ShusuVq32hc , George Montañez 


