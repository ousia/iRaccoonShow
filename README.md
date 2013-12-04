# iRaccoonShow

iRaccoonShow enables the creation of presentations that include slides with synchronized sound. One presentation (re)created with iRaccoonShow is <http://www.free-culture.tk>.

Of course, your favourite screencast software can be used to record a presentation. But such a video cannot beat the presentations generated by iRaccoonShow in two different areas:

* File size: each slide image is include only once in the final presentation.

* Image quality: vector images allow higher resolutions without higher file sizes.

Digital video requires to include the same image many times per second. This is a huge waste of unrequired size. And when the number of images per second is decreased, audio can loose sync with images.

But even if the slide could be included only once for its full display time, its image would have a given resolution. Image size in video cannot increased without decreasing its definition. Maybe a higher resolution could be set in some cases, but the resulting file would be higher.

iRaccoonShow includes each image only once in the presentation, preserving each resolution–independent image as such.

## Tools

There are two main tools in iRaccoonShow:

* `recslides` records the sound to a file and writes the slide transitions to a text file, while displaying the slides at full screen.

* `supershow-generator` generates the final Flash presentation and loader from the PDF file, the sound recording and the time transitions.

## Warning

Just in case you wonder and before further reading: I cannot code. My background isn’t technical and I have never learned programming. Sorry, but I must confess it’s too complex for a simple mind such as mine :smirk:.

What I have done here could be considered trial–and–error writing. It works for me, but it is full of glitches. I’m aware of the limits of iRaccoonShow, but I cannot overcome them.

<!--- ## Motivation

I -->

## The Name of the Game

