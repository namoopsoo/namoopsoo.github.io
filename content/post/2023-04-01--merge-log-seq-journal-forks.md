---
title: Merge log-seq journal forks
date: 2023-04-01
---

### This is what happens to me 
When editing with https://logseq.com , on my phone, laptop and ipad, I end up seeing this 

```sh
$ fd ' ' journals/
journals/2021_03_13 2.md
journals/2021_05_30 2.md
journals/2021_10_17 2.md
journals/2022_01_23 2.md
journals/2022_05_15 2.md
journals/2022_06_11 2.md
journals/2022_07_16 2.md
journals/2022_08_21 2.md
journals/2022_09_01 2.md
journals/2022_09_07 2.md
journals/2022_09_07 3.md
journals/2022_09_10 2.md
journals/2022_09_26 2.md
journals/2022_10_22 2.md
journals/2022_10_22 3.md
journals/2022_12_14 2.md
journals/2023_01_12 2.md
journals/2023_02_04 2.md
journals/2023_03_10 2.md
journals/2023_03_21 2.md
```

I think this is mostly happening when you start editing a file before a icloud sync has had a chance to take place.

### Look at the forked files 
Since this is rare and my daily journal files are not too intense, I just wanted to look at everything, so I did it like this,

```sh
fd ' ' journals/ |xargs  -I {} sh -c 'echo "file: {}" ; arr=({}); first=${arr[0]};echo "first thing $first" ; for file in ${first}*; do echo  "============="; echo "$file";echo "============="; cat "$file";echo  ; done'
```

#### Actually the above one-liner  is hard to read
So I put it into https://github.com/namoopsoo/handy/blob/master/bash/logseq-fork-display-helper.sh , 

```sh
# (helper script for quickly displaying logseq journal files that have forked off)
# Takes as a parameter a filename that has spaces in it,
#   applies a glob to the first substring when splitting by spaces, 
#   and cat all the files that are available when using that glob.
file=$1
echo "file: $file" ; arr=($file); 
first=${arr[0]};
echo "first thing $first" ; 
for file in ${first}*; 
	do echo  "============="; 
    echo "$file";echo "============="; 
    cat "$file";echo  ; 
done
```

#### And just using that like, 

```sh
fd ' ' journals/ |xargs  -I {} /blah/path/to/my/handy/bash/logseq-fork-display-helper.sh {}
```
which shows me, 

```sh
file: journals/2021_03_13 2.md
first thing journals/2021_03_13
=============
journals/2021_03_13 2.md
=============
something here oh wow 

=============
journals/2021_03_13.md
=============
oops something else though


```

I realized, sometimes the above forks are completely different, but also the changes are just a few lines,
so I just used `vimdiff "journals/2021_03_13 2.md" journals/2021_03_13.md` to help me resolve the diffs.

#### Actually a bunch of them ended up being somehow identical
So checking hash first 

```sh
md5 "journals/2021_03_13 2.md" journals/2021_03_13.md
MD5 (journals/2021_03_13 2.md) = 3d25f70f50d699a9401695a8cb1fe38a
MD5 (journals/2021_03_13.md) = 3d25f70f50d699a9401695a8cb1fe38a
```
since then I can just `rm` the culprit fork.

#### Otherwise, 

```
md5 journals/2023_01_12*
MD5 (journals/2023_01_12 2.md) = f98be369e775312a0c6357562f150ea9
MD5 (journals/2023_01_12.md) = 1a0217cbaa534810a8175f62ad3e8148
```
I can jump straight to the vimdiff, or macvim diff, `mvim -d journals/2023_01_12*`


#### Wow stumbled on one with 3 forks

```sh
(base) $ md5 journals/2022_10_22*
MD5 (journals/2022_10_22 2.md) = 293736c508df2f05e07516e2b4f6e4c9
MD5 (journals/2022_10_22 3.md) = ea02d222564aadd005be662e131b7914
MD5 (journals/2022_10_22.md) = be9ba3be408d55dcd24cc89421a66e36
```
