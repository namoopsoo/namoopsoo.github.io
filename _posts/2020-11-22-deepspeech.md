---
title: Quick test drive this Mozilla/Baidu Deep Speech
date: 2020-11-22
tag: speech recognition, audio
---


#### Summary
Ok managed to get [DeepSpeech](https://github.com/mozilla/DeepSpeech) to run, but the output for my voice maybe does not translate to any text that makes sense hahaha. But it was pretty funny to read the interpretation.

#### My recording was in m4a so I had to change over to wav first
* ffmpeg is good for m4a to wav conversion but my `ffmpeg` is having some issues.

```
(deep3) $ ffmpeg
dyld: Library not loaded: /usr/local/opt/openssl/lib/libssl.1.0.0.dylib
  Referenced from: /usr/local/bin/ffmpeg
  Reason: image not found
Abort trap: 6
(deep3) $

```

* I ran `brew update`
* Then

```
$ brew upgrade ffmpeg
...
==> Upgrading 1 outdated package:
ffmpeg 4.1.1 -> 4.3.1_4
==> Upgrading ffmpeg 4.1.1 -> 4.3.1_4
...
```

* That worked but I saw this at the end , so I did that

```
...
Error: Xcode alone is not sufficient on Mojave.
Install the Command Line Tools:
  xcode-select --install

```

* Still getting..

```
$ ffmpeg
dyld: Library not loaded: /usr/local/opt/openssl/lib/libssl.1.0.0.dylib
  Referenced from: /usr/local/bin/ffmpeg
  Reason: image not found
Abort trap: 6
```

*  ok thank the ages, [this stackoverflow](https://stackoverflow.com/questions/59006602/dyld-library-not-loaded-usr-local-opt-openssl-lib-libssl-1-0-0-dylib) helped a lot !!

```
$ brew switch openssl 1.0.2s
Error: openssl does not have a version "1.0.2s" in the Cellar.
openssl's installed versions: 1.0.2q
$ brew switch openssl 1.0.2q
Cleaning /usr/local/Cellar/openssl/1.0.2q
Opt link created for /usr/local/Cellar/openssl/1.0.2q
$ ffmpeg
ffmpeg version 4.1.1 Copyright (c) 2000-2019 the FFmpeg developers
  built with Apple LLVM version 10.0.0 (clang-1000.11.45.5)
...

```

#### These instructions are pretty clear to get setup w/ deepspeech
* [Starting page](https://github.com/mozilla/DeepSpeech) and the [readthedocs](https://deepspeech.readthedocs.io/en/v0.9.1/?badge=latest)
* I created a separate environment for this with `conda create -n deep3` and `source activate deep3`

```
# Install DeepSpeech
pip install deepspeech

# Download pre-trained English model files
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-models.pbmm
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/deepspeech-0.9.1-models.scorer

# Download example audio files
curl -LO https://github.com/mozilla/DeepSpeech/releases/download/v0.9.1/audio-0.9.1.tar.gz
tar xvf audio-0.9.1.tar.gz

# Transcribe an audio file
deepspeech --model deepspeech-0.9.1-models.pbmm --scorer deepspeech-0.9.1-models.scorer --audio audio/2830-3980-0043.wav

Loading model from file deepspeech-0.9.1-models.pbmm
TensorFlow: v2.3.0-6-g23ad988fcd
DeepSpeech: v0.9.1-0-gab8bd3e1
Loaded model in 0.0486s.
Loading scorer from files deepspeech-0.9.1-models.scorer
Loaded scorer in 0.00625s.
Running inference.
experience proves this
Inference took 5.095s for 1.975s audio file.
```

* That mini sample worked fine.. "experience proves this" is 100% accurate according to my ears at least.

#### I Read Some tips on the conversion
* Ok cool according to [here](https://www.howtoforge.com/tutorial/ffmpeg-audio-conversion/) I can use `ffmpeg` to convert from `m4a` to `wav` with just `ffmpeg -i blah.m4a blah.wav`
* But I tried `deepspeech` on my wav file

```
deepspeech --model deepspeech-0.9.1-models.pbmm --scorer deepspeech-0.9.1-models.scorer --audio blah.wav

Loading model from file deepspeech-0.9.1-models.pbmm
TensorFlow: v2.3.0-6-g23ad988fcd
DeepSpeech: v0.9.1-0-gab8bd3e1
Loaded model in 0.0648s.
Loading scorer from files deepspeech-0.9.1-models.scorer
Loaded scorer in 0.00534s.
Warning: original sample rate (24000) is different than 16000hz. Resampling might produce erratic speech recognition.
```

* Then the `sox` program for resampling not present...
* I read Some notes on resampling [here](https://transcoding.wordpress.com/2011/11/16/careful-with-audio-resampling-using-ffmpeg/) and finding that `ffmpeg` has `sox` built in now.

```
workdir=/blah/my/workdir
infile=${workdir}/2020-11-22-09.54.59.wav
outfile=${workdir}/2020-11-22-09.54.59--resampled.wav
ffmpeg -i $infile  -af aresample=resampler=soxr -ar 16000 $outfile
```

```
deepspeech --model deepspeech-0.9.1-models.pbmm --scorer deepspeech-0.9.1-models.scorer --audio $outfile
```

* Ok hahaha this time after resampling to `16000Hz` finally worked, but the output does not match any kind of reality haha.

```
Loading model from file deepspeech-0.9.1-models.pbmm
TensorFlow: v2.3.0-6-g23ad988fcd
DeepSpeech: v0.9.1-0-gab8bd3e1
Loaded model in 0.0451s.
Loading scorer from files deepspeech-0.9.1-models.scorer
Loaded scorer in 0.00534s.
Running inference.
so then listened and even interesting it interesting idea for talking about the habitation main point is a paradise his crimes and the periostracum basically like ours person wrote his book or started this is to other thinking harrison article or are frontiersman like a loathing at the summer sententiam first creation antoinette to mitigate they had had been important role spoke for catering people is catching people attention and then destournier take nineteen and working on the antithetic aeternitate which takes a attakapas
Inference took 65.434s for 114.816s audio file.
```
