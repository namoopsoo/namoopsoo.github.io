


#### Trying
* Per [here](http://tooloftrade.blogspot.com/2011/10/merging-images-into-movie-using-ffmpeg.html) tried

```
 ffmpeg -i image%03d.jpeg -sameq -r 25 outmovie.mp4
```

* But getting

```
Option 'sameq' was removed. If you are looking for an option to preserve the quality (which is not what -sameq was for), use -qscale 0 or an equivalent quality factor option.
Failed to set value '1' for option 'sameq': Invalid argument
```

*

```
ffmpeg -framerate 24 -i img%03d.png output.mp4
```

* To glob...
```
ffmpeg -framerate 24 -pattern_type glob -i '*.jpg' -c:v libx264 -pix_fmt yuv420p out.mp4
```

* That kind of did the trick, but kind of fast. only lasted 2 seconds..
* Per  the "Additional Info: Frame rates" section in https://trac.ffmpeg.org/wiki/Slideshow  ,
```
ffmpeg -framerate 1/3 -pattern_type glob -i '2021-05-19 09.0*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p out.slower.mp4
```
* Wow nice that was perfect , so `1/3` indeed sets the duration at `3 seconds` per image...

* Going to try again with `0.75 seconds` so

```
ffmpeg -framerate 4/3 -pattern_type glob -i '2021-05-19 09.0*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p out.slower.three_quarters.mp4
```
* Okay that was about perfect I think.
* Only thing is my images are rotated still, so think I got to rotate them first ..

```
ffmpeg -framerate 4/3 -pattern_type glob -i '*R.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p out.slower.three_quarters.mini.mp4

```
* Wow very weird, but "turns out" hehe , all I had to do was rotate the image 360 degrees and it still managed to get modified and then the `mp4` orientation ended up being correct finally.

* Hopefully image magick has the same effect?  ( per [here](https://codeyarns.com/tech/2016-07-05-how-to-rotate-image-using-imagemagick.html) )

```
convert -rotate "360" "2021-05-19 09.02.15.jpg"   "2021-05-19 09.02.15.R360.jpg"

$ md5 "2021-05-19 09.02.15.jpg"   "2021-05-19 09.02.15.R360.jpg"
MD5 (2021-05-19 09.02.15.jpg) = 63efd132e1c609672f260c0af1c84058
MD5 (2021-05-19 09.02.15.R360.jpg) = 08c2a4716cb90e8d53a0bde0d3d0a397
```
* Wow something definitely happened here hmm.
* Try a few more and reproduce..

```
convert -rotate "360" "2021-05-19 09.02.24.jpg" "2021-05-19 09.02.24.R360.jpg"
convert -rotate "360" "2021-05-19 09.02.32.jpg" "2021-05-19 09.02.32.R360.jpg"
```

* And try on just the image magick images..

```
ffmpeg -framerate 4/3 -pattern_type glob -i '*R360.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p out.slower.three_quarters.mini4.mp4

```
* Hmm dang the output `out.slower.three_quarters.mini4.mp4` is still rotated.
* Maybe image magick is doing some pure math rotation, but perhaps using the "Preview" app to do the rotation resets some kind of EXIF rotation setting.
