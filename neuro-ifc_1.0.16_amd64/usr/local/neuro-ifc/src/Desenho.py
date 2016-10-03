#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
import sys, pygame
from pygame.locals import *
import traceback


class Desenho(object):
    def __init__(self, lista):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480), 0, 32)
        self.blue = (0,0,255)
        self.red = (255, 0,0)
        self.white = (255,255,255)
        self.gray = (128,128,128)
        self.black = (0,0,0)
        self.screen.fill(self.black)
        self.clock = pygame.time.Clock()
        self.FPS = 30
        pygame.display.set_caption("Arquitetura de rede neural artificial feedforward")
        self.lista = lista

    def loopFrame(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    try:
                        pygame.quit()
                        sys.atexit()
                    except:
                        return None
                    #sys.exit()
            self.clock.tick(self.FPS)
            pygame.display.update()

    def criarArquitetura (self):
        try:


            lista_str = self.lista.split(",")
            try:
                lista = [ int(lista_str[i]) for i in xrange(len(lista_str) )]
            except:
                pygame.quit()
                sys.atexit()

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
                    pygame.draw.circle(self.screen,self.gray, (x,y*(aux+2)), tamNodo, 0)
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
                                pygame.draw.line(self.screen, self.blue, (coord[aux_X]+tamNodo,coord[aux_X+1]),(coord[aux_Y]-tamNodo,coord[aux_Y+1]), 2)
                            else:
                                break

                    index=i+1
                    i+=1
            self.loopFrame()
        except:
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            #print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)
