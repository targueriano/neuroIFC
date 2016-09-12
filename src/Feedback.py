#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer

class Feedback(object):

    def __init__(self, status):
        self.status = status
        self._gerarContextos()

    def _gerarContextos(self):
        self.contexto_pronto = self.status.get_context_id("1")
        self.contexto_treinado = self.status.get_context_id("2")
        self.contexto_max = self.status.get_context_id("3")
        self.contexto_simulacao = self.status.get_context_id("4")
        self.contexto_erro = self.status.get_context_id("5")
        self.contexto_save = self.status.get_context_id("6")
        self.contexto_load = self.status.get_context_id("7")
        self.contexto_rede = self.status.get_context_id("8")
        self.contexto_train = self.status.get_context_id("9")
        self.contexto_erroSim = self.status.get_context_id("10")
        self.contexto_redeCriada = self.status.get_context_id("11")

    def gerarStatus(self, contexto):
        if contexto == self.contexto_pronto:
            self.status.push(self.contexto_pronto, "Pronto!")
        elif contexto == self.contexto_treinado:
            self.status.push(self.contexto_treinado, "O objetivo do aprendizado foi atingido.")
        elif contexto == self.contexto_max:
            self.status.push(self.contexto_max, "O objetivo não foi atingido dentro do número de épocas.")
        elif contexto == self.contexto_simulacao:
            self.status.push(self.contexto_simulacao, "Saída gerada com sucesso.")
        elif contexto == self.contexto_erro:
            self.status.push(self.contexto_erro, "Ocorreu uma exceção, verifique seu arquivo trace para mais informações.")
        elif contexto == self.contexto_save:
            self.status.push(self.contexto_save, "A configuração da rede não pode ser nula.")
        elif contexto == self.contexto_load:
            self.status.push(self.contexto_load, "O arquivo deve possuir extensão .net.")
        elif contexto == self.contexto_rede:
            self.status.push(self.contexto_rede, "Inserir arquivo de entrada antes de criar a rede.")
        elif contexto == self.contexto_train:
            self.status.push(self.contexto_train, "Verifique as fases anteriores antes de treinar.")
        elif contexto == self.contexto_erroSim:
            self.status.push(self.contexto_erroSim, "Realize as fases anteriores ou insira um arquivo com as entradas.")
        elif contexto == self.contexto_redeCriada:
            self.status.push(self.contexto_redeCriada, "RNA criada com sucesso.")
