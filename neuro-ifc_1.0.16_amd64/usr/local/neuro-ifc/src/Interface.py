#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
#algoritmo para chamar a interface principal do neuroIFC
################################################################################
#Inserir:
#        1. Regra BFGS --- OK
################################################################################
import traceback
from __builtin__ import file
from cgi import log
import json
import random
import numpy as np
import Desenho as desenho
import RNA as rna
import Grafico as grafico
import Treinamento as treino
import Sobre as sobre
import thread
import time
import subprocess
import Terminal as terminal
import Animacao as anima
from multiprocessing import Process
import Information as info

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    from gi.repository import Gio
    from pyexcel_ods import get_data
    from pyexcel_ods import save_data
    import pylab
    import neurolab
    import pygame, sys
    from pygame.locals import *

except:
    #pega a excecao gerada
    trace = traceback.format_exc()
    #imprime
    print "Ocorreu um erro: \n",trace
    #salva em arquivo
    file("trace.log","a").write(trace)
    #encerra programa
    raise SystemExit

class Interface (object):
    '''
    Descrição:
    Classe principal para o programa neuroIFC. Classe que ficará responsável pela
    chamada do Gtk, versão do Debian 8, com Gnome 3.14.
    Utilização:
    Para iniciar o programa basta chamar essa classe com o comando:
    python Interface.py
    '''
    def __init__(self):
        gladeXML = "Interface.glade"
        builder = Gtk.Builder()
        builder.add_from_file(gladeXML)

        win = builder.get_object("window1")

        box = builder.get_object("box2")
        self.t = terminal.Terminal()
        box.add(self.t)

        #dicionario para a barra de status
        self.dir_context = {
            0:"Pronto!",
            1:"O objetivo do aprendizado foi atingido.",
            2:"O objetivo não foi atingido dentro do número de épocas.",
            3:"Saída gerada com sucesso.",
            4:"A configuração da rede não pode ser nula.",
            5:"O arquivo deve possuir extensão .net.",
            6:"Inserir arquivo de entrada antes de criar a rede.",
            7:"Verifique as fases anteriores antes de treinar.",
            8:"Realize as fases anteriores ou insira um arquivo com as entradas.",
            9:"RNA criada com sucesso.",
            10:"Crie uma RNA e realize um treinamento."
        }

        self.getVars(builder)

        #statusbar
        self.status = builder.get_object("statusbar1")
        self._statusDefault()

        self.statusFile = builder.get_object("statusbar2")
        contexto = self.statusFile.get_context_id("desconhecido")
        self.statusFile.push(contexto, "Desconhecido")

        #variaveis para arquitetura
        self.inputs = list()
        self.pesos = list()
        self.targets = list()
        self.errors = list()
        self.net = None
        self.saidaSimulador = list()
        self.inputSimulador = list()
        self.dialog = None


        win.show_all()
        builder.connect_signals({"gtk_main_quit":Gtk.main_quit,
                                 "on_butVerArquitetura_clicked": self.desenharArquitetura,
                                 "on_butTreinar_clicked": self.treinar,
                                 "on_butOpenEntradas_file_set": self.tratarEntrada,
                                 "on_butOpenSimulador_file_set":self.tratarDadosSimulacao,
                                 "on_butSimular_clicked": self.simular,
                                 "on_butGrafico_clicked":self.montarGrafico,
                                 "on_butGraficoSimulador_clicked":self.montarGraficoSimulador,
                                 "on_butOpenFast_clicked":self.pegarRedeSalva,
                                 "on_butSaveFast_clicked":self.salvar,
                                 "on_butCriarRede_clicked":self.criarRede,
                                 "on_butClearFast_clicked":self.limpar,
                                 "on_sobre_activate": self.sobre,
                                 "on_butTerminal_clicked": self.ativarTerminal,
                                 "on_menuOpen_activate": self.pegarRedeSalva,
                                 "on_menuSaveAs_activate": self.salvar,
                                 "on_menuClear_activate": self.limpar,
                                 "on_butSLP_clicked":self.treinarExemploSLP,
                                 "on_butMLP_clicked":self.treinarExemploMLP,
                                 "on_information_activate":self.verInformation,
                                 "on_sair_activate": Gtk.main_quit
                                 })



    def _statusDefault(self):
        contexto = self.status.get_context_id(self.dir_context[0])
        self.status.push(contexto,self.dir_context[0])

    def _statusDinamico(self, dic):
        contexto = self.status.get_context_id(dic)
        self.status.push(contexto, dic)
        time.sleep(5)
        self.status.pop(contexto)

    def verInformation(self, widget):
        info.DrawInformation()

    def treinarExemploMLP(self, widget):
        self.inputs = [[0,0],[0,1],[1,0],[1,1]]
        self.targets = [[0],[1],[1],[0]]
        ep = 500
        show = 1
        # Create network with 2 layers and random initialized
        self.net = neurolab.net.newff([[-7, 7], [-7, 7]],[5, 1])

        # Train network
        self.errors = self.net.train(self.inputs, self.targets, epochs=ep,
                                                        show=show, goal=0.02)
        #imprimir Regra de Aprendizado em dados
        self.storeRA.append([str(self.net.trainf)])
        #atualizar pesos e bias
        numTargets = [float(self.targets[i][j])
                        for i in xrange(len(self.targets)) for j in xrange(1)]
        self._setListStore(self.inputs, numTargets, True)
        #imprimir Erro
        for i in xrange(show-1, len(self.errors),show):
            self.storeErro.append((i+1, self.errors[i]))



    def treinarExemploSLP(self, widget):
        #AND logical
        self.inputs = [[0,0],[0,1],[1,0],[1,1]]
        self.targets = [[0],[0],[0],[1]]
        show = 1
        ep = 100
        # Create net with 2 inputs and 1 neuron
        self.net = neurolab.net.newp([[0, 1],[0, 1]], 1)

        # train with delta rule
        # see net.trainf
        self.errors = self.net.train(self.inputs, self.targets, epochs=ep,
                                            show=show, lr=0.1)
        #imprimir Regra de Aprendizado em dados
        self.storeRA.append([str(self.net.trainf)])
        #atualizar pesos e bias
        numTargets = [float(self.targets[i][j])
                        for i in xrange(len(self.targets)) for j in xrange(1)]
        self._setListStore(self.inputs, numTargets, True)
        #imprimir Erro
        for i in xrange(show-1, len(self.errors),show):
            self.storeErro.append((i+1, self.errors[i]))



    '''
    Descrição:
    Método responsável pelo desenho da RNA. Se as entradas foram inseridas,
    então o desenho as incluirá na primeira camada, caso contrário apenas
    será desenhado camada oculta(s) + saída.
    '''
    def desenharArquitetura(self, widget):
        if self.inputs:
            strTamEntradas = str(len(self.inputs[0]))
            strTamEntradas += ","
            strTamEntradas += self.listaNeuronios.get_text()
            d = desenho.Desenho(lista=strTamEntradas)
            d.criarArquitetura()
        else:
            lista = self.listaNeuronios.get_text()
            d = desenho.Desenho(lista=lista)
            d.criarArquitetura()

    def sobre(self,widget):
        sobre.Sobre()

    #terminal VTE
    def ativarTerminal(self, widget):
        self.t.terminalVTE()


    #Método para retornar ao estado inicial. Isso pode ser feito toda vez que
    #se deseja iniciar uma nova arquitetura com um novo treinamento.
    def limpar(self, widget):
        self.modelStore.clear()
        self.modelStoreErro.clear()
        self.modelStoreDados.clear()
        self.modelStorePesos.clear()
        self.modelStoreRA.clear()
        self.modelStoreBias.clear()

        self.pesos = list()
        self.errors = list()
        if self.net:
            self.net.reset
            self.net = None
        self.butOpenSimulador.unselect_all()
        self.butOpenEntradas.unselect_all()
        self.inputs = list()
        self.targets = list()
        self.inputSimulador = list()
        self.saidaSimulador = list()
        #limpar variaveis do simulador
        #status do arquivo
        contexto = self.statusFile.get_context_id("clear")
        self.statusFile.push(contexto, "Desconhecido")


    '''
    Descrição:
    Esse método abre uma janela de diálogo padrão do Gtk+ a fim de criar e
    armazenar um arquivo .net. Esse arquivo contém dados relacionados à RNA
    criada.
    Utilização: o evento apenas será gerado se houver uma RNA criada.
    '''
    def salvar(self, widget):
        try:
            if self.net and self.errors:
                self.dialog = Gtk.FileChooserDialog("Selecione o local e informe o nome do arquivo", None,
                    Gtk.FileChooserAction.SAVE,
                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                     Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

                response = self.dialog.run()
                if response == Gtk.ResponseType.OK:
                    nome = self.dialog.get_filename()+".net"
                    self.net.save(nome)

                #altera status para nome do arquivo
                contexto = self.statusFile.get_context_id("fileSave")
                self.statusFile.push(contexto,str(self.dialog.get_filename()))
                self.dialog.destroy()
            else:
                thread.start_new_thread(self._statusDinamico, (self.dir_context[10],))
        except:
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            #print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)
            self.dialog.destroy()

    #método para seleção de um arquivo .net, que contém dados referentes a uma
    #RNA salva.
    def pegarRedeSalva(self, widget):
        try:
            dialog = Gtk.FileChooserDialog("Por favor, escolha um arquivo .net",
                                None,
                                Gtk.FileChooserAction.OPEN,
                                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                #carrega o arquivo
                self.net = neurolab.load(dialog.get_filename())
                #extrai e coloca nos liststores
                numTargets = [float(self.targets[i][j])
                        for i in xrange(len(self.targets)) for j in xrange(1)]
                self._setListStore(self.inputs, numTargets, True)
                self.storeRA.append([str(self.net.trainf)])
                #altera status para nome do arquivo
                contexto = self.statusFile.get_context_id("fileAbrir")
                self.statusFile.push(contexto,str(dialog.get_filename()))

        except:
            thread.start_new_thread(self._statusDinamico,(self.dir_context[5],))
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            #print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)

        finally:
            dialog.destroy()

    '''
    Desrição:
    Esse método cria a rede neural artificial. Independente das entradas,
    o intervalo será entre -100 e 100 para cada entrada. O método verifica
    qual função de ativação está selecionada, depois chama a classe responsável
    pela criação em si. Se não ocorrer nenhuma exceção, então será impresso
    os dados relacionaos à rede.
    '''
    def criarRede(self, widget):
        try:
            #criar o intervalo de entradas
            intervalo = [[-100, 100] for i in xrange(len(self.inputs[0]))]
            #criar a rede neural artificial
            rede = rna.Rede(intervalo, self.linear.get_active(),
                                    self.heaviside.get_active(),
                                    self.tangente.get_active(),
                                    self.sigmoide.get_active(),
                                            self.listaNeuronios)
            self.net = rede.criarRede()
            numTargets = [float(self.targets[i][j])
                    for i in xrange(len(self.targets)) for j in xrange(1)]

            self._setListStore(self.inputs, numTargets, True)

            #status
            thread.start_new_thread(self._statusDinamico,(self.dir_context[9],))
        except:
            thread.start_new_thread(self._statusDinamico,(self.dir_context[6],))
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            #print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)

    def carregarSpinner(self):
        self.spinner.start()

    def aprender(self):
        try:
            tr = treino.Treinamento(self.net, self.inputs,
                self.targets, self.epocas, self.show, self.objetivo,
                self.taxaAprendizado,self.taxaIncremento, self.taxaDecremento,
                                        self.impulso, self.taxaRegularizacao)
            #treinar
            if self.delta.get_active():
                self.errors = tr.treinar("delta")

            elif self.gd.get_active():
                self.errors = tr.treinar("gd")

            elif self.gdm.get_active():
                self.errors = tr.treinar("gdm")

            elif self.gda.get_active():
                self.errors = tr.treinar("gda")

            elif self.gdx.get_active():
                self.errors = tr.treinar("gdx")

            elif self.rprop.get_active():
                self.errors = tr.treinar("rprop")

            elif self.bfgs.get_active():
                self.errors = tr.treinar("bfgs")

            #imprimir Erro
            for i in xrange(self.show.get_value_as_int()-1, len(self.errors),
                                        self.show.get_value_as_int()):
                self.storeErro.append((i+1, self.errors[i]))

            #imprimir Regra de Aprendizado em dados
            self.storeRA.append([str(self.net.trainf)])
            #atualizar pesos e bias
            numTargets = [float(self.targets[i][j])
                        for i in xrange(len(self.targets)) for j in xrange(1)]
            self._setListStore(self.inputs, numTargets, True)

            if len(self.errors) < self.epocas.get_value_as_int():
                thread.start_new_thread(self._statusDinamico,(self.dir_context[1],))
            else:
                thread.start_new_thread(self._statusDinamico,(self.dir_context[2],))

            if self.switchAnimacao.get_active() and len(self.errors) <= 100:
                self._animarErro()

        except:
            thread.start_new_thread(self._statusDinamico,(self.dir_context[7],))
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            #print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)
        finally:
            self.spinner.stop()

    '''
    Descrição:
    Método privado chamado quando o switch está ativo. Esse método cria um novo
    processo para criar um gráfico animado por meio do matplotlib.
    Utilização:
    A quantidade de erros deve ser menor ou igual a 100.
    '''
    def _animarErro(self):
        try:
            p = Process(target=anima.Animacao, args=(self.errors,))
            p.start()
            p.join()
        except:
            #pega a excecao gerada
            trace = traceback.format_exc()
            file("trace.log","a").write(trace)
        finally:
            p.terminate()

    '''
    Descrição:
    Esse método cria duas threads. Uma para o processo de aprendizado e outra
    para o spinner. O fim das threads acontece quando o treinamento termina.
    '''
    def treinar(self,widget):
        thread.start_new_thread(self.carregarSpinner,())
        thread.start_new_thread(self.aprender,())


    """
    Descrição:
    Lê e interpreta o arquivo de entrada (.ods). O método chama o extrair_dados,
    que acessa o arquivo, coloca-os numa lista de duas dimensões e separa-os da
    seguinte forma:
    1  4  5  7 -1
    2  4  2 -3  1
    inputs = [[1,4,5,7], [2,4,2,-3]]
    targets = [[-1], [1]]
    Os arquivos devem apenas possuir uma saída.
    """
    def tratarEntrada(self, widget):
        try:
            self.inputs = list()
            self.targets = list()
            caminho = None
            caminho = self.butOpenEntradas.get_filename()
            novaf = self.extrair_dados(caminho)
            if novaf:
                #tam = len(novaf[0])-1
                for i in range(len(novaf)):
                    self.targets.append(novaf[i][-1])
                    del novaf[i][-1]

                self.targets = [[self.targets[i]]
                                        for i in xrange(len(self.targets))]
                self.inputs = novaf

        except:
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)

    def extrair_dados(self, caminho):
        try:
            data = get_data(caminho)
            nova = list()
            for i in xrange(len(data)):
                if data[i]:
                    nova.append(data[i])

            return nova
        except:
            trace = traceback.format_exc()
            file("trace.log","a").write(trace)


    def tratarDadosSimulacao(self, widget):
        try:
            caminho = self.butOpenSimulador.get_filename()
            novaf = self.extrair_dados(caminho)
            self.inputSimulador = novaf
        except:
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)

    '''
    Descrição:
    Método privado para configurar e inserir os dados na tela.
    '''
    def _setListStore(self, input, target, dados):
        if dados:
            for i in xrange(len(input)):
                self.storeDados.append((str(input[i]), target[i]) )

            pesos = self.net.layers[0].np['w']
            pesos = [[str(pesos[i][j])] for i in xrange(len(pesos))
                                            for j in xrange(len(pesos[0]))]
            for i in xrange(len(pesos)):
                self.storePesos.append(pesos[i])


            bias = self.net.layers[0].np['b']
            bias = [[str(bias[i])] for i in xrange(len(bias))]
            for i in range(len(bias)):
                self.storeBias.append(bias[i])


        else:
            for i in xrange(len(self.saidaSimulador)):
                self.store.append((str(input[i]),
                                    target[i],
                                    float(self.saidaSimulador[i])
                                 ))

    def simular(self, widget):
        try:
            if self.butOpenSimulador.get_filename():
                self.saidaSimulador = self.net.sim(self.inputSimulador)
                numTargets = [0 for i in xrange(len(self.inputSimulador)) ]
                self._setListStore(self.inputSimulador, numTargets, False)
            else:
                self.saidaSimulador = self.net.sim(self.inputs)
                numTargets = [float(self.targets[i][j])
                        for i in xrange(len(self.targets)) for j in xrange(1)]
                self._setListStore(self.inputs, numTargets, False)

            #self.feedStatus.gerarStatus(self.feedStatus.contexto_simulacao)
            thread.start_new_thread(self._statusDinamico,(self.dir_context[3],))

        except:
            #self.feedStatus.gerarStatus(self.feedStatus.contexto_erroSim)
            thread.start_new_thread(self._statusDinamico,(self.dir_context[8],))
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            #print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)


    def montarGrafico(self, widget):
        graf = grafico.Grafico(self.errors, self.saidaSimulador,
                                                self.inputs, self.targets)
        graf.gerarGraficoErro()
        #anima.Animacao(self.inputs, self.net)


    def montarGraficoSimulador(self, widget):
        if not self.butOpenSimulador.get_filename():
            graf = grafico.Grafico(self.errors, self.saidaSimulador,
                                                self.inputs, self.targets)
            graf.gerarGraficoSimulacao()

    def getVars(self, builder):
        #variaveis da 1 fase
        self.butOpenEntradas = builder.get_object("butOpenEntradas")

        #variaveis 2 Fase
        self.listaNeuronios = builder.get_object("listaNeurons")
        self.epocas = builder.get_object("spinEpocas")
        self.objetivo = builder.get_object("spinObjetivo")
        self.show = builder.get_object("spinShow")
        self.taxaAprendizado = builder.get_object("spinTaxaAprendizado")
        self.impulso = builder.get_object("spinImpulso")
        self.taxaRegularizacao = builder.get_object("spinRegularizacao")
        self.taxaIncremento = builder.get_object("spinTaxaIncremento")
        self.taxaDecremento = builder.get_object("spinTaxaDecremento")

        #variaveis da 3 Fase
        self.delta = builder.get_object("radioDelta")
        self.gd = builder.get_object("radioGD")
        self.gdm = builder.get_object("radioGDM")
        self.gdx = builder.get_object("radioGDX")
        self.gda = builder.get_object("radioGDA")
        self.rprop = builder.get_object("radioRPROP")
        self.bfgs = builder.get_object("radioBFGS")

        #variaveis da 4 Fase
        self.heaviside = builder.get_object("radioHeaviside")
        self.linear = builder.get_object("radioLinear")
        self.tangente = builder.get_object("radioTangente")
        self.sigmoide = builder.get_object("radioSigmoide")

        #variaveis 6 Fase
        self.switchAnimacao = builder.get_object("switch1")

        #variaveis 7 Fase
        self.butOpenSimulador = builder.get_object("butOpenSimulador")

        #liststore
        self.store = builder.get_object("liststore1")
        self.storeErro = builder.get_object("liststore2")
        self.storeDados = builder.get_object("liststore3")
        self.storePesos = builder.get_object("liststore4")
        self.storeBias = builder.get_object("liststore5")
        self.storeRA = builder.get_object("liststore6")

        #textview
        self.modelStore = builder.get_object("treeview1").get_model()
        self.modelStoreErro = builder.get_object("treeview2").get_model()
        self.modelStoreDados = builder.get_object("treeview3").get_model()
        self.modelStorePesos = builder.get_object("treeview4").get_model()
        self.modelStoreBias = builder.get_object("treeview5").get_model()
        self.modelStoreRA = builder.get_object("treeview6").get_model()

        #spinner
        self.spinner = builder.get_object("spinner1")


if __name__ == "__main__":
    Interface()
    Gtk.main()
