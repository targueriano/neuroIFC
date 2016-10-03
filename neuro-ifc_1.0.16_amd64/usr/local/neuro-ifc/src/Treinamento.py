#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
import neurolab

class Treinamento(object):

    def __init__(self, net, inputs, targets, epocas, show, goal, lr, lr_inc, lr_dec, mc, rr):
        self.net = net
        self.inputs = inputs
        self.targets = targets
        self.epocas = epocas
        self.show = show
        self.objetivo = goal
        self.taxaAprendizado = lr
        self.taxaIncremento = lr_inc
        self.taxaDecremento = lr_dec
        self.taxaImpulso = mc
        self.taxaRegularizacao = rr
        self.errors = list()


    def treinar(self, regra):
        if regra == "delta":
            self.errors = self.net.train(self.inputs, self.targets,
                            epochs=self.epocas.get_value_as_int(),
                            show=self.show.get_value_as_int(),
                            lr=self.taxaAprendizado.get_value()
                          )
            return self.errors
        elif regra == "gd":
            self.net.trainf = neurolab.train.train_gd
            print self.net.trainf
            self.errors = self.net.train(self.inputs, self.targets,
                                epochs=self.epocas.get_value_as_int(),
                                show=self.show.get_value_as_int(),
                                goal=self.objetivo.get_value(),
                                lr=self.taxaAprendizado.get_value()
                                )
            return self.errors
        elif regra == "gdm":
            self.net.trainf = neurolab.train.train_gdm
            self.errors = self.net.train(self.inputs, self.targets,
                            epochs=self.epocas.get_value_as_int(),
                                show=self.show.get_value_as_int(),
                                         goal=self.objetivo.get_value(),
                                         lr=self.taxaAprendizado.get_value(),
                                         mc=self.taxaImpulso.get_value(),
                                         rr=self.taxaRegularizacao.get_value()
                                        )
            return self.errors
        elif regra == "gda":
            self.net.trainf = neurolab.train.train_gda
            self.errors = self.net.train(self.inputs, self.targets,
                            epochs=self.epocas.get_value_as_int(),
                                show=self.show.get_value_as_int(),
                                         goal=self.objetivo.get_value(),
                                         lr=self.taxaAprendizado.get_value(),
                                         lr_inc=self.taxaIncremento.get_value(),
                                         lr_dec=self.taxaDecremento.get_value(),
                                         rr=self.taxaRegularizacao.get_value()
                                        )
            return  self.errors
        elif regra == "gdx":
            self.net.trainf = neurolab.train.train_gdx
            print self.net.trainf
            self.errors = self.net.train(self.inputs, self.targets,
                            epochs=self.epocas.get_value_as_int(),
                                show=self.show.get_value_as_int(),
                                         goal=self.objetivo.get_value(),
                                         lr=self.taxaAprendizado.get_value(),
                                         lr_inc=self.taxaIncremento.get_value(),
                                         lr_dec=self.taxaDecremento.get_value(),
                                         mc=self.taxaImpulso.get_value(),
                                         rr=self.taxaRegularizacao.get_value()
                                        )
            return self.errors
        elif regra == "rprop":
            self.net.trainf = neurolab.train.train_rprop
            self.errors = self.net.train(self.inputs, self.targets,
                            epochs=self.epocas.get_value_as_int(),
                                show=self.show.get_value_as_int(),
                                         goal=self.objetivo.get_value(),
                                         lr=self.taxaAprendizado.get_value(),
                                        )
            return self.errors

        elif regra == "bfgs":
            self.net.trainf = neurolab.train.train_bfgs
            self.errors = self.net.train(self.inputs, self.targets,
                                          epochs=self.epocas.get_value_as_int(),
                                          show=self.show.get_value_as_int(),
                                          goal=self.objetivo.get_value(),
                                          rr=self.taxaRegularizacao.get_value()
                                         )
            return self.errors
