#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer


import traceback
import cv2
import numpy as np
import sys

class Desenho(object):
    def __init__(self, lista):
        self.lista = lista
        self.BLUE = (255, 0, 0)
        self.RED = (0, 0, 255)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.BLACK = (0, 0, 0)
        #canvas = np.ones((300,400,3))*255
        canvas = np.zeros((500, 500,3), np.uint8)
        self.criarDesenho(canvas)

    def criarDesenho(self, canvas):
        try:
            lista_str = self.lista.split(',')
            try:
                lista = [ int(lista_str[i]) for i in xrange(len(lista_str) )]
            except:
                return None

            #posicao na tela (x,y)
            x = 25
            y = 15
            tamNodo = 10
            rate=3
            aux=0
            auxLine=0
            coord=list()
            for i in xrange(len(lista)):
                while lista[i] > 0:
                    cv2.circle(canvas, (x,y*(aux+2)), tamNodo, self.GRAY,-1)
                    #pygame.draw.circle(self.screen,self.gray, (x,y*(aux+2)), tamNodo, 0)
                    coord.append(x)
                    coord.append(y*(aux+2))
                    lista[i]-=1
                    aux+=rate

                coord.append(-1)
                x+=100
                aux=0

            i=0
            index=0
            while(i < len(coord)):
                if coord[i] != -1:
                    i+=2
                else:
                    for aux_X in xrange(index,i,2):
                        for aux_Y in xrange((i+1), len(coord),2 ):
                            if coord[aux_Y] != -1:
                                cv2.line(canvas,(coord[aux_X]+tamNodo,coord[aux_X+1]), (coord[aux_Y]-tamNodo,coord[aux_Y+1]), self.BLUE, 1)
                                #pygame.draw.line(self.screen, self.blue, (coord[aux_X]+tamNodo,coord[aux_X+1]),(coord[aux_Y]-tamNodo,coord[aux_Y+1]), 2)
                            else:
                                break

                    index=i+1
                    i+=1
            cv2.imshow("Arquitetura de rede neural artificial feedforward",canvas)
            cv2.waitKey(0)
        except:
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)


if __name__ == "__main__":
    Desenho(sys.argv[1])
