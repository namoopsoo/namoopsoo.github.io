---
title: "Immich to vimeo Update"
date: 2026-03-01T16:17:52-05:00
draft: false

# optional thumbnail
images:
  - "https://s3.amazonaws.com/my-blog-content/note2026-03-01-immich-video-update/image_1772396160156_0.png"
cover:
  image: "https://s3.amazonaws.com/my-blog-content/note2026-03-01-immich-video-update/image_1772396160156_0.png"
---

I was trying to use chat gpt codex to save myself a few minutes, to add two new vimeo rest api parameters, `name` and `description` , to my upload script I mentioned earlier<sup>[3](#references)</sup>. I encountered a `500` and so I could not create a PR. 


{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-03-01-immich-video-update/image_1772400657943_0.png" width="50%">}}
however the cool thing is that I learned about the `git apply` capability, which somehow I did not realize existed .

{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-03-01-immich-video-update/image_1772400772117_0.png" width="50%">}}

But it worked seamlessly, with just taking the patch and `git apply codex.patch`. 

## Frivolity

I use this script in particular to upload to vimeo from my immich. And prior to my patch here, of adding `name` , I had found it amusing that I uploaded the video that is the image for this post, because it reminds me of The Untitled Goose game<sup>[4](#references)</sup>, which I have not played haha in quite some time.

## ugrep, ug 

One more cool note, is that I had found my original notes for my immich to vimeo upload by finally finding out about and using ugrep<sup>[5](#references)</sup>, which unlike `ag`, the silver searcher, can take a search like, what I used, and point out files where multiple terms exist in a file, but in an unknown order on possibly multiple lines

```sh
ug -%% 'vimeo immich' my_notes/
```
And this brought me to my exact notes from haha, 10 months ago, where I created the upload script<sup>[1](#references)</sup> in question and proceeded to completely forget about it. I then added<sup>[3](#references)</sup> , retrospectively, a note of what I learned as of that date 10 months ago. 

Anywyay, looking forward more time saved by ugrep!


# References
1. https://github.com/namoopsoo/manage-my-photos/blob/main/vimeo/upload.py
2. https://developer.vimeo.com/api/reference/videos#upload_video
3. https://michal.piekarczyk.xyz/note/2025-06-01--immich-to-vimeo/
4. https://goose.game/
5. https://manpages.ubuntu.com/manpages/noble/man1/ugrep.1.html
