---
date: 2025-05-16
title: apple photos to immich
---
_draft_
A few weeks ago stumbled upon an amazing Apple iPhoto alternative, [immich](https://immich.app/), a self hosted photo server, and I have been on the journey to migrate but wow Apple has been shining exceptionally in maintaining its death-grip on my assets, relentlessly reaffirming why I am trying to get off Apple Photos.

Immich gives you the control Apple Photos lacks and it has really nice UI elements too.

## Willing to serve
Seeing the bustling development on the [immich github](https://github.com/immich-app/immich) and pleased to see both geolocation pinching goodness and time granularity on a nice [demo site](https://demo.immich.app/),  I started flipping through the [nice looking docs](https://immich.app/docs/overview/welcome), but I did not easily notice how I can start serving my immich instance in the cloud. Doing some more online reading, I realized home self-hosting is the reason why. 

I dug around for a mini computer I have in my spare parts, but I realized I don’t have a hard drive that fits at the moment, so I opted for the costlier but faster EC2 approach.

##  Making moves
How do I migrate my photo collection? You can simply export photos from the apple photos menu, but struggled to do this because photos was already taking up disk space on my laptop, so I found it counter intuitive to be doubling the disk space I was using by the same photos. Also I did not have as much free disk space to spare.

> In retrospect, a kind of a batch export using the photos GUI actually would indeed have been the most straightforward way.

So I tried to understand how can I dig out the photos which were already taking up space on my disk instead.

One initial step I took was to download the immich mobile app, and this over the course of a few days, ended up transferring lots of my photos over to my server.

## Just between you and me
Photos from conversations, appear in Apple photos, but only on your phone, and I was puzzled why I didn't see them on my computer. The reason when you think about it makes sense though, maybe you do not want all photos someone sends you to automatically import to your photos. Fair! So I had to do some manual review, clicking save . And yea the context of who the photo is from helps. But what ended up happening often times was after I imported these to immich, many photos dates were messed up I think because they were sent with scrubbed EXIF. So immich, in lieu of Creation Date will fallback to other dates available. And GPS data for many photos like this was also totally gone. Some I have manually fixed, but many, are free floating. As I write this, I realize probably I can query for the photos directly without the expected EXIF. 

## From backups
But yea ha ha I have a few  islands of photos , similarly, to conversations, of imports , from dumps from other locations too , that had EXIF mysteriously scrubbed, so I found a few dates with several hundreds of photos just hanging out.
Probably will fix this later, but I don't want to go into this rabbit hole at the moment. But it can drive you a bit crazy, when you are deleting photos on the Apple Photos side, because for these orphaned photos on immich, you cannot easily find them.