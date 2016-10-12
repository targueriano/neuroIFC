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

        plt.title("Erro durante treinamento")
        plt.xlim(0,len(erro))
        plt.ylim(0, erro[0]*3)
        plt.xlabel('Epoch')
        plt.ylabel('Erro (default SSE)')
        ani = animation.FuncAnimation(fig, self._animacao,
                   np.arange(0,self.epoca), repeat=False, interval = 30)
        plt.show()


    def _getError(self, index):
        return self.error[index]

    #funcao de animacao, ela eh chamada sequencialmente
    def _animacao(self, i):
        if i == self.epoca-1:
            return True
        self.y.append(self._getError(i))
        plt.plot(self.y)
