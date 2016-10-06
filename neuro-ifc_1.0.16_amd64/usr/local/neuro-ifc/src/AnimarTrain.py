#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

"""
x = qtdade de letras
y = numero do ciclo, funcao de soma para cada entrada
"""
class AnimarTrain(object):
    def __init__(self):
        self.font = {'family': 'serif',
                'color':  'darkred',
                'weight': 'normal',
                'size': 10,
                }
        #plt.xlabel('size', fontdict=self.font)
        #plt.ylabel('instructions', fontdict=self.font)

        self.dir_text = {0:"Entrada = [[0,0], [0,1], [1,0], [1,1]]",
                1:"Alvo (logic AND) = [[0], [0], [0], [1]]",
                2:"Taxa de aprendizado = 0.5",
                3:"Pesos = [0,0,0]",
                4:"Bias = [1,1,1,1]",
                5:"ciclo 1 (Hard_limiter(SOMA)) >> f(w0 * x0 + w1 * x1 + w2 * x2)",
                6:"Entrada 1: s = f(0 * 1 + 0 * 0 + 0 * 0) = f(0) = alvo",
                7:"Entrada 2: s = f(0 * 1 + 0 * 1 + 0 * 0) = f(0) = alvo",
                8:"Entrada 3: s = f(0 * 1 + 0 * 0 + 0 * 1) = f(0) = alvo",
                8:"Entrada 4: s = f(0 * 1 + 0 * 1 + 0 * 1) = f(0) != alvo",
                9:"s diferente do alvo, ajusta pesos:",
                10:"w0 = w0 + (taxa * (alvo - s)*x0) = 0 + (0.5 * (1-0)*1)=0.5",
                11:"w1 = w1 + (taxa * (alvo - s)*x0) = 0 + (0.5 * (1-0)*1)=0.5",
                12:"w2 = w2 + (taxa * (alvo - s)*x0) = 0 + (0.5 * (1-0)*1)=0.5",
                13:"ciclo 2",
                14:"Entrada 1: s = f(0.5*1 + 0.5*0 + 0.5*0) = f(0.5) != alvo",
                15:"w0 = w0 +(taxa * (alvo-s)*x0) = 0.5 + (0.5 * (0-1)*1) = 0",
                16:"w1 = 0.5 + (0.5 * (0-1)*0) = 0.5",
                17:"w2 = 0.5 + (0.5 * (0-1)*0) = 0.5",
                18:"Entrada 2: s = f(0*1 + 0.5*0 + 0.5*1) = f(0.5) != alvo",
                19:"w0 = w0 + (taxa * (alvo-s)*x0) = 0 + (0.5 * (0-1)*1) = -0.5",
                20:"w1 = 0.5 + (0.5 *(0-1)*0) = 0.5",
                21:"w2 = 0.5 + (0.5 *(0-1)*1) = 0",
                22:"Entrada 3: s = f(-0.5*1 + 0.5*1 + 0*0) = f(0) = alvo",
                23:"Entrada 4: s = f(-0.5*1 + 0.5*1 + 0*1) = f(0) != alvo",
                24:"w0 = -0.5 + (0.5 *(1-0)*1) = 0",
                25:"w1 =  0.5 + (0.5 *(1-0)*1) = 1",
                26:"w2 =  0 + (0.5 *(1-0)*1) = 0.5",
                27:"ciclo 3",
                28:"Entrada 1: s = f(0*1 + 1*0 + 0.5*0) = f(0) = alvo",
                29:"Entrada 2: s = f(0*1 + 1*0 + 0.5*1) = f(0.5) != alvo",
                30:"w0 = w0 +(taxa * (alvo-s)*x0) = -0.5 + (0.5 *(0-1)*1) = -1",
                31:"w1 = 1 + (0.5 *(0-1)*0 = 1",
                32:"w2 = 0.5 + (0.5 *(0-1)*1) = 0",
                33:"Entrada 3: s = f(-1*1 + 1*1 + 0*0) = f(0) = alvo",
                34:"Entrada 4: s = f(-1*1 + 1*1 + 0*1) = f(0) != alvo",
                35:"w0 = -1 + (0.5 *(1-0)*1) = -0.5",
                36:"w1 =  1 + (0.5 *(1-0)*1) = 1.5",
                37:"w2 =  0 + (0.5 *(1-0)*1) = 0.5",
                38:"ciclo 4",
                39:"Entrada 1: s = f(-0.5*1 + 1.5*0 + 0.5*0) = f(-0.5) = alvo",
                40:"Entrada 2: s = f(-0.5*1 + 1.5*0 + 0.5*1) = f(0) = alvo",
                41:"Entrada 3: s = f(-0.5*1 + 1.5*1 + 0.5*0) = f(1) != alvo",
                42:"w0 = -1, w1 = 1, w2 = 0.5",
                43:"Entrada 4: s = f(-1*1 + 1*1 + 0.5*1) = f(0.5) = alvo",
                44:"ciclo 5",
                45:"Entrada 1: s = f(-1*1 + 1*0 + 0.5*0) = f(-1) = alvo",
                46:"Entrada 2: s = f(-1*1 + 1*0 + 0.5*1) = f(-0.5) = alvo",
                47:"Entrada 3: s = f(-1*1 + 1*1 + 0.5*0) = f(0) = alvo",
                48:"Entrada 4: s = f(-1*1 + 1*1 + 0.5*1) = f(0.5) = alvo",
                49:"Como saidas convergem, fim do treinamento.",
                50:"Pesos finais: [-1, 1, 0.5]"
                }


        #plt.title("Passo a passo - SLP - AND")
        fig = plt.figure()
        self.y = list()
        self.x = 3
        self.aux = 300
        plt.xlim(0,500)
        plt.ylim(-100,300)

        ani = animation.FuncAnimation(fig, self._animacao,
                   np.arange(0,51), repeat=False, interval = 500)
        plt.show()

    def _getDir(self, index):
        self.aux-=10
        return self.aux

    #funcao de animacao, ela eh chamada sequencialmente
    def _animacao(self, i):
        self.aux = self._getDir(i)
        if i == 38:
            self.x *= 90
            self.aux = 290
        plt.text(self.x, self.aux, self.dir_text[i], fontdict=self.font)
