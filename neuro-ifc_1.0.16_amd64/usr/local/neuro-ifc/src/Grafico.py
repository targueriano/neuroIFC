#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer

import pylab as pl
import numpy as np


class Grafico(object):
    def __init__(self, erro, outSim, inputs, targets):
        self.erro = erro
        self.outSim = outSim
        self.inputs = inputs
        self.targets = targets

    def gerarGraficoErro(self):
        pl.plot(self.erro)
        pl.title("F(epoch) = erro")
        pl.xlabel('Epoch')
        pl.ylabel('Erro (default SSE)')
        pl.grid()
        pl.show()


    def gerarGraficoSimulacao(self):
        try:
            x = np.array(self.inputs)
            y = np.array(self.targets)
            y2 = self.outSim.reshape(len(x))
            x_list = list()
            for i in xrange(len(x)):
                x_sum=0
                for j in xrange(len(x[i])):
                    x_sum += x[i][j]
                x_list.append(x_sum)

            pl.plot(x_list, y2, "-",x_list , y, ".", x_list, y2,"p")
            pl.legend(['Obtidos', 'Desejados'])
            pl.grid()
            pl.title("Valores obtidos e desejados")
            pl.show()
        except:
            pass
