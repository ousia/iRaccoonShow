# iRaccoonShow

iRaccoonShow enables the creation of presentations that include slides with synchronized sound. Of course, a screencasting facility can be used to record video, but these output files won’t match the much smaller file sizes and the much higher image quality achieved with iRaccoonShow.

One presentation (re)created with iRaccoonShow is <http://www.free-culture.tk>.

There are two main tools in iRaccoonShow:

* `iraccoonshow` generates the final Flash presentation and loader from the PDF file, the sound recording and the time transitions.

* `recslides` records the sound to a file and writes the slide transitions to a text file, while displaying the slides at full screen.

## Warning

Just in case you wonder and before further reading: I cannot code. My background isn’t technical and I have never learnt programming. Sorry, but I must confess it’s too complex for a simple mind like mine :smirk:.

What I have done here is could be considered trial--and--error writing. It works for me, but it is full of glitches. I’m aware of the limits of iRacconShow, but I cannot overcome them.

## Requirements

iRaccoonShow has the following dependencies:

* Python: was the original script language of RaccoonShow, from what everything evolved.
* PyGTK, PyGlade: GUI.
* Poppler: PDF display.
* GStreamer, PyGST: audio recording.
* SWFTools: generation of Flash files.

It is mainly a command--line software. In `recslides`, command--line is only used to invoke the tool (after that is pure image).

And this only works on Linux. Not saying that it cannot be ported to other platforms, but this is something still to be done.

## How It Works


## Help Wanted

Copy and paste is the wrong technique to write anything. This also applies to code writing.

Even before I can start sharing code, I already have issues. If you are interested, any help is welcome.

## Compatibility

the other 

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
