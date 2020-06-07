---
title: Using ffmpeg to Merge Videos
date: 2019-03-16
tags: mpeg xargs
---

#### Put together our hyperlapse puzzle videos...
* First stab at a merge using `ffmpeg`
```
time ffmpeg -safe 0 -f concat -i infiles.txt -vcodec copy -acodec copy merged.MOV
```
* [full output here](#full-output-of-the-merge-command)
* and used this `infiles.txt` , following the directions
```
file ./2019-03-09\ 23.03.34.mov
file ./2019-03-10\ 01.21.50.mov
file ./2019-03-10\ 13.01.46.mov
file ./2019-03-10\ 13.03.59.mov
file ./2019-03-10\ 13.05.02.mov
file ./2019-03-10\ 18.43.53.mov
```

#### Did it do the right thing? 
* What are my mov lengths..
```
$ cat fileslist.txt |xargs -t -I % sh -c 'ffmpeg -i "%"  2>&1 |grep Duration '
sh -c ffmpeg -i "./2019-03-09 23.03.34.mov"  2>&1 |grep Duration 
  Duration: 00:00:30.40, start: 0.000000, bitrate: 14837 kb/s
sh -c ffmpeg -i "./2019-03-10 01.21.50.mov"  2>&1 |grep Duration 
  Duration: 00:00:34.50, start: 0.000000, bitrate: 14971 kb/s
sh -c ffmpeg -i "./2019-03-10 13.01.46.mov"  2>&1 |grep Duration 
  Duration: 00:00:00.07, start: 0.000000, bitrate: 15840 kb/s
sh -c ffmpeg -i "./2019-03-10 13.03.59.mov"  2>&1 |grep Duration 
  Duration: 00:00:01.40, start: 0.000000, bitrate: 16455 kb/s
sh -c ffmpeg -i "./2019-03-10 13.05.02.mov"  2>&1 |grep Duration 
  Duration: 00:00:32.63, start: 0.000000, bitrate: 14944 kb/s
sh -c ffmpeg -i "./2019-03-10 18.43.53.mov"  2>&1 |grep Duration 
  Duration: 00:00:39.10, start: 0.000000, bitrate: 14868 kb/s
```
* And the length of the merged movie created ... 
```
$ ffmpeg -i merged.MOV 2>&1|grep Duration
  Duration: 00:02:18.10, start: 0.000000, bitrate: 14921 kb/s
```
* Doing some quick mental maths, that actually roughly adds up.

#### Grr but at minute 1:05 it flips the video
* What the heck? Ah according to [stackoverflow](https://superuser.com/questions/578321/how-to-rotate-a-video-180-with-ffmpeg) , ffmpeg uses rotation metadata to autorotate. Except heh in this case perhaps the autorotate did not happen when I was concatenating?
* My file `2019-03-10 13.05.02.mov` appears to be the one which was rotated.
* Trying to process it to see what happens...
```
ffmpeg -i 2019-03-10\ 13.05.02.mov -c:a copy 2019-03-10\ 13.05.02.ROTATED.mov

```
* Wow that took at least a minute. So umm, since the initial concatenation took under a second, I seriously doubt the autorotation was done during the concatenation.
* Okay, lets try that concat one more time, this time with the new file... and new files list
```
file ./2019-03-09\ 23.03.34.mov
file ./2019-03-10\ 01.21.50.mov
file ./2019-03-10\ 13.01.46.mov
file ./2019-03-10\ 13.03.59.mov
file ./2019-03-10\ 13.05.02.mov
file ./2019-03-10\ 18.43.53.mov
```
```
time ffmpeg -safe 0 -f concat -i infiles.2019-03-16T2004Z.txt -vcodec copy -acodec copy 2019-03-16T2006Z-puzzle-merged.MOV

```
* Unfortunately, `2019-03-16T2006Z-puzzle-merged.MOV` is even worse, because for some reason, only one frame is displayed for several minutes. So some more tweaking is needed.

### Appendix
#### full output of the merge command
```
ffmpeg version 4.1.1 Copyright (c) 2000-2019 the FFmpeg developers
  built with Apple LLVM version 10.0.0 (clang-1000.11.45.5)
  configuration: --prefix=/usr/local/Cellar/ffmpeg/4.1.1 --enable-shared --enable-pthreads --enable-version3 --enable-hardcoded-tables --enable-avresample --cc=clang --host-cflags='-I/Library/Java/JavaVirtualMachines/openjdk-11.0.2.jdk/Contents/Home/include -I/Library/Java/JavaVirtualMachines/openjdk-11.0.2.jdk/Contents/Home/include/darwin' --host-ldflags= --enable-ffplay --enable-gnutls --enable-gpl --enable-libaom --enable-libbluray --enable-libmp3lame --enable-libopus --enable-librubberband --enable-libsnappy --enable-libtesseract --enable-libtheora --enable-libvorbis --enable-libvpx --enable-libx264 --enable-libx265 --enable-libxvid --enable-lzma --enable-libfontconfig --enable-libfreetype --enable-frei0r --enable-libass --enable-libopencore-amrnb --enable-libopencore-amrwb --enable-libopenjpeg --enable-librtmp --enable-libspeex --enable-videotoolbox --disable-libjack --disable-indev=jack --enable-libaom --enable-libsoxr
  libavutil      56. 22.100 / 56. 22.100
  libavcodec     58. 35.100 / 58. 35.100
  libavformat    58. 20.100 / 58. 20.100
  libavdevice    58.  5.100 / 58.  5.100
  libavfilter     7. 40.101 /  7. 40.101
  libavresample   4.  0.  0 /  4.  0.  0
  libswscale      5.  3.100 /  5.  3.100
  libswresample   3.  3.100 /  3.  3.100
  libpostproc    55.  3.100 / 55.  3.100
Input #0, concat, from 'infiles.txt':
  Duration: N/A, start: 0.000000, bitrate: 14833 kb/s
    Stream #0:0(und): Video: hevc (Main) (hvc1 / 0x31637668), yuvj420p(pc), 1920x1080, 14833 kb/s, 30 fps, 30 tbr, 600 tbn, 600 tbc
    Metadata:
      rotate          : 180
      creation_time   : 2019-03-10T05:20:20.000000Z
      handler_name    : Core Media Video
      encoder         : HEVC
Output #0, mov, to 'merged.MOV':
  Metadata:
    encoder         : Lavf58.20.100
    Stream #0:0(und): Video: hevc (Main) (hvc1 / 0x31637668), yuvj420p(pc), 1920x1080, q=2-31, 14833 kb/s, 30 fps, 30 tbr, 19200 tbn, 600 tbc
    Metadata:
      rotate          : 180
      creation_time   : 2019-03-10T05:20:20.000000Z
      handler_name    : Core Media Video
      encoder         : HEVC
Stream mapping:
  Stream #0:0 -> #0:0 (copy)
Press [q] to stop, [?] for help
[mov @ 0x7fba5d80dc00] Non-monotonous DTS in output stream 0:0; previous: 1246080, current: 1246080; changing to 1246081. This may result in incorrect timestamps in the output file.
frame= 2828 fps=0.0 q=-1.0 size=  172544kB time=00:01:34.20 bitrate=15005.1kbitsframe= 4142 fps=0.0 q=-1.0 Lsize=  251538kB time=00:02:18.00 bitrate=14931.9kbits/s speed= 148x    
video:251484kB audio:0kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: 0.021355%

real	0m1.186s
user	0m0.124s
sys	0m0.232s
```

#### reference
* [xargs reference](https://shapeshed.com/unix-xargs/)
