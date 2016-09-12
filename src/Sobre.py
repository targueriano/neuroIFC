#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Sobre(object):
    def __init__(self):
        gladeSobre = "Sobre.glade"
        builder = Gtk.Builder()
        builder.add_from_file(gladeSobre)
        win = builder.get_object("aboutdialog1")

        win.show()
        builder.connect_signals({"gtk_main_quit":Gtk.main_quit})
