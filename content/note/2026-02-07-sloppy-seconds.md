---
title: The Good the bad and the ugly of AI benefit shortfalls
date: 2026-02-08
---

I'm reading AI Snake Oil, and the authors intro by saying they will focus on the examples of AI that harm and they will not include the ones that benefit society. But it is not straightforward to create a list of the good examples. I think one of their examples in the good column was autocorrect. But auto orrect is a good example of where you can't just sprinkle AI on a problem to solve it. You need to put a lot of effort to get the UX right. 

I was personally getting very frustrated when using the apple keyboard version of swipe typing because I would spend just way too much time not getting the word I intended, hitting backspace, trying again and again, giving up and typing it in manually. Actually I was not alone. Typewise, created a keyboard alongside published research showing you save time if you type letter by letter, and instead apply auto correction when you misspell common words. I have been using typewise for a few yeats now, but it has also caused me a lot of pain with its UX issues. I described one [3], where its autocorrect "undo", which is what you press if the correction is wronr, overwrote the autocomplete of the app you are using. In my case, I was using Logseq, which auto-completes your node names, so when typewise attempts to correct , hitting undo it ignores the state change performed by the app and puts you into an irreversible state. The only solution is to shake your phone, which triggers a system Undo, which works, but that feels terrible because you keep shaking your phone 😆, which compounds the anger. Plus the local model doesn't learn from the system undo so there is no way to prevent this from happening again. 


Typewise actually has a nice page for submitting and upvoting bugs and issues. I love that they have this but it suffers from the papercuts problem described at Amazon, that is, problems that are affecting a very small minority usually go unsolved for a long time.  

I dont know if my problem ever got solved. I gave up. I ended up giving up on logseq mobile because the mobile experience was just too slow. So I am waiting for logseq mobile to speed up and in the meantime I have fewer typewise autocorrect pain points 😀.

But haha that was a long epicycloid on autocorrect not necessarily being a straightforward benefit of AI/ML. You need good UX research to drive it home. Actually typewise also claims their autocorrect is way better if you give it permission to talk to its cloud LLM model. I'm glad I at least have a choice in the matter, because as much as I may end up suffering from not ideal autocorrect, I will gladly hold out on a local or private Transformers model that I don't have to trust to be a custodian of everything I type! 

## RAG search
I think one of the examples in the good column, is search, especially local corpus search! In typing here, I was able to quickly look up on the search *"where is the article I had about typewise?"* and in just 5 seconds, I got back just what I was looking for. I recently setup the Cloudflare auto RAG AI search [5] for this blog. (Found that link in the same way!)

<<auto-RAG-search-screenshot>>

## Real estate listing furnishing AI
The reason I opened up this page was to note [1] this interesting example in The Atlantic about how the current state of using gen AI to auto furnish --*autocorrect 😉?*--an empty unit is creating some weird disappointmentsh from potential clients who were not aware that AI was used to furnish the listing in question . 



# references
1. https://www.theatlantic.com/app/webview/685871/?app-privacy=apple-att&articleAudioPlaying=false&color-scheme=auto&fontScale=1#:~:text=house%20in%20a,feel%20let%20down.%E2%80%9D 
, The Unsettling Rise of AI Real-Estate Slop , Franklin Schneider

2. AI Snake Oil
3. https://michal.piekarczyk.xyz/post/2024-05-24-typewise-plus-logseq/

4. link to typewise autocorrect research paper
5. https://michal.piekarczyk.xyz/note/2026-01-25-hook-up-cloudflare-rag-search/



