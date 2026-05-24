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

## Dump from photos to laptop then upload then delete
Initially I tried osxphotos [2] to export any remaining photos from my Photo library but it just had too many misses. I describe a it more on this in a section further below. So I went back to exporting from Apple Photos, their plain manual UI. This took an insane amount of patience, so much clicking!

After exporting to a location on my laptop disk, then, I used this node.js npm tool described here [1]. So `npm` is a prerequisite and then you can install it `npm i -g @immich/cli`.  You setup an API key env variable straight from your immich server.

```sh
IMMICH_API_KEY=<api-key-from-immich>
```

And then you login, like 

```sh
immich  login-key https://<your-immich-server> $IMMICH_API_KEY
```
and finally upload, importantly with the `--recursive` and `--delete` flags.

```sh
$ immich upload /some/path/to/your/apple-photo-exports --delete  --recursive
Crawling for assets...
Hashing files           | ████████████████████████████████████████ | 100% | ETA: 0s | 4455/4455 asses
Checking for duplicates | ████████████████████████████████████████ | 100% | ETA: 0s | 4455/4455 asset
Found 579 new files and 3876 duplicates
Uploading assets | ███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ | 16% | ETA: 50s | 112.2 MB/677.1 MB
```

however, the `--delete` only seems to work with what gets uploaded and not on duplicates. And so afterwards you have to manually `rm -rf /some/path/to/your/apple-photo-exports` to get rid of any remaining duplicates.

### Excerpt from osxphotos

From [3], osxphotos very thoughtfully and probably painstakingly describe,  the below. I really really really wanted this to work, but I kept on discovering I had photos that I saw in my photos library that did not get exported through osxphotos. After more research I settled on Apple photos just being incredibly unreliable from third party access like per osxphotos. The locked in Apple ecosystem  is one of the reasons why I was so desparate to get away. I really apprecite what the authors here tried to do but Apple either changed something or I wasn't patient enough, but I begrudgingly went back to using the Apple UI Photos interface for exporting. Because that appeared to be the only way to reliably summon all the photos that got stuck in icloud land.

> osxphotos works by copying photos out of the Photos library folder to export them. You may see osxphotos report that one or more photos are missing and thus could not be exported. One possible reason for this is that you are using iCloud to synch your Photos library and Photos either hasn't yet synched the cloud library to the local Mac or you have Photos configured to "Optimize Mac Storage" in Photos Preferences. Another reason is that even if you have Photos configured to download originals to the Mac, Photos does not always download photos from shared albums or original screenshots to the Mac.

> If you encounter missing photos you can tell osxphotos to download the missing photos from iCloud using the --download-missing option. --download-missing uses AppleScript to communicate with Photos and tell it to download the missing photos. Photos' AppleScript interface is somewhat buggy and you may find that Photos crashes. In this case, osxphotos will attempt to restart Photos to resume the download process. There's also an experimental --use-photokit option that will communicate with Photos using a different "PhotoKit" interface. This option must be used together with --download-missing:

> `osxphotos export /path/to/export --download-missing`

> `osxphotos export /path/to/export --download-missing --use-photokit`

# References
1. https://immich.app/docs/features/command-line-interface/#installation-npm
2. https://rhettbull.github.io/osxphotos/tutorial.html
3. https://rhettbull.github.io/osxphotos/tutorial.html#missing-photos
