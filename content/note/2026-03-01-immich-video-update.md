---
title: "Immich to vimeo Update"
date: 2026-03-01T16:17:52-05:00
draft: true

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

But it worked seamlessly.

# References
1. https://github.com/namoopsoo/manage-my-photos/blob/main/vimeo/upload.py
2. https://developer.vimeo.com/api/reference/videos#upload_video
3. https://michal.piekarczyk.xyz/note/2025-06-01--immich-to-vimeo/{{< figure src="https://s3.amazonaws.com/my-blog-content/2026-03-01-immich-video-update/image_1772400772117_0.png" width="50%">}}