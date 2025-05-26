---
date: 2025-05-16
title: apple iphoto to immich
---
_draft_
A few weeks ago stumbled upon an amazing Apple iPhoto alternative, immich, a self hosted photo server, and I have been on the journey to migrate but wow Apple has been shining exceptionally in maintaining its deathgrip on my assets, relentlessly reaffirming why I am trying to get off Apple Photos.

Immich gives you the control Apple Photos lacks and it has really nice UI elements too.

## Willing to serve
Seeimg the bustling development on the [immich github](https://github.com/immich-app/immich) and pleased to see both geolocation pinching goodness and time granularity on a nice [demo site](https://demo.immich.app/),  I started flipping through the [nice looking docs](https://immich.app/docs/overview/welcome), but I did not easily notice how I can start serving my immich instance in the cloud. Doing some more online reading, I realized home self-hosting is the reason why. 

I dug around for a mini computer I have in my spare parts, but I realized I don’t have a hard drive that fits at the moment, so I opted for the costlier but faster EC2 approach.

##  Making moves
How do I migrate my photo collection? You can simply export photos from the apple photos menu, but struggled to do this because photos was already taking up disk space on my laptop, so I found it counter intuitive to be doubling the disk space I was using by the same photos. Also I did not have as much free disk space to spare.

> In retrospect, a kind of a batch export using the photos GUI actually would indeed have been the most straightforward way.

So I tried to understand how can I dig out the photos which were already taking up space on my disk instead.

One initial step I took was to download the immich mobile app, and this over the course of a few days, ended up transfering lots of my photos over to my server.

