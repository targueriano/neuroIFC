#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer


import matplotlib.pyplot as plt
import numpy as np
import neurolab as nl

class Animacao(object):
    """
    Para animar eu preciso saber dos pesos, do bias e das entradas
    """
    def __init__(self, inputs, net):
        self.inputs = inputs
        self.pesos = net.layers[0].np['w']
        self.bias = net.layers[0].np['b']

        self.animacao()


    def animacao(self):
        #pares ordenados para interpretacao geometrica
        x = list()
        y = list()
        y3 = list()
        e = self.inputs
        p = self.pesos
        b = self.bias
        print e
        print p
        print b
        aux_bias = 0
        #qtdade de entradas por amostra
        qtd_entrada = len(self.inputs[0])
        #verifica se eh par ou impar a fim de plotar entradas no plano cartesiano
        if qtd_entrada % 2 == 0: #par
            for i in xrange(len(self.inputs)):
                soma = 0
                for j in xrange(0,len(self.inputs[i]),2):
                    x.append(self.inputs[i][j])
                    y.append(self.inputs[i][j+1])
                    #----------------------------
                    soma += (e[i][j]*p[0][j] + b[0])/p[0][j+1]
                    soma *= -1
                    y3.append(soma)


        else: #impar
            for i in xrange(len(self.inputs)):
                for j in xrange(0,len(self.inputs[i])-1,2):
                    x.append(self.inputs[i][j])
                    y.append(self.inputs[i][j+1])
                    #----------------------------
                    soma += (e[i][j]*p[0][j] + b[0])/p[0][j+1]
                    soma *= -1
                    y3.append(soma)



        #y2 = [0,0,0,0]
        plt.xlim(-1,2)
        plt.ylim(-1,2)
        plt.grid()
        #plt.plot(x,y2,'b-')
        plt.plot(x,y, 'ro', x,y3,'g-')


        plt.annotate(u'estado final', xy=(0.5, 1), xytext=(1.5, 1.5),
            arrowprops=dict(facecolor='black',shrink=0.05))

        plt.annotate(u'estado inicial', xy=(0.5, 0), xytext=(0.5, -0.5),
            arrowprops=dict(facecolor='black',shrink=0.05))

        plt.show()
