---
title: "Terminate Your Photos"
date: 2025-05-17
# draft: true

# optional thumbnail
images:
  - "THUMBNAIL_PLACEHOLDER"
cover:
  image: "THUMBNAIL_PLACEHOLDER"
---
Continuing, my apple to immich experience, spending a lot of time on my immich bash terminal, I often had the need to look at my photos but bash is headless of course. 

Yes, of course immich is a browser based photo server of course, but often I found myself needing to look at some specific photo more quickly without finding it wihin the immich gui. 

## Enter chafa<sup>[2](#references)</sup>
I had the need and an idea of just using maybe ascii art to help and found someone had already done this and it was called `chafa`! Image to text redefined haha.

Here is an example I had looked up at one point.
```
chafa --colors=8 --symbols=ascii  --size=100x40  '/mnt/immich-storage/library/blah/blah/blah/2025/2025-04-24/2025-04-24 23.40.18.jpg'
```

{{< row >}}
{{< column >}} 

{{< figure src="https://s3.amazonaws.com/my-blog-content/2025-05-17-terminate-your-photos/image_1747506902784_0.png" width="70%">}}
 {{< /column >}}
{{< column >}} 
{{< figure src="https://s3.amazonaws.com/my-blog-content/2025-05-17-terminate-your-photos/image_1747506891839_0.png" width="70%">}}
 {{< /column >}}
{{< /row >}} 


One more example, of a nice house.

{{< row >}}
{{< column >}} 
{{< figure src="https://s3.amazonaws.com/my-blog-content/2025-05-17-terminate-your-photos/image_1769973325077_0.png" width="70%">}}
 {{< /column >}}
{{< column >}} 
{{< figure src="https://s3.amazonaws.com/my-blog-content/2025-05-17-terminate-your-photos/image_1747510049617_0.png" width="70%">}}
 {{< /column >}}
{{< /row >}} 



# References
1. https://michal.piekarczyk.xyz/post/2025-05-16-apple-iphoto-to-immich/ 
2. https://hpjansson.org/chafa/ , Hans Petter Jansson