iRaccoonShow stands for “improved RaccoonShow”. [RaccoonShow](https://github.com/jonobacon/raccoonshow/) was originally developed by [Jono Bacon](http://www.jonobacon.org). I expanded the original script for my personal use.

Actually the expansion was motivated by the development of SuperShow. Sergio Costas provided a more powerful method for Flash generation. But SuperShow was designed with slide show recreation in mind. Here was were the original `raccoonshow` script came handy. iRaccoonShow names the whole project.

The `raccoonshow` script—the same way as its `supershow-generator` development—focused only on the Flash generation. It required already recorded sound and slide transition times. Depending on the presentation style, writing this time line could be crazy.

So, I developed for my own use a script that recorded both sound and slides transition times when giving the presentation. [With giving the presentation, I don’t mean the public speaking; sitting in front of the computer does the work as well.] `recslides` is extremely simple, but it does the job.

Both scripts are part of iRaccoonShow. They work for me. And I thought they might be useful for others. If not as running software, as an inspiration to develop similar software.

`supershow-generator` is named after SuperShow. The `swfc` script used to generate the Flash presentation is a derivative version of `script.base` that comes with SuperShow.

## Requirements

iRaccoonShow has the following dependencies:

* Python: was the original script language of RaccoonShow, from what iraccoonshow evolved.
* GTK, PyGTK: minimal GUI.
* Poppler: PDF display.
* GStreamer, PyGST: audio recording.
* SWFTools: generation of Flash files.

iRaccoonShow is a command–line software. In `recslides`, command–line is only used to invoke the tool (after that, there is no command–line :wink:).

It only works on Linux. I’m not saying that it cannot be ported to other platforms: this is something still to be done.

## How It Works

### `recslides`

`recslides` records the sound from the microphone and registers each slide transition timing.

1. It’s invoked in the command–line with something like `recslides presentation.pdf`.
    * To avoid unintended data loss, if there are sound and/or times files already recorded, `recslides` will prompt whether to overwrite them or to quit.
    * Extension will be appended when not specified (either `.pdf` or `.PDF`). If the file doesn’t exist, `recslides` will quit.

1. A new window is opened in the middle of the screen, displaying the first slide from presentation.
    * If you close the window before the next step (before the presentation goes full screen), previously existing files won’t be modified. This might be important when you realize that the already existing files are the ones you want to keep.

1. When the mouse is single–clicked for the first time, presentation goes to full screen and sound from microphone starts to be recorded in a sound file (something like `presentation-audio.wav`).

1. Each time the mouse is clicked, presentation advances to next slide and the transition time is recorded to a text file (named such as `presentation-times.txt`).

1. When the last slide is reached and the mouse is clicked, presentation leaves full screen and audio recording is stopped. It takes half a second extra to avoid problems with the Flash generation.

With `recslides`, you obtain both the recorded sound and transition times from each slide in presentation. This means you have two key features:

* Having the transition times and sound, you can generate the final presentation in the format you like (being Flash only one of the possible ones [more on this](#flash)).

* This is the best (or maybe the only possible) way to get accurate transition times. Times are recorded when giving the presentation (not necessarily in public), not recreated by calculating how long each slide took.

<!--- this is so simple stupid that it just works -->

### `supershow-generator`

`supershow-generator` generates both the Flash presentation and a loader from PDF slides, the recorded sound and the timeline.

1. It’s invoked in the command–line by something like `supershow-generator presentation.pdf`
    * It needs at least a PDF file as argument. It can append the extension. If only the PDF file is specified, it assumes that sound file and times files are named `presentation-audio.wav` and `presentation-times.txt`. (Yes, as they are named by `recslides`.)
    * If sound and times files aren’t named according the convention described in the previous paragraph, creating two symbolic links following the naming conventions to the real files will do the work.

1. Options can be appended to the argument, but they need reworking. The only one relevant (and known to work option) is `-k`, that keeps script files and generated slides and cover slides.

1. `supershow-generator` creates a Flash presentation file (`presentation-presentation.swf`) and a loader file (`presentation-loader.swf`).

1. The loader can be embedded in the HTML page, using code similar to:
    ```
    <object type="application/x-shockwave-flash" data="./presentation-loader.swf">
        <param name="movie" value="./presentation-loader.swf"/>
        <param name="play" value="true"/>
        <param name="loop" value="false"/>
        <param name="quality" value="high"/>
        <param name="loop" value="false"/>
        <param name="allowfullscreen" value="true"/>
    </object>
    ```

1. The presentation could be embedded also in the HTML page. I really discourage this as a bad idea. The browser will have to load a huge file—the presentation itself—to get the page fully loaded.

1. The loading path for the presentation in the loader is relative. There is a new way to create absolute paths in the loader.

## Bugs

If you find a bug using iRaccoonShow, please [report it](https://github.com/ousia/iRaccoonShow/issues/new). I cannot promise I’ll (be able to) fix it.

Of course, this simple piece of software has bugs. I cannot code, so you can [report issues](https://github.com/ousia/iRaccoonShow/issues). But if you can contribute code, issues will be fixed earlier.

Any help is appreciated.

`swfc` has a bug with latest `lame` version. Until this is fixed in [SWFTools](http://www.swftools.org/), the workaround is to provide the .mp3 file to `supershow-generator`. One needs to invoke `lame` directly such as in:

    lame -s 16 -m m -b 32 presentation-audio.wav presentation-audio.mp3

## Compatibility Issues

I think there are two main areas in with compatibility issues might arise: iRaccoonShow as the tool and Flash as the output format.

### iRaccoonShow

Porting iRaccoonShow to Windows and MacOSX isn’t impossible, but this is beyond my (non–existent) technical skills.

My guess is that it may be easier to write these tools with native libraries for those platforms. At least, the libraries for PDF display and audio recording. But this is only a(n educated?) guess.

[SWFTools](http://www.swftools.org/) works out–of–the box in Windows. And it may be installed in MacOSX (using [MacPorts](https://www.macports.org/install.php) or even [Homebrew](http://brew.sh/) [the latter seems harder to install]).

I run Linux on my machine. So, even if I had something designed for Windows or MacOSX, I wouldn’t be able to check it on these platforms.

### Flash

Flash is available for Windows, MacOSX and Linux. iPad isn’t supported, since Apple doesn’t want to have it supported.

Linux has a Flash player, but its development has stopped in version 11.2 ([security fixes will be added for five years after this release](http://www.adobe.com/devnet/flashplatform/whitepapers/roadmap.html)).

Since Flash is a dead project in Linux, there are two other possibilities:

* Generate a movie with variable frame–rate. Image quality with the [VP9 codec](http://www.vp9videocodec.com) seems to be the best available. And audio can be much compressed with a higher quality using the [Opus codec](http://www.opus-codec.org/).

* PDF can be a good format for vector–based presentations. It only requires some multimedia JavaScript and a PDF reader implemented by Adobe.

## License

All code published within this repository is released to the public under the GNU General Public License version 3 or any later version.

There are two `swfc` scripts used for Flash generation, either from presentation of the loader—`swfc.basic` and `swfc.loader`. These scripts contain an exception that prevents the GNU GPLv3 being automatically applied to the generated presentation or the loader themselves.

The code comes with no warranty. Use at your own risk.

## Acknowledgments

Well, I gratefully acknowledge that I stand on the shoulders of many giants:

* Lawrence Lessig gave the original talk at the O’Reilly Open Source Conference in 2002.

* Leonard Lin created the first Flash presentation and posted it [online](http://randomfoo.net/oscon/2002/lessig/). (Originally released under a Creative Commons Attribution–ShareAlike license. ActionScript code kindly reissued under the BSD 3-clause license [here](https://github.com/lhl/free_culture/).)

* Matthias Kramm develops [SWFTools](http://www.swftools.org/), a GNU GPLv2+ licensed software that makes all the Flash generation.

* Jono Bacon developed [RaccoonShow](http://www.jonobacon.org/files/raccoonshow-0.6.tgz), the first tool that enabled the recreation from a Flash file  from PDF slides and recorded video. (Released under the GNU GPLv2 license. Abandoned project, but kindly reissued under the GNU GPLv2+ license [here](https://github.com/jonobacon/raccoonshow/).)

* Sergio Costas developed [SuperShow](http://www.rastersoft.com/programas/supershow.html), which allows the user to recreate a presentation from a video file and the slides in PDF format. (Released under the GNU GPLv3 license. Abandoned project, but Sergio was kind enough to relicense `script.base` under the GNU GPLv3+ license with an exception [[here]](https://github.com/rastersoft/supershow).)

* I recreated the original presentation and posted it [online](http://www.free-culture.tk). Thanks to the improvements to [SWFTools](http://www.swftools.org/) by Matthias Kramm, the original file was decreased in a 27% smaller size. I couldn’t have done that without the help of Matthias Kramm, Sergio Costas, Chris Pugh, Ricardo Pedroso and Huub Schaeks.
