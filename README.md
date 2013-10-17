# iRaccoonShow

iRaccoonShow enables the creation of presentations that include slides with synchronized sound. Of course one can use a screencasting facility and save a video, but output files won’t match the file sizes and image quality achieved with iRaccoonShow.

One sample achieved with iRaccoonShow is <http://www.free-culture.tk>.

There are two main tools in iRaccoonShow:

* `iraccoonshow` generates the final Flash presentation and loader from the PDF file, the sound recording and the time transitions.

* `recslides` records the sound to a file and writes the slide transitions to a text file, while displaying the slides at full screen.

## Warning

Just in case you wonder and before further reading: I cannot code. My background isn’t technical and I have never learnt programming. Sorry, but I must confess it’s too complex for me :smirk:.

What I have done here is merely fortunate copying and pasting. It works for me, but it is full of glitches. I’m aware of the limits of iRacconShow, but I cannot overcome them.

## Requirements

iRS has the following dependencies:

* SWFTools: Flash generation.
* PyGTK: 
* PyGlade: 
* Poppler: PDF display.
* GStreamer.
* PyGST.

It is mainly a command--line software. In `recslides`, command--line is only used to invoke the tool (after that is pure image).

And this only works on Linux. Not saying that it cannot be 

## Help Wanted

Copy and paste is the wrong techcnique to write anything. This also applies to code writing.

## Multiplattform

## License

All code released within this repository is under the GNU General Public License version 3 or any later version.

The code comes with no warranty.

## Acknowledgments

Well, I thankfully acknowledge that I’m standing on the shoulders of many giants:

* Lawrence Lessig gave the original talk at the O’Reilly Open Source Conference in 2002.

* Leonard Lin created the first Flash presentation and posted it [online](http://randomfoo.net/oscon/2002/lessig/).

* Matthias Kramm develops [SWFTools](http://swftools.org/), a GNU GPL software that makes all the Flash generation.

* Jono Bacon developed [RaccoonShow](http://www.jonobacon.org/files/raccoonshow-0.6.tgz), the first tool that enabled the Flash file generation from PDF slides and synced audio.

* Sergio Costas developed [SuperShow](http://www.rastersoft.com/programas/supershow.html), which allows the user to recreate a presentation with .

* I recreated the original presentation and posted it [online](http://www.free-culture.tk). Thanks to the improvements to SWFTools by Matthias Kramm, the original file was decreased in a 27% smaller size. I couldn’t have done that without the help of Matthias Kramm, Sergio Costas, Chris Pugh, Ricardo Pedroso and Huub Schaeks.
