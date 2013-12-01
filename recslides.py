#!/usr/bin/python
# coding: utf-8
#
# Copyright 2008-2013 (C) Pablo Rodríguez
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA or see <http://www.gnu.org/licenses/gpl.html>.

import sys, os, time
import gnomevfs
import gtk
try:
    import poppler
except:
    print "python-poppler is not available"
import cairo
import pygst
pygst.require("0.10")
import gst

class rec_presentation:
    def __init__(self):

        if(len(sys.argv) < 2):
            print "  recslides" + ". Written by Pablo Rodríguez."
            print "  Usage: recslides mypresentation.pdf"
            sys.exit(2)

        self.filename = os.path.splitext(sys.argv[1])[0]

        if os.path.splitext(sys.argv[1])[1] != (".pdf" or ".PDF"):
            self.pdffilename = os.path.splitext(sys.argv[1])[0] + ".pdf"
            if  os.path.exists(self.pdffilename) == False:
                self.pdffilename = os.path.splitext(sys.argv[1])[0] + ".PDF"
            elif os.path.exists(self.pdffilename) == False:
                print "\n  recslides requires a PDF document to work with."
                print "  recslides will now exit.\n"
                sys.exit()
        else:
            self.pdffilename = sys.argv[1]

        uri = gnomevfs.make_uri_from_shell_arg(self.pdffilename)

        self.audiofilename = self.filename + "-audio.wav"
        self.timesfilename = self.filename + '-times.txt'

        if (os.path.exists(self.audiofilename) or os.path.exists(self.timesfilename)) == True:
            print "\n  WARNING: there are preexisting files from a previous recording."
            print "  Files are: " + self.audiofilename + ", " + self.timesfilename + "."
            print "  If recslides continues, files will be overwritten."
            continue_or_delete = raw_input("  Do you want to continue? (y/n): ")
            if continue_or_delete == ("y" or "y"):
                print "  Continuing to sound and times recording.\n"
                pass
            else:
                print "  recslides will exit now.\n"
                sys.exit()

        self.document = poppler.document_new_from_file (uri, None)
        self.n_pages = self.document.get_n_pages()
        self.page_selector = self.document.get_page(0)
        self.current_page = 0

        self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
        start_width, start_height = 400, 300
        self.win.set_default_size(start_width, start_height)
        self.win.set_title ("recslides")
        self.win.set_position(gtk.WIN_POS_CENTER)
        self.full_screen = 0
        self.win.connect("delete-event", gtk.main_quit)

        self.win.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.win.connect('button-press-event', self.button_press_event)

        self.width, self.height = self.win.get_size()
        self.page_width, self.page_height= self.page_selector.get_size()

        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24,
                                          int(self.width),
                                          int(self.height))

        vbox = gtk.VBox(False, 0)

        self.area = gtk.DrawingArea()
        black = gtk.gdk.color_parse("black")
        self.area.modify_bg(gtk.STATE_NORMAL, black)
        self.area.set_size_request(int(self.width), int(self.height))
        self.area.connect("expose-event", self.on_expose)

        vbox.pack_start(self.area, True, True, 0)

        self.win.add(vbox)

        self.win.show_all()

        self.player = gst.Pipeline("player")
        #~ self.clock = self.player.get_clock()

        self.source = gst.element_factory_make("alsasrc", "alsa-source")
        #~ self.caps = gst.Caps("audio/x-raw-int,rate=16000,channels=1")

        self.encoder = gst.element_factory_make("wavenc", "wavenc")

        self.fileout = gst.element_factory_make("filesink", "sink")
        self.fileout.set_property("location", self.audiofilename )

        self.player.add(self.source, self.encoder, self.fileout)
        gst.element_link_many(self.source, self.encoder, self.fileout)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('message', self.on_message)

        self.playing = False

        self.recording_time = self.player.get_last_stream_time()
        #~ self.file_times.write("supershow" + "\n")

        self.win.show_all()

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            gtk.main_quit()
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)


    #~ def query_position(self):
        #~ "Returns a (position, duration) tuple"
        #~ try:
            #~ position, format = self.player.query_position(gst.FORMAT_TIME)
        #~ except:
            #~ position = gst.CLOCK_TIME_NONE
#~
        #~ try:
            #~ duration, format = self.player.query_duration(gst.FORMAT_TIME)
        #~ except:
            #~ duration = gst.CLOCK_TIME_NONE

    def button_press_event(self, widget, event):
        if event.button == 1:
            if self.playing == False:
                self.win.fullscreen()
                self.playing = True
                starting = time.time()
                self.start = []
                self.start.append(starting)
                self.player.set_state(gst.STATE_PLAYING)
                self.file_times = open(self.timesfilename, 'w')
            elif self.playing == True:
                if self.current_page + 1 < self.n_pages:
                    self.starting_time = self.start[0]
                    right_now = time.time()
                    time_interval = str(int((right_now - self.starting_time)*1000))
                    self.file_times.write(time_interval + "\n")
                    self.current_page += 1
                    self.page_selector = self.document.get_page(self.current_page)
                    self.area.set_size_request(int(self.width),int(self.height))
                    self.area.queue_draw()
                elif self.current_page + 1 == self.n_pages:
                    right_now = time.time()
                    time_interval = str(int((right_now - self.starting_time)*1000))
                    self.file_times.write(time_interval + "\n")
                    self.file_times.close()
                    self.win.unfullscreen()
                    #~ self.win.resize(1,1)
                    time.sleep(0.5) # add half a second to avoid problems with iRaccoonShow
                    self.player.send_event(gst.event_new_eos())
                    self.current_page =+ 1

    def on_expose(self, widget, event):
        add_x = 0
        add_y = 0

        if (self.area.allocation.width/self.page_width) < (self.area.allocation.height/self.page_height):
            self.scale = self.area.allocation.width/self.page_width
        else:
            self.scale = self.area.allocation.height/self.page_height

        if (self.area.allocation.width/self.page_width) > (self.area.allocation.height/self.page_height):
            add_x= int(((self.area.allocation.width-(self.page_width*self.scale))/2)/self.scale)
        else:
            add_y= int(((self.area.allocation.height-(self.page_height*self.scale))/2)/self.scale)

        cr = widget.window.cairo_create()
        cr.set_source_surface(self.surface)
        cr.set_source_rgb(1, 1, 1)

        if self.scale != 1:
            cr.scale(self.scale, self.scale)

        cr.translate(add_x, add_y)
        cr.rectangle(0, 0, self.page_width, self.page_height)
        cr.fill()
        self.page_selector.render(cr)

    def gtk_main_quit(self, widget, event):
        gtk.main_quit()

    def main(self):
        gtk.main()


rec = rec_presentation()
rec.main()
