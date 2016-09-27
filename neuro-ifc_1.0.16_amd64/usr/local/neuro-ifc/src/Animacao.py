#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import sys

class Animacao(object):
    def __init__(self, erro):
        self.error = erro
        fig = plt.figure()
        self.y = list()
        self.epoca = len(erro)
        #intervalo = int(self.epoca*0.2)
        #print intervalo
        plt.xlim(0,len(erro)+5)
        plt.ylim(0, erro[0]*3)
        ani = animation.FuncAnimation(fig, self._animacao,
                   np.arange(0,self.epoca), repeat=False, interval = 30)
        plt.show()


    def _getError(self, index):
        return self.error[index]

    #funcao de animacao, ela eh chamada sequencialmente
    def _animacao(self, i):
        if i == self.epoca-1:
            sys.exit()
        self.y.append(self._getError(i))
        plt.plot(self.y)







#e = [18,15,12,10,0.77]
#p = Process(target=Animacao, args=(e,))
#p.start()
#p.join()
#a = Animacao(e)
#thread.start_new_thread(a.run, ())
