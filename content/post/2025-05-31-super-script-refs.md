---
title: super scripts
date: 2025-05-31
---
# adapting super script references
I was mentioning in another post<sup>[1](#references)</sup> about switching from hyperlinks to citation style links thanks to seeing Doug Slater’s<sup>[2](#references)</sup> use of this technique. I am sure I have seen it elsewhere too but I forget. 

# how to use the new technique 
- An inline reference is simply "some text`<sup>[1](#references)</sup>`", which has a corresponding `1. blahblah` at the references at the end
- To make sure hugo allows the custom `<sup>` html you need in your config.yaml or config.toml something like     

    ```yaml
    markup:
      goldmark:
        renderer:
          unsafe: true    
    ```
- and optionally you can spice up your hugo papermod<sup>[3](#references)</sup>, adding some color to a custom css, `assets/css/extended/my_custom_super.css` like 

    ```css
    sup a {
        color: #666;
    }
    ```


# Thanks
Also I definitely did not know about the goldmark and css tips off the top of my head. This advice came from ChatGPT when prompted about hmm why wasn't the `<sup>` lighting up when I tried it out for the first time. 

# references
1. [other post](https://michal.piekarczyk.xyz/post/2025-05-31-tabs-vs-spaces/#wherever-you-go-there-you-are) 
2. [Doug Slater](https://www.slater.dev/accelerated-incompetence/)
3. [hugo papermod](https://github.com/adityatelange/hugo-PaperMod)