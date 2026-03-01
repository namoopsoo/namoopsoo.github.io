---
title: "Immich to Vimeo"
# slug: "2025-06-01--immich-to-vimeo"
date: 2026-03-01T14:43:17-05:00
# draft: true

# optional thumbnail
images:
  - "THUMBNAIL_PLACEHOLDER"
cover:
  image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->

Into my immich journey I tried out a way to upload videos to vimeo straight from immich, with the vimeo REST API.

Added a small upload script here, https://github.com/namoopsoo/manage-my-photos/blob/main/vimeo/upload.py , 

which just requires a `VIMEO_TOKEN` defined as an env variable

```sh
python vimeo/upload.py --local-path /path/to/file.mov
```
