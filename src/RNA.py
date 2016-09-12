#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
import neurolab as nl
import traceback

class Rede(object):

    def __init__(self, intervaloEntrada, linear, degrau, hiperbolica, logistica, listaNeuronios):
        self.intervaloEntrada = intervaloEntrada
        self.linear = linear
        self.degrau = degrau
        self.hiperbolica = hiperbolica
        self.logistica = logistica
        self.listaNeuronios = listaNeuronios.get_text()

    def criarRede(self):
        try:
            listaNeuronios = self.listaNeuronios.split(',')
            self.listaNeuronios = [int(listaNeuronios[i]) for i in xrange(len(listaNeuronios))]

            #Se x != 1 entao multilayer, senao singlelayer
            if len(self.listaNeuronios) > 1 and self.listaNeuronios[0] != 1:
                trans=list()
                #criando rede artificial n entradas e 2+ neuronios + funcao de ativacao
                if self.logistica:
                    logsig = nl.trans.LogSig()
                    for i in range(len(self.listaNeuronios)):
                        trans.append(logsig)
                    net = nl.net.newff(self.intervaloEntrada, self.listaNeuronios, trans)
                else:
                    tansig = nl.trans.TanSig()
                    for i in range(len(self.listaNeuronios)):
                        trans.append(tansig)
                    net = nl.net.newff(self.intervaloEntrada, self.listaNeuronios, trans)
            else:
                if self.linear:
                    net = nl.net.newp(self.intervaloEntrada, int(self.listaNeuronios[0]), nl.trans.SatLin())
                elif self.degrau:
                    net = nl.net.newp(self.intervaloEntrada, int(self.listaNeuronios[0]), nl.trans.HardLim() )
                elif self.logistica:
                    net = nl.net.newp(self.intervaloEntrada, int(self.listaNeuronios[0]), nl.trans.LogSig())
                elif self.hiperbolica:
                    net = nl.net.newp(self.intervaloEntrada, int(self.listaNeuronios[0]), nl.trans.TanSig())

            return net

        except:
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            #print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)
