---
layout: post
title:  "Updates"
date:   2020-05-30 17:24:43 -0400
categories: jekyll update meta
author: michal
---


#### Summary
I tried rebuilding today after 7 months of forgetting how this works and when I tried to `jekyll build` I got

```
$ jekyll build
Traceback (most recent call last):
...
/usr/local/Cellar/ruby/2.6.5/lib/ruby/2.6.0/bundler/lockfile_parser.rb:108:in `warn_for_outdated_bundler_version': You must use Bundler 2 or greater with this lockfile. (Bundler::LockfileError)
```

Per [this answer](https://stackoverflow.com/a/57125886), I ran `gem list bundler` to see my rubygems version and then `gem update --system`

```
$ gem list bundler

*** LOCAL GEMS ***

bundler (2.0.2, 1.17.2)
$ gem update --system
Updating rubygems-update
Fetching rubygems-update-3.1.3.gem
Successfully installed rubygems-update-3.1.3
...
...
RubyGems installed the following executables:
	/usr/local/Cellar/ruby/2.6.5/bin/gem
	/usr/local/Cellar/ruby/2.6.5/bin/bundle
    
RubyGems system software updated
```
* Now I get
```
$ gem list bundler

*** LOCAL GEMS ***

bundler (default: 2.1.4, 2.0.2, 1.17.2)
$ 

```
* And now my `jekyll build` worked!
