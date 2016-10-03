#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DrawPerceptron(object):
    def __init__(self):
        gladeXML = "imagePerceptron.glade"
        builder = Gtk.Builder()
        builder.add_from_file(gladeXML)

        win = builder.get_object("window1")

        win.show_all()
        builder.connect_signals({"gtk_main_quit":Gtk.main_quit,})
