

#### TLDR
This time, the `brew update && brew upgrade` approach resolved my `openssl`  `dyld: Library not loaded` woes. And `brew` apparently no longer has the `switch` command which had been the cornerstone of a popular stackoverflow answer for this problem.


#### Trying to run this new ffmpeg usage, but...

```
$  ffmpeg -i 2021*.jpg -sameq -r 25 outmovie.mp4
dyld: Library not loaded: /usr/local/opt/openssl/lib/libssl.1.0.0.dylib
  Referenced from: /usr/local/bin/ffmpeg
  Reason: image not found
Abort trap: 6

```

```
$ brew update
Error:
  homebrew-core is a shallow clone.
  homebrew-cask is a shallow clone.
To `brew update`, first run:
  git -C /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core fetch --unshallow
  git -C /usr/local/Homebrew/Library/Taps/homebrew/homebrew-cask fetch --unshallow
These commands may take a few minutes to run due to the large size of the repositories.
This restriction has been made on GitHub's request because updating shallow
clones is an extremely expensive operation due to the tree layout and traffic of
Homebrew/homebrew-core and Homebrew/homebrew-cask. We don't do this for you
automatically to avoid repeatedly performing an expensive unshallow operation in
CI systems (which should instead be fixed to not use shallow clones). Sorry for
the inconvenience!
```

*
```
$ openssl version
OpenSSL 1.0.2n  7 Dec 2017
$ ls -al /usr/local/Cellar/openssl
ls: /usr/local/Cellar/openssl: No such file or directory
$ ls -al /usr/local/Cellar/openssl\@1.1/
total 0
drwxr-xr-x    3 michal  staff    96 22 nov 20:38 .
drwxr-xr-x  111 michal  admin  3552  1 mai 16:11 ..
drwxr-xr-x   14 michal  staff   448 16 oct  2020 1.1.1h
```
* Well [this subject](https://stackoverflow.com/questions/59006602/dyld-library-not-loaded-usr-local-opt-openssl-lib-libssl-1-0-0-dylib)  is super busy on stack overflow. But the top answer did not work for me hmm
```
$ brew switch openssl 1.1.1h
Error: Unknown command: switch
$
```
* And yea according to [here]()  , `switch` command is no more

* Doing `brew upgrade`

```
==> Installing ruby dependency: openssl@1.1
==> Pouring openssl@1.1--1.1.1k.mojave.bottle.tar.gz
==> Regenerating CA certificate bundle from keychain, this may take a while...
🍺  /usr/local/Cellar/openssl@1.1/1.1.1k: 8,071 files, 18.4MB
...
...
==> Upgrading openssl@1.1 1.1.1k -> 1.1.1k
Removing: /usr/local/Cellar/openssl@1.1/1.1.1h... (8,067 files, 18.4MB)
```
* Ok anyway that took like 20 minutes but now running my `ffmpeg` command again, now no more `openssl` error..
