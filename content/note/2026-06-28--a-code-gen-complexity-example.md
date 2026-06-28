---
title: "Code Gen Complexity Example"
# slug: "2026-06-28--a-code-gen-complexity-example"
date: 2026-06-28T16:18:29-04:00
# draft: true

# optional thumbnail
# images:
#   - "THUMBNAIL_PLACEHOLDER"
# cover:
#   image: "THUMBNAIL_PLACEHOLDER"
---

<!-- Write your intro paragraph here. -->
I noticed, mentioning here<sup>[1](#references)</sup> also, how images with spaces display fine on logseq will not display on  github. But also that I learned about the hack to wrap paths with `<>` to support both without having to rename filenames like I had done in the past. Well I used codex to create a utility for this into my logseq_utils repo, and that ended up being a cool code gen complexity example.

So with my original prompt, 
> i want to create a simple utility function that can take a string and convert the image markdown which may or may not have spaces , or other special characters like parentheses that filenames can have , and wrap the path with angle brackets, `<>` , for example `![image.png](../assets/some image with spaces.png)` becomes `![image.png](<../assets/some image with spaces.png>)`  and `![image.png](../assets/some other image okay (2).jpeg)`  becomes `![image.png](<../assets/some other image okay (2).jpeg>)` and `![image.png](../assets/blah-image-no-spaces-213.png)` becomes `![image.png](<../assets/blah-image-no-spaces-213.png>)`

I ended up with a PR from codex<sup>[2](#references)</sup>, that took a interesting nested while loop approach. I think it's safe to say that a regex is the more intuitive approach which gives you a one or two liner basically. When I prompted for that, I did get that on the next try from codex, in that same PR, as the second commit.

> great. looks like it works nicely. however this func `wrap_image_markdown_paths` can probably also be written using a regex instead , I think, to make it much simpler , right ?

So it is a cherry picked example, but I think this is super common and slightly mysterious.

## References
1. https://michal.piekarczyk.xyz/note/2026-06-28--markdown-image/
2. https://github.com/namoopsoo/logseq_utils/pull/9

