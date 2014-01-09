#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
# supershow-generator
# Based on racccoonshow by Jono Bacon
# Modified by Pablo Rodríguez using code from SuperShow
# (http://www.rastersoft.com/programas/supershow.html)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA or see <http://www.gnu.org/licenses/gpl.html>.

import commands
import glob
import sys
import os
import getopt
import gfx
import iRS_settings

class Backend:

    def __init__(self):
        self.keepfiles = False
        self.relative_times = False
        self.audiofile = ""
        self.pdffile = ""
        self.swffile = ""
        self.outputfile = ""
        self.frame_rate = ""
        self.format = ""
        self.installpath = os.path.dirname(os.path.realpath(__file__))

        self.filename = os.path.splitext(sys.argv[1])[0]
        self.filepath = os.path.dirname(os.path.abspath(sys.argv[1]))

        if os.path.splitext(sys.argv[1])[1] == (".swf" or ".SWF"):
            self.swffile = sys.argv[1]
        elif os.path.splitext(sys.argv[1])[1] != (".pdf" or ".PDF"):
            self.pdffile = os.path.splitext(sys.argv[1])[0] + ".pdf"
            if os.path.exists(self.pdffile) == False:
                self.pdffile = os.path.splitext(sys.argv[1])[0] + ".PDF"
        elif os.path.exists(sys.argv[1]):
            self.pdffile = sys.argv[1]

        if os.path.exists(self.filename + "-audio.mp3"):
            self.audiofile = self.filename + "-audio.mp3"
        elif os.path.exists(self.filename + "-audio.wav"):
            self.audiofile = self.filename + "-audio.wav"

        if os.path.exists(self.filename + '-times.txt'):
            self.timeline = self.filename + '-times.txt'

        self.slidesfile = self.filename + "-slides.swf"
        self.coverslidefile = self.filename + "-first.swf"
        self.scriptfile = self.filename + ".sc"
        self.loaderscript = self.filename + "-loader.sc"
        self.loader = self.filename + "-loader.swf"

    def setPDFFile(self, setting):
        pdffile = setting
        if pdffile:
            self.pdffile = os.path.abspath(pdffile)
            extension = self.pdffile[-3:]
            if extension == "pdf" or extension == "PDF":
                self.filename = self.pdffile[:-4]
            else:
                self.filename = self.pdffile
            self.scriptfile = self.filename + ".sc"

    def getSWFFile(self, setting):
        swffile = setting
        if swffile:
            self.swffile = os.path.abspath(setting)
            extension = self.swffile[-3:]
            if extension == "swf" or extension == "swf":
                self.filename = self.swffile[:-4]
            else:
                self.filename = self.swffile
            self.slidesfile = ""
            self.scriptfile = self.filename + ".sc"

    def setAudioFile(self, setting):
        self.audiofile = os.path.abspath(setting)

    def setTimeLine(self, setting):
        self.timeline = os.path.abspath(setting)

    def setOutputFile(self, setting):
        self.outputfile = os.path.abspath(setting)

    def setFrameRate(self, setting):
        self.frame_rate = setting

    def setFormat(self, setting):
        self.format = setting

    def importTimeLine(self):
        print "Reading in the timeline...\t(" + self.timeline + ")"
        timeline = open(self.timeline,"r")
        self.times =  filter(lambda x: len(x.strip()) > 0, list(x.rstrip("\n") for x in timeline) )

    def inputFileCheck(self):
        if not (self.pdffile or self.swffile):
            print "Error:\tYou have neither specified PDF nor SWF file.\n\tUse one of the -p or -s (--pdf or --swf) options to do this."
            sys.exit(2)

        if not self.audiofile:
            print "Error:\tYou have not specified an audio file.\n\tUse the -a or --audio option to do this."
            sys.exit(2)

        if not self.timeline:
            print "Error:\tYou have not specified a timeline.\n\tUse the -t or --timeline option to do this."

        if not self.outputfile:
            self.presentation = self.filename + "-presentation.swf"
        else:
            self.presentation = self.outputfile

        if not self.frame_rate:
            self.time_scale = 1
        else:
            self.time_scale = self.frame_rate

        if not self.format:
            self.format = "miliseconds"

    def convertPdf(self):
        if self.swffile:
            print "Using already converted SWF presentation\t(" + self.swffile + ")"
        elif self.pdffile:
            print "Converting slides to Flash...\t(" + self.slidesfile + ")"
            commands.getoutput("pdf2swf -T 8 -s filloverlap -s linksopennewwindow " + self.pdffile + " -o " + self.slidesfile)

    def get_param(self, text):  # copied from SuperShow 2.3
        pos1_old=0;
        while True:
            pos1=text.find("{",pos1_old)
            if pos1==-1: # no more sequences to replace
                return (-1,0,"","")

            pos2=text.find("}",pos1)
            if pos2==-1: # sequence not ended: no more sequences to replace
                return (-1,0,"","")

            t1=text.find(":",pos1,pos2) # check that there are ':' in the middle
            if t1==-1: # if there isn't it, it's not a sequence
                pos1_old=pos2
                continue

            t2=text.find("\n",pos1,pos2) # check that there aren't newlines in the middle
            if t2!=-1: # if there are it, it's not a sequence
                pos1_old=pos2
                continue

            t2=text.find(";",pos1,pos2) # check that there aren't semicolons in the middle
            if t2!=-1: # if there are it, it's not a sequence
                pos1_old=pos2
                continue

            t2=text.find(" ",pos1,pos2) # check that there aren't blank spaces in the middle
            if t2!=-1: # if there is any, it's not a sequence
                pos1_old=pos2
                continue

            return (pos1,pos2,text[pos1+1:t1],text[t1+1:pos2])

    def createScript(self):
        print "Building the presentation script... (" + self.scriptfile + ")"

        counter=len(self.times)

        filescript=open( self.installpath + "/script.tiny","r")
        filebuffer=filescript.read()
        filescript.close()

        filebuffer+="\n"

        while True:

            (start,end,param,var)=self.get_param(filebuffer)
            if start==-1:
                break

            if param=="program":
                if var=="version":
                   filebuffer=filebuffer[:start]+"supershow-generator-"+iRS_settings.version+filebuffer[end+1:]
                   continue

            if param=="filename":
                if var=="output":
                   filebuffer=filebuffer[:start]+self.presentation+filebuffer[end+1:]
                   continue
                if var=="slides":
                    if self.swffile:
                        filebuffer=filebuffer[:start]+self.swffile+filebuffer[end+1:]
                    else:
                        filebuffer=filebuffer[:start]+self.slidesfile+filebuffer[end+1:]
                    continue
                if var=="audio":
                    filebuffer=filebuffer[:start]+self.audiofile+filebuffer[end+1:]
                    continue
                if var=="installpath":
                    filebuffer=filebuffer[:start]+self.installpath+filebuffer[end+1:]
                    continue

            if param=="maxtime":
                filebuffer=filebuffer[:start]+var+"="+str(counter)+";"+filebuffer[end+1:]
                continue

            if param=="timelist":
                list_tmp=var+"[0]=0;\n"
                num = 1
                audio_delay = 500

                for element in self.times:
                    t=int(element)
                    list_tmp+="\t"+var+'['+str(num)+']='+str(t+audio_delay)+';\n'
                    num+=1
                filebuffer=filebuffer[:start]+list_tmp+filebuffer[end+1:]
                continue

           # if not recognized, remove it
            filebuffer=filebuffer[:start]+filebuffer[end+1:]

        print "Saving the script at " + self.scriptfile
        script_file = open(self.scriptfile,"w")
        script_file.write(filebuffer)
        script_file.close()

    def processScript(self):
        print "Generating presentation to SWF... (" + self.presentation + ")"
        commands.getoutput("swfc " + self.scriptfile)

    def convertFirstSlide(self):
        if self.pdffile:
            print "Converting first slide to Flash...\t(" + self.coverslidefile + ")"
            commands.getoutput("pdf2swf -p 1 -T 8 -s filloverlap -s linksopennewwindow " + self.pdffile + " -o " + self.coverslidefile)

    def createLoaderScript(self):
        print "Building the loader... (" + self.loaderscript + ")"

        filescript=open(self.installpath + "/script.loader","r")
        filebuffer=filescript.read()
        filescript.close()

        filebuffer+="\n"

        while True:

            (start,end,param,var)=self.get_param(filebuffer)
            if start==-1:
                break

            if param=="program":
                if var=="version":
                   filebuffer=filebuffer[:start]+"supershow-generator-"+iRS_settings.version+filebuffer[end+1:]
                   continue

            if param=="filename":
                if var=="loader":
                   filebuffer=filebuffer[:start]+self.loader+filebuffer[end+1:]
                   continue
                if var=="first":
                    filebuffer=filebuffer[:start]+self.coverslidefile+filebuffer[end+1:]
                    continue
                if var=="installpath":
                    filebuffer=filebuffer[:start]+self.installpath+filebuffer[end+1:]
                    continue
                if var=="output":
                    filebuffer=filebuffer[:start]+os.path.basename(self.presentation)+filebuffer[end+1:]
                    continue

            if param=="presentation":
                swf_first_slide = gfx.open("swf", self.presentation)
                measurement_page = swf_first_slide.getPage(1)

                if var=="width":
                   filebuffer=filebuffer[:start]+str(measurement_page.width)+filebuffer[end+1:]
                   continue
                if var=="height":
                    filebuffer=filebuffer[:start]+str(measurement_page.height)+filebuffer[end+1:]
                    continue
                if var=="installpath":
                    filebuffer=filebuffer[:start]+self.installpath+filebuffer[end+1:]
                    continue

           # if not recognized, remove it
            filebuffer=filebuffer[:start]+filebuffer[end+1:]

        print "Saving the loader at " + self.loaderscript
        loader_file = open(self.loaderscript,"w")
        loader_file.write(filebuffer)
        loader_file.close()

    def processLoader(self):
        print "Generating loader... (" + self.loader + ")"
        commands.getoutput("swfc " + self.loaderscript)

    def clean(self):
        if self.keepfiles == True:
            print "Keeping script and slides... (" + self.slidesfile + ", " + self.scriptfile + self.coverslidefile + ", " +  self.loaderscript + ")"
        else:
            try:
                os.remove(self.scriptfile)
                print "Cleaning script... \t(" + self.scriptfile + ")"
            except OSError:
                pass
            try:
                os.remove(self.slidesfile)
                print "Cleaning slides... \t(" + self.slidesfile + ")"
            except OSError:
                pass
            try:
                os.remove(self.coverslidefile)
                print "Cleaning cover slide... \t(" + self.coverslidefile + ")"
            except OSError:
                pass
            try:
                os.remove(self.loaderscript)
                print "Cleaning loader script... \t(" + self.loaderscript + ")"
            except OSError:
                pass


    def run(self):
        print "\nsupershow-generator-" + iRS_settings.version
        self.inputFileCheck()
        self.convertPdf()
        self.importTimeLine()
        self.createScript()
        self.processScript()
        self.convertFirstSlide()
        self.createLoaderScript()
        self.processLoader()
        self.clean()

        print "\nPresentation successfully created!\n"

