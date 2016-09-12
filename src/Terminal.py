#!/usr/bin/env python

from gi.repository import Gtk, Vte
from gi.repository import GLib
import os
import subprocess

class Terminal(Vte.Terminal):

    def terminalVTE(self):
        super(Terminal, self)
        self.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/sh"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            )

    def subprocessTerminal(self):
        subprocess.call(["gnome-terminal", "&" ])
