#!/usr/bin/env python
import gi
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, Vte
from gi.repository import GLib
import os
import time
import subprocess

def command_on_VTE(self,command):
    length=len(command)
    self.terminal.feed_child(command, length)


class Terminal(Vte.Terminal):

    def terminalVTE(self):
        self.terminal = super(Terminal, self)
        self.terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/sh"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            )


    def getTerminalVTE(self, erros):
        #primeiro tem q descobrir o ID do terminal desejado
        #Para isso usa-se o cmd tty e lanca a saida no dir tmp
        command_on_VTE(self, '''tty > /tmp/terminal_number\n''')

        #agora verifica se o arquivo terminal_number existe...
        #se sim, pega referencia do caminho e atribui numa var global
        # read the terminal ID
        while not os.path.exists("/tmp/terminal_number"):
            time.sleep(0.1)
        with open('/tmp/terminal_number', 'r') as f:
            self.VTE_redirect_path=f.readline()
            os.remove('/tmp/terminal_number')

         # this cleans the vte
        os.system('''printf "\\033c" > {0}'''.format(self.VTE_redirect_path))


        for err in erros:
            os.system(str(err).format(rdc=self.VTE_redirect_path))


    def subprocessTerminal(self, lista):
        path = "/usr/local/neuro-ifc/src/"
        os.chdir(path)
        subprocess.call(["./Desenho_cv2.py", lista ])
