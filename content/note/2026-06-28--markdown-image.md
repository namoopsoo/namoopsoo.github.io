---
title: "Cool Markdown Image hack"
# slug: "2026-06-28--markdown-image"
date: 2026-06-28T14:29:58-04:00
# draft: true

# optional thumbnail
# images:
#   - "THUMBNAIL_PLACEHOLDER"
# cover:
#  image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->


if an image in logseq has the form 
```sh
![image.png](../assets/some image with spaces.png)
```
that displays fine on logseq but does not display on github. On github, without changing the filename you can however replace spaces with `%20` 

```sh
![image.png](../assets/some%20image%20with%20spaces.png)
```
but that doesn't work on logseq.  However interestingly, though according to this [link](https://talk.commonmark.org/t/whitespace-in-image-paths/1121) I found per a google search, common mark supports one alternative that works in both logseq and github markdown ! 

```sh
![image.png](<../assets/some image with spaces.png>)
```
