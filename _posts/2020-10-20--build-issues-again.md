


#### Build issues again haha

I am doing `jekyll build` but this time from a `Makefile` , containing 

```
build:
    jekyll build

```
* with `make build`
* And I'm getting 

```
$ make build
jekyll build
Traceback (most recent call last):
	10: from /usr/local/lib/ruby/gems/2.6.0/bin/jekyll:23:in `<main>'
	 9: from /usr/local/lib/ruby/gems/2.6.0/bin/jekyll:23:in `load'
	 8: from /usr/local/lib/ruby/gems/2.6.0/gems/jekyll-4.0.0/exe/jekyll:11:in `<top (required)>'
	 7: from /usr/local/lib/ruby/gems/2.6.0/gems/jekyll-4.0.0/lib/jekyll/plugin_manager.rb:52:in `require_from_bundler'
	 6: from /usr/local/lib/ruby/gems/2.6.0/gems/bundler-2.0.2/lib/bundler.rb:107:in `setup'
	 5: from /usr/local/lib/ruby/gems/2.6.0/gems/bundler-2.0.2/lib/bundler/runtime.rb:26:in `setup'
	 4: from /usr/local/lib/ruby/gems/2.6.0/gems/bundler-2.0.2/lib/bundler/runtime.rb:26:in `map'
	 3: from /usr/local/lib/ruby/gems/2.6.0/gems/bundler-2.0.2/lib/bundler/spec_set.rb:148:in `each'
	 2: from /usr/local/lib/ruby/gems/2.6.0/gems/bundler-2.0.2/lib/bundler/spec_set.rb:148:in `each'
	 1: from /usr/local/lib/ruby/gems/2.6.0/gems/bundler-2.0.2/lib/bundler/runtime.rb:31:in `block in setup'
/usr/local/lib/ruby/gems/2.6.0/gems/bundler-2.0.2/lib/bundler/runtime.rb:319:in `check_for_activated_spec!': You have already activated public_suffix 4.0.5, but your Gemfile requires public_suffix 4.0.1. Prepending `bundle exec` to your command may solve this. (Gem::LoadError)
make: *** [build] Error 1
```
* Ok cool. Whatever that means haha. So going full Memento here, looking at [my earlier notes](/jekyll/update/meta/2020/05/30/trying-again.html) , I see last time I used `gem update --system` to solve the problem.
* So doing that again this time , and saw this output..

```
$ gem update --system
Updating rubygems-update
Fetching rubygems-update-3.1.4.gem
Successfully installed rubygems-update-3.1.4
Parsing documentation for rubygems-update-3.1.4
Installing ri documentation for rubygems-update-3.1.4
Installing darkfish documentation for rubygems-update-3.1.4
Done installing documentation for rubygems-update after 59 seconds
Parsing documentation for rubygems-update-3.1.4
Done installing documentation for rubygems-update after 0 seconds
Installing RubyGems 3.1.4
  Successfully built RubyGem
  Name: bundler
  Version: 2.1.4
  File: bundler-2.1.4.gem
Bundler 2.1.4 installed
RubyGems 3.1.4 installed
Regenerating binstubs
Parsing documentation for rubygems-3.1.4
Installing ri documentation for rubygems-3.1.4

=== 3.1.4 / 2020-06-03

Minor enhancements:

* Deprecate rubyforge_project attribute only during build
  time. Pull request #3609 by Josef Šimánek.
* Update links. Pull request #3610 by Josef Šimánek.
* Run CI at 3.1 branch head as well. Pull request #3677 by Josef Šimánek.
* Remove failing ubuntu-rvm CI flow. Pull request #3611 by
  Josef Šimánek.


------------------------------------------------------------------------------

RubyGems installed the following executables:
	/usr/local/Cellar/ruby/2.6.5/bin/gem
	/usr/local/Cellar/ruby/2.6.5/bin/bundle

Ruby Interactive (ri) documentation was installed. ri is kind of like man 
pages for Ruby libraries. You may access it like this:
  ri Classname
  ri Classname.class_method
  ri Classname#instance_method
If you do not wish to install this documentation in the future, use the
--no-document flag, or set it as the default in your ~/.gemrc file. See
'gem help env' for details.

RubyGems system software updated
You have new mail in /var/mail/michal
$ 
```


#### ok letss try again
```
make build
```
* Darn getting same result. Ok it says to use `bundle exec jekyll build` instead. Going to try that 

* Ok now it did stuff...
```
$ make build
bundle exec jekyll build
Configuration file: /xxxx/repo/namoopsoo.github.io/_config.yml
            Source: /xxxx/repo/namoopsoo.github.io
       Destination: /xxxx/namoopsoo.github.io/_site
 Incremental build: disabled. Enable with --incremental
      Generating... 
             Error: could not read file /xxxx/namoopsoo.github.io/_posts/2019-05-13--keras-hello-world-fashion_files/2019-05-13--keras-hello-world-fashion_18_0.png: invalid byte sequence in UTF-8
...
...
       Jekyll Feed: Generating feed for posts
                    done in 1.715 seconds.
 Auto-regeneration: disabled. Use --watch to enable.
$ 
```
* Now it doesnt like some pngs. Maybe it worked though. Will try. 
