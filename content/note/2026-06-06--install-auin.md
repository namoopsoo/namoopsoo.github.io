---
title: "Reverse search and Atuin"
# slug: "2026-06-06--install-auin"
date: 2026-06-06
# draft: true

# optional thumbnail
images:
  - "THUMBNAIL_PLACEHOLDER"
cover:
  image: "THUMBNAIL_PLACEHOLDER"
---

I was interested in improving my reverse search `Control R` experience on my shell because many of my previous commands are not easily searchable or they disappear too fast. 

Initially I just wanted to figure out if you can use fzf for the reverse-search, but ChatGPT made me aware of atuin too. This sounded super fancy and the atuin<sup>[1](#references)</sup>  idea of using a local sqlite db for a command cache looked interesting, so I tried to `brew install atuin` first.

## I have an intel x86 mac, so home brew installing atuin took over 7 hours. 

I had some spare time, so I did see that indeed, the releases<sup>[2](#references)</sup> only have x86_64 releases for linux and windows, but not for macos.

Looks like this took a long time in particular, because atuin is built in rust and also incidentally the rust toolchain to build atuin was needed, including llvm which itself took over 5 hours to build.


```
🍺  /usr/local/Cellar/cmake/4.3.3: 4,041 files, 71.3MB, built in 23 minutes 4 seconds
🍺  /usr/local/Cellar/googletest/1.17.0: 76 files, 2.4MB
🍺  /usr/local/Cellar/abseil/20260107.1: 806 files, 11.1MB, built in 1 minute 35 seconds
🍺  /usr/local/Cellar/protobuf/35.0: 373 files, 17.6MB, built in 17 minutes 51 seconds
🍺  /usr/local/Cellar/ca-certificates/2026-05-14: 4 files, 201.0KB
🍺  /usr/local/Cellar/openssl@3/3.6.2: 7,618 files, 38MB, built in 12 minutes 46 seconds
🍺  /usr/local/Cellar/libssh2/1.11.1_1: 201 files, 1.3MB, built in 29 seconds
🍺  /usr/local/Cellar/llhttp/9.4.1: 15 files, 146.2KB, built in 5 seconds
🍺  /usr/local/Cellar/pkgconf/2.5.1: 28 files, 472KB
🍺  /usr/local/Cellar/libgit2/1.9.4: 109 files, 5.0MB, built in 1 minute 27 seconds
🍺  /usr/local/Cellar/readline/8.3.3: 56 files, 2.6MB, built in 32 seconds
🍺  /usr/local/Cellar/sqlite/3.53.2: 13 files, 5.3MB, built in 53 seconds
🍺  /usr/local/Cellar/xz/5.8.3: 96 files, 2.6MB, built in 1 minute 11 seconds
🍺  /usr/local/Cellar/expat/2.8.1: 23 files, 727.8KB, built in 25 seconds
🍺  /usr/local/Cellar/python@3.14/3.14.5: 9,679 files, 238.1MB, built in 11 minutes 27 seconds
🍺  /usr/local/Cellar/z3/4.15.4: 120 files, 35.1MB, built in 15 minutes 22 seconds
🍺  /usr/local/Cellar/ninja/1.13.2: 10 files, 462.8KB, built in 51 seconds
🍺  /usr/local/Cellar/swig/4.4.1: 833 files, 6.1MB, built in 52 seconds
🍺  /usr/local/Cellar/llvm/22.1.6: 9,638 files, 1.7GB, built in 311 minutes 20 seconds
🍺  /usr/local/Cellar/rust/1.96.0: 4,791 files, 395.9MB, built in 81 minutes 42 seconds
🍺  /usr/local/Cellar/atuin/18.16.1: 15 files, 33.8MB, built in 10 minutes 29 seconds
```

## fzf in the meantime
Actually since I already had `fzf` from earlier, from attempting to use fuzzy search for another reason, I learned that adding `eval "$(fzf --bash)"` to my `~/.bash_profile` was enough to set fzf to replace the bash `Control R` search.

This worked pretty well actually, with fuzzy search allowing you to type, missing letters in your commands. 

However, fzf out of the box doesn't appear to be good with typos I am realizing, though the improvement might be good enough for what I need.

## atuin finished installing
Didn't get a chance to try it out yet haha, but will see if just fzf helps me enough. The atuin learning curve seems slightly high. But I also started trying out just<sup>[2](#references)</sup>, which seems to handle lots of use cases as well.

## References
1. https://atuin.sh/
2. https://github.com/atuinsh/atuin/releases 
3. https://just.systems/man/en/