def usage():
    print "\n  supershow-generator-" + iRS_settings.version + " (http://www.iraccoonshow.tk)"
    print "  Written by Pablo Rodríguez, based on raccoonshow by Jono Bacon."
    print "  Usage: supershow-generator presentation [options]"
    print "  \t (presentation must be a PDF or SWF file)"
    print "\t-k, --keep-files\tkeep slides and script files"
    print "\t-t, --timeline\t\ta file containing the timeline"
    print "\t-a, --audio\t\tWAV/MP3 file with the recorded audio"
    #~ print "\t-r, --relative-times\ttimeline has relative times (not absolute)"
    print "\t-o, --output\t\toutput file name"
    #~ print "-f, --format\t\tthe timeline format"
    print "\t-v, --version\t\tdisplay supershow-generator version number"
    print ""

def main(argv):
    back = Backend()

    try:
        opts, args = getopt.getopt(argv, "hkp:s:a:t:o:f:rv", ["help", "debug", "keep-files", "pdf=", "swf=", "audio=", "output=", "timeline=", "--frame-rate", "relative-times"])
    except getopt.GetoptError:
        print "\nUnknown option"
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        if opt in ("-k", "--keep-files"):
            back.keepfiles = True
        if opt in ("-p", "--pdf"):
            back.setPDFFile(arg)
        if opt in ("-s", "--swf"):
            back.getSWFFile(arg)
        if opt in ("-a", "--audio"):
            back.setAudioFile(arg)
        if opt in ("-t", "--timeline"):
            back.setTimeLine(arg)
        if opt in ("-o", "--output"):
            back.setOutputFile(arg)
        if opt in ("-f", "--frame-rate"):
            back.setFrameRate(arg)
        if opt in ("-r", "--relative-times"):
            back.relative_times = True
        if opt in ("-v", "--version"):
            print "supershow-generator-" + iRS_settings.version
            sys.exit()

    back.run()

if(len(sys.argv) < 2):
    usage()
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
