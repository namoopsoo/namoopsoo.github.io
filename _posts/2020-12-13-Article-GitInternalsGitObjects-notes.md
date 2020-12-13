---
title: notes on Git Internals Git Objects article
date: 2020-12-13
---


Reading https://git-scm.com/book/en/v2/Git-Internals-Git-Objects


```
(pandars3) $ echo 'test content' | git hash-object -w --stdin
d670460b4b4aece5915caf5c68d12f560a9fe3e4
```
* I tried that and oh hah so `-w` tells `git hash-object` to actually add that hash to my git key value store database hmm..
* lets see if i can find it ..

```
(pandars3) $ file .git/objects/d6/70460b4b4aece5915caf5c68d12f560a9fe3e4
.git/objects/d6/70460b4b4aece5915caf5c68d12f560a9fe3e4: VAX COFF executable not stripped - version 737
```

* Ah indeed. ok binary though. hmm but apparently this is actual data..

```
(pandars3) $ ls -lh .git/objects/d6/
total 32
-rw-r--r--@ 1 michal  staff   152B Dec  6 15:06 20fe6a1800a210848ce33e3ec41fc1077feeee
-rw-r--r--@ 1 michal  staff   153B Jul  4 14:20 56ffc9856515711c4114654acb0f36c1ee8ddb
-rw-r--r--@ 1 michal  staff    29B Dec 13 17:28 70460b4b4aece5915caf5c68d12f560a9fe3e4
-rw-r--r--@ 1 michal  staff   1.2K Nov 13 11:17 953fd15e1fa200b94fd6124f661adf1528165a
```

* Hmm but it looks like some of the other files here actually have header looking things.     

```
git cat-file -p d670460b4b4aece5915caf5c68d12f560a9fe3e4
```

* But I'm not seeing actual data, just metadata like commit messages, parent hash, tree hash, author, and timestamps

```
(pandars3) $ git cat-file -p d670460b4b4aece5915caf5c68d12f560a9fe3e4
test content
(pandars3) $ git cat-file -p d656ffc9856515711c4114654acb0f36c1ee8ddb
tree 5ff96d0717daba0106acba2dd1b1145ba1e99275
parent ff184a61f4d8bd871ef41cb7934423ecce17177a
author Michal Piekarczyk <namoopsoo> 1593886823 -0400
committer Michal Piekarczyk <namoopsoo> 1593886823 -0400

moar
(pandars3) $
(pandars3) $ git cat-file -p d620fe6a1800a210848ce33e3ec41fc1077feeee
tree 271d395b3591534ebfe7b1e519a744c379f84daf
parent 0a41871bd7588b15f8f48b04bf024851ffdfe231
author Michal Piekarczyk <namoopsoo> 1607285215 -0500
committer Michal Piekarczyk <namoopsoo> 1607285215 -0500

moar

```
*  

```
echo 'version 1' > test.txt
git hash-object -w test.txt
# 83baae61804e65cc73a7201a7252750c76066a30

echo 'version 2' > test.txt
git hash-object -w test.txt
# 1f7a7a472abf3dd9643fd615f6da379c4acb3e3a

(pandars3) $ cat test.txt
version 2

# And I can restore the original..
(pandars3) $ git cat-file -p 83baae61804e65cc73a7201a7252750c76066a30 > test.txt
(pandars3) $ cat test.txt
version 1

```

#### Tree objects
* Ahhh, reading more now so a _Tree Object_ is what solves the problem of how to store file names and group multiple files together.
