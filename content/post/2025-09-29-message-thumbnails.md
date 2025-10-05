---
title: Thumbs Up
date: 2025-09-29
---
## Who has two thumbnail learnings about hugo blog post images? 😀👍👍

Note that I finally learned how to make hugo blog links sent by imessage have thumbnails and I re-learned how to make hugo blog posts thumbnails show up.

So as far as text message thumbnails go, apparently, since my images live on s3, I needed to make sure their content type was `image/jpeg` because in my case they were `binary/octet-stream`. 

First blog post where I fixed this was here<sup>[1](#references)</sup>.

## Content-Type update
The way to change that, was to run, 

```
aws s3api copy-object \
  --bucket my-blog-content \
  --copy-source my-blog-content/2025-09-28-fix-chipped-pint-glass/IMG_7717.jpeg \
  --key 2025-09-28-fix-chipped-pint-glass/IMG_7717.jpeg \
  --metadata-directive REPLACE \
  --content-type image/jpeg \
  --cache-control "public, max-age=31536000, immutable" \
  --acl public-read
```
from the cli, because this capability was not available for update from the console itself.

## The yaml front matter matters too
And if you want an image to be that thumbnail , for the purposes of the hugo index and also for the text message, I had to add the message to the front matter in two different ways 

```yaml
---
title: blahblah
images:
  - "https://s3.amazonaws.com/my-blog-content/2025-09-28-fix-chipped-pint-glass/IMG_7717.jpeg"
cover:
  image: "https://s3.amazonaws.com/my-blog-content/2025-09-28-fix-chipped-pint-glass/IMG_7717.jpeg"
---
```

## Scale it though
That seemed to work as a one off but I would like to batch update all previous content too.

# References
1. https://michal.piekarczyk.xyz/post/2025-09-28-fix-chipped-pint-glass/


{{< figure src="https://s3.amazonaws.com/my-blog-content/2025-09-29-message-thumbnails/2025-10-05---12_38_55.png" width="50%">}}