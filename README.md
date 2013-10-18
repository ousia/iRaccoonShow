# iRaccoonShow

iRaccoonShow enables the creation of presentations that include slides with synchronized sound. One presentation (re)created with iRaccoonShow is <http://www.free-culture.tk>.

Of course, your favourite screencast software can be used to record a presentation. But such a video cannot beat the presentations generated by iRaccoonShow in two different areas:

* File size: each slide image is include only once in the final presetation.

* Image quality: vector images allow higher resolutions without higher file sizes.

Digital video requires to include the same image many times per second. This is a huge waste of unrequired size. And when the number of images per second is decreased, audio can loose sync with images.

But even if the slide could be included only once for its full display time, its image would have a given resolution. Image size in video cannot increased without decreasing its definition. Maybe a higher resolution could be set in some cases, but the resulting file would be higher.

iRaccoonShow includes each image only once in the presentation, preserving each resolution–independent image as such.

## Tools

There are two main tools in iRaccoonShow:

* `recslides` records the sound to a file and writes the slide transitions to a text file, while displaying the slides at full screen.

* `iraccoonshow` generates the final Flash presentation and loader from the PDF file, the sound recording and the time transitions.

## Warning

Just in case you wonder and before further reading: I cannot code. My background isn’t technical and I have never learned programming. Sorry, but I must confess it’s too complex for a simple mind such as mine :smirk:.

What I have done here is could be considered trial–and–error writing. It works for me, but it is full of glitches. I’m aware of the limits of iRacconShow, but I cannot overcome them.

## Requirements

iRaccoonShow has the following dependencies:

* Python: was the original script language of RaccoonShow, from what everything evolved.
* PyGTK, PyGlade: GUI.
* Poppler: PDF display.
* GStreamer, PyGST: audio recording.
* SWFTools: generation of Flash files.

iRaccoonShow is mainly a command–line software. In `recslides`, command–line is only used to invoke the tool (after that, there is no command–line :wink:).

It only works on Linux. I’m not saying that it cannot be ported to other platforms: this is something still to be done.

## How It Works

### `recslides`

`recslides` records the sound from the microphone and registers each slide transition timing.

1. It’s invoked in the command–line with something like `recslides mypresentation.pdf`.

1. A new window is opened, displaying the first slide from presentation.

1. When the space bar is pressed for the first time, presentation goes to full screen and sound from microphone starts to be recorded in a sound file.

1. Each time the space bar is pressed, presentation advances to next slide and the transition time is recorded to a text file.

1. When the last slide is reached and the space bar is pressed, presentation leaves full screen and audio recording is stopped.

With `recslides`, you obtain both the recorded sound and transition times from each slide in presentation. This means you have two key features:

* Having the transition times and sound, you can generate the final presentation in the format you like (being Flash only one of the possible ones [more on this]).

* This is the best (or maybe the only possible) way to get accurate transition times. Times are recorded when giving the presentation (not necessarily in public), not recreated by calculating how long each slide took.

<!--- this is so simple stupid that it just works -->

### `ìraccoonshow`

`ìraccoonshow` should be cleared before it can be released to the public ([read the issue](https://github.com/ousia/iRaccoonShow/issues/1)).

## Help Wanted. Apply Within

Copy and paste is the wrong technique to write anything meaningful. This also applies to code writing.

Even before I can start sharing code, I already have [issues](https://github.com/ousia/iRaccoonShow/issues). If you are interested, any help is highly appreciated.

Unless I have assigned an issue to myself (and we can even discuss that in the issue itself), you are welcome to take any issue and solve it.

## Compatibility issues

I think there are two main areas in with compatibility issues might arise: iRaccoonShow as the tool and Flash as the output format.

### iRaccoonShow

I’m only an average user that uses Linux at home and Windows at work. Altough I know how to use a computer (more than particular programs), I’m more proficient in Linux than in Windows. I know that MacOSX is a Unix version, but I don’t have any access to a Mac computer. I don’t think that tablets, phones and such (running iOS or Android) are computers in the proper sense of the term.

One of the main features with iRaccoonShow is the dependency on well established libraries in the Linux ecosystem. This makes portability of the software itself more difficult. As far as I know, it could be possible for Windows, but harder for MacOSX.





Being a command-line program, SWFTools is developed for both Windonws and Linux. I think there is at least one Mac port, but installing it requires to install additional software.

Poppler is a PDF rendering library developed for Linux systems. It

### Flash

Flash

## License

All code published within this repository is released to the public under the GNU General Public License version 3 or any later version.

The code comes with no warranty. Use at your own risk.

## Acknowledgments

Well, I gratefully acknowledge that I stand on the shoulders of many giants:

* Lawrence Lessig gave the original talk at the O’Reilly Open Source Conference in 2002.

* Leonard Lin created the first Flash presentation and posted it [online](http://randomfoo.net/oscon/2002/lessig/). (Originally released under a Creative Commons Attribution-ShareAlike license.)

* Matthias Kramm develops [SWFTools](http://swftools.org/), a GNU GPL software that makes all the Flash generation.

* Jono Bacon developed [RaccoonShow](http://www.jonobacon.org/files/raccoonshow-0.6.tgz), the first tool that enabled the recreation from a Flash file  from PDF slides and recorded video. (Released under the GNU GPLv2 license. Abandoned project.)

* Sergio Costas developed [SuperShow](http://www.rastersoft.com/programas/supershow.html), which allows the user to recreate a presentation from a video file and the slides in PDF format. (Released under the GNU GPLv3 license. Abandoned project.)

* I recreated the original presentation and posted it [online](http://www.free-culture.tk). Thanks to the improvements to SWFTools by Matthias Kramm, the original file was decreased in a 27% smaller size. I couldn’t have done that without the help of Matthias Kramm, Sergio Costas, Chris Pugh, Ricardo Pedroso and Huub Schaeks.
