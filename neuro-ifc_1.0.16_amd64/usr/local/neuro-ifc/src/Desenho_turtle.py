#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
import turtle
class Desenho(object):
    def __init__(self):
        pen = turtle.Pen()
        pen.circle(40)
        pen.right(5)

        pen2 = turtle.Pen()
        pen2.speed(speed="slowest")
        pen2.forward(100)
        pen2.left(90)
        pen2.forward(100)
        pen2.left(90)
        pen2.forward(100)
        pen2.left(90)
        pen2.forward(100)

Desenho()
