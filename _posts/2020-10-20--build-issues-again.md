


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
* Also I forgot that as long as I don't want to care what this looks like locally, I can just push commits to github and then everything just builds there and nothing needs to be done locally.
* Anyway but for local preview, I wonder if I can just find a jekyll docker to make this easier so as not to worry about these weird ruby configurations.

#### Oh wow docker
* Turns out per reading [here](https://jekyllrb.com/docs/continuous-integration/buddyworks/) , there is indeed a [jekyll Docker image](https://hub.docker.com/r/jekyll/jekyll/) already. 
* Let me just test run that wow.


```
docker pull jekyll/jekyll
...
Digest: sha256:bb45414c3fefa80a75c5001f30baf1dff48ae31dc961b8b51003b93b60675334
Status: Downloaded newer image for jekyll/jekyll:latest
```
* But then when running from the [github](https://github.com/envygeeks/jekyll-docker/blob/master/README.md) , 
```
export JEKYLL_VERSION=3.8
docker run --rm \
  --volume="$PWD:/srv/jekyll" \
  -it jekyll/jekyll:$JEKYLL_VERSION 

# jekyll build <= left out this part so I can look inside... 
```
* But I got this 
```
Unable to find image 'jekyll/jekyll:3.8' locally
3.8: Pulling from jekyll/jekyll
...
Digest: sha256:9521c8aae4739fcbc7137ead19f91841b833d671542f13e91ca40280e88d6e34
Status: Downloaded newer image for jekyll/jekyll:3.8
```
* So I suppose latesst was not `3.8`. 
* Anyway wow, a few minutes later this run command is still well, _running_
```
Fetching gem metadata from https://rubygems.org/.........
Fetching public_suffix 4.0.1
Installing public_suffix 4.0.1
Fetching addressable 2.7.0
Installing addressable 2.7.0
Using bundler 2.0.2
Fetching colorator 1.1.0
Installing colorator 1.1.0
Fetching concurrent-ruby 1.1.5
Installing concurrent-ruby 1.1.5
Fetching eventmachine 1.2.7
Installing eventmachine 1.2.7 with native extensions
Fetching http_parser.rb 0.6.0
Installing http_parser.rb 0.6.0 with native extensions
Fetching em-websocket 0.5.1
Installing em-websocket 0.5.1
Fetching ffi 1.11.1
Installing ffi 1.11.1 with native extensions
Fetching forwardable-extended 2.6.0
Installing forwardable-extended 2.6.0
Fetching i18n 1.7.0
Installing i18n 1.7.0
Fetching sassc 2.2.1
Installing sassc 2.2.1 with native extensions
```
* ok continued.. that last part took a while, but the later stuff was quick.
```
Fetching jekyll-sass-converter 2.0.1
Installing jekyll-sass-converter 2.0.1
Fetching rb-fsevent 0.10.3
Installing rb-fsevent 0.10.3
Fetching rb-inotify 0.10.0
Installing rb-inotify 0.10.0
Fetching listen 3.2.0
Installing listen 3.2.0
Fetching jekyll-watch 2.2.1
Installing jekyll-watch 2.2.1
Fetching kramdown 2.1.0
Installing kramdown 2.1.0
Fetching kramdown-parser-gfm 1.1.0
Installing kramdown-parser-gfm 1.1.0
Fetching liquid 4.0.3
Installing liquid 4.0.3
Fetching mercenary 0.3.6
Installing mercenary 0.3.6
Fetching pathutil 0.16.2
Installing pathutil 0.16.2
Fetching rouge 3.12.0
Installing rouge 3.12.0
Fetching safe_yaml 1.0.5
Installing safe_yaml 1.0.5
Fetching unicode-display_width 1.6.0
Installing unicode-display_width 1.6.0
Fetching terminal-table 1.8.0
Installing terminal-table 1.8.0
Fetching jekyll 4.0.0
Installing jekyll 4.0.0
Fetching jekyll-feed 0.12.1
Installing jekyll-feed 0.12.1
Fetching jekyll-seo-tag 2.6.1
Installing jekyll-seo-tag 2.6.1
Fetching jekyll-sitemap 1.3.1
Installing jekyll-sitemap 1.3.1
Fetching minima 2.5.1
Installing minima 2.5.1
Bundle complete! 8 Gemfile dependencies, 31 gems now installed.
Bundled gems are installed into `/usr/local/bundle`
ruby 2.6.3p62 (2019-04-16 revision 67580) [x86_64-linux-musl]
jekyll 4.0.0 -- Jekyll is a blog-aware, static site generator in Ruby

Usage:

  jekyll <subcommand> [options]

Options:
        -s, --source [DIR]  Source directory (defaults to ./)
        -d, --destination [DIR]  Destination directory (defaults to ./_site)
            --safe         Safe mode (defaults to false)
        -p, --plugins PLUGINS_DIR1[,PLUGINS_DIR2[,...]]  Plugins directory (defaults to ./_plugins)
            --layouts DIR  Layouts directory (defaults to ./_layouts)
            --profile      Generate a Liquid rendering profile
        -h, --help         Show this message
        -v, --version      Print the name and version
        -t, --trace        Show the full backtrace when an error occurs

Subcommands:
  compose               
  docs                  
  import                
  build, b              Build your site
  clean                 Clean the site (removes site output and metadata file) without building.
  doctor, hyde          Search site and print specific deprecation warnings
  help                  Show the help message, optionally for a given subcommand.
  new                   Creates a new Jekyll site scaffold in PATH
  new-theme             Creates a new Jekyll theme scaffold
  serve, server, s      Serve your site locally
```
* Oops, guess I ran this poorly... wait hmm I have the interactive flags, not sure why it quit. weird.
* Going to try again ... and w/o the `--rm` so I dont have to redo it...
```
export JEKYLL_VERSION=3.8
docker run  \
  --volume="$PWD:/srv/jekyll" \
  -i -t jekyll/jekyll:$JEKYLL_VERSION 

```
* Start `16:18 UTC .. 16:23 UTC` ... but still not playing nice. not sure why quitting.
* But the container should at least be running now hopefully..
* So let me at least try build. Hmm but `docker ps` shows nothing weird.
* COnfused why it's exiting...
```
$ docker ps --last 5
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                     PORTS                                            NAMES
9ac4abb74269        jekyll/jekyll:3.8   "/usr/jekyll/bin/ent…"   7 minutes ago       Exited (0) 2 minutes ago                                                    compassionate_mccarthy
```
* Anyway trying with `jekyll build` did work but of course it exited again, so this is not really useful if it takes `5 minutes` for stuff to happen and I can't keep the container around. 
* I do see in the `Dockerfile` [here](https://github.com/envygeeks/jekyll-docker/blob/master/repos/jekyll/Dockerfile) that `4000` is permanently exposed so I dont even have to specify that with the `docker run` command so that's cool.

* Hmm in the README it is written to use `gem "jekyll", "~> 3.8"` in your `Gemfile`. 
My `Gemfile`  has `"jekyll", "~> 4.0.0"` actually. I wonder if ...
* Aha and in the output it does actually show
```
Fetching jekyll 4.0.0
Installing jekyll 4.0.0
```
* So it is almost like this mismatch may have caused this to be taking extra time.
* So probably the `Gemfile` should be consistent with this docker image and then it will not take `5 bonus minutes` ?
* Maybe this phenomenon is described [here](https://github.com/envygeeks/jekyll-docker#my-gems-arent-caching) "my gems arent caching".... Ok so I'm diverging indeed ok.

* Ok trying again w/ `gem "jekyll", "~> 3.8"` in my Gemfile this time.
```
$ docker run    --volume="$PWD:/srv/jekyll"   -i -t jekyll/jekyll:$JEKYLL_VERSION jekyll build

Fetching gem metadata from https://rubygems.org/..........
Fetching gem metadata from https://rubygems.org/.
You have requested:
  jekyll ~> 3.8

The bundle currently has jekyll locked at 4.0.0.
Try running `bundle update jekyll`

If you are updating multiple gems in your Gemfile at once,
try passing them all to `bundle update`
```
* Hmm but where is this state maintained?


