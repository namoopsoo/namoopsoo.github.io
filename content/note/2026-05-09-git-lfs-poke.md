---
title: "Git Lfs Poke"
# slug: "2026-05-09-git-lfs-poke"
date: 2026-05-09T12:50:14-04:00
# draft: true

# optional thumbnail
images:
  - "THUMBNAIL_PLACEHOLDER"
cover:
  image: "THUMBNAIL_PLACEHOLDER"
---

While I was reviewing my git lfs based logseq markdown backup, I noticed a git lfs inconsistency. 

So 
```sh
git lfs fsck
```
reported 339 .PNG files as `pointer: unexpectedGitObject: "assets/IMG_4942.PNG" (treeish 53f01b6616262c6e9bcb6eabb3cc11cb298fab1c) should have been a pointer but was not`, even though when I looked at my `.gitattributes` I did see `*.PNG filter=lfs diff=lfs merge=lfs -text`.

The numbers suggested my .PNG however was not on my git-lfs.
```sh
$ git lfs ls-files |wc -l 
1715
```
and 
```sh
$ ls -1 assets/*.PNG |wc -l 
338
```
and
```sh
$ ls -1 assets|wc -l
2077
```

I believe I had run into this before. So I had added .PNG into my .gitattributes but I did not migrate. And well now all new .PNG are git lfs  going forward but not backwards. This appears to be a rare .PNG uppercase format. Most of my screenshots are .png . 

Ok so to migrate I did 
```sh
$ git lfs migrate import --no-rewrite -- assets/*.PNG
migrate: checkout: ..., done.
```
and that added a new git commit, moving all of those .PNG to lfs. And now my next git push I saw the conversion.
```sh
$ git push origin $(git current )
Uploading LFS objects:   4% (14/337), 92 MB | 12 MB/s
```
That `--no-rewrite` means don't rewrite git history. Less risky. 

And now a final consistency check, `git lfs fsck`, now just has two odd .PNG files and not 339. And looks like most are in there except for 1.

```sh
$ git lfs ls-files|grep '.PNG$'|wc -l
     338
```
