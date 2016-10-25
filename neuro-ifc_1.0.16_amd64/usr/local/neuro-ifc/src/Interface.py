#!/usr/bin/env python
#-*- coding: utf-8 -*-
#autor Taylan Branco Meurer
#algoritmo para chamar a interface principal do neuroIFC
################################################################################
#Inserir:
#        1. Titulo de cada secao
#        2. status mais ativos
#        3. colocar regra de treinamento na segunda fase
#        4. ocultar entradas conforme regra escolhida
#        5. mostrar rna e seus parametros
#        6. titulo de cada grafico
#        7. incluir erro (SSE ou MSE ou MAP) na tabela de simulacao
#        8. perguntar antes de apagar tudo
################################################################################
import traceback
from __builtin__ import file
import numpy as np
#import Desenho as desenho
#import Desenho_cv2 as cv2
import RNA as rna
import Grafico as grafico
import Treinamento as treino
import Sobre as sobre
import thread
import time
#import subprocess
import Terminal as terminal
import Animacao as anima
from multiprocessing import Process
import Information as info

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk
    from gi.repository import Gio
    from pyexcel_ods import get_data
    from pyexcel_ods import save_data
    import neurolab
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
            10:"Crie uma RNA e realize um treinamento.",
            11:"Treinando...",
            12:"Dados inseridos com sucesso!",
            13:"O arquivo deve ter extensão .ods.",
            14:"Arquivo incorreto, verifique a configuração da rede.",
            15:"A rede deve possuir apenas um neurônio na camada de saída.",
            16:"A RNA foi salva com sucesso!",
            17:"Arquivo aberto com sucesso!"
        }

        self.novoContexto = 1
        self.dir_context_path = {
            0:"Desconhecido",
            1:"Novo"
        }

        self.getVars(builder)

        #statusbar
        self.status = builder.get_object("statusbar1")
        self.statusFile = builder.get_object("statusbar2")
        self._statusDefault()

        self._fontColor("black")

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
                                 "on_radioDelta_clicked":self.ativarDelta,
                                 "on_radioGDM_clicked":self.ativarGDM,
                                 "on_radioGD_clicked":self.ativarGD,
                                 "on_radioGDA_clicked":self.ativarGDA,
                                 "on_radioGDX_clicked":self.ativarGDX,
                                 "on_radioRPROP_clicked": self.ativarRPROP,
                                 "on_radioBFGS_clicked": self.ativarBFGS,
                                 "on_sair_activate": Gtk.main_quit
                                 })


    def _fontColor(self, cor):
        self.status.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse(cor))

    def ativarBFGS(self, widget):
        self._desativarEntradas()
        self.taxaRegularizacao.set_sensitive(True)
        self._ativarListaNeuronios()
        self._ativarFuncTrainMLP()

    def ativarRPROP(self, widget):
        self._desativarEntradas()
        self._ativarListaNeuronios()
        self._ativarFuncTrainMLP()

    def ativarGDX(self, widget):
        self.impulso.set_sensitive(True)
        self.taxaRegularizacao.set_sensitive(True)
        self.taxaDecremento.set_sensitive(True)
        self.taxaIncremento.set_sensitive(True)
        self._ativarListaNeuronios()
        self._ativarFuncTrainMLP()


    def ativarGDA(self, widget):
        self._desativarEntradas()
        self.taxaRegularizacao.set_sensitive(True)
        self.taxaDecremento.set_sensitive(True)
        self.taxaIncremento.set_sensitive(True)
        self._ativarListaNeuronios()
        self._ativarFuncTrainMLP()


    def _desativarEntradas(self):
        self.taxaRegularizacao.set_sensitive(False)
        self.taxaDecremento.set_sensitive(False)
        self.taxaIncremento.set_sensitive(False)
        self.impulso.set_sensitive(False)
        self.listaNeuronios.set_sensitive(False)
        #######
        self.linear.set_sensitive(False)
        self.heaviside.set_sensitive(False)
        self.tangente.set_sensitive(False)
        self.sigmoide.set_sensitive(False)

    def _ativarListaNeuronios(self):
        self.listaNeuronios.set_text('3,3,1')
        self.listaNeuronios.set_sensitive(True)

    def ativarGDM(self, widget):
        self._desativarEntradas()
        self.taxaRegularizacao.set_sensitive(True)
        self.impulso.set_sensitive(True)
        self._ativarListaNeuronios()
        self._ativarFuncTrainMLP()


    def ativarGD(self, widget):
        self._desativarEntradas()
        self._ativarListaNeuronios()
        self._ativarFuncTrainMLP()

    def _ativarFuncTrainMLP(self):
        self.tangente.set_sensitive(True)
        self.tangente.set_active(True)
        self.sigmoide.set_sensitive(True)


    def ativarDelta(self, widget):
        self._desativarEntradas()
        self.listaNeuronios.set_text("1")
        self.listaNeuronios.set_sensitive(False)
        #####
        self.heaviside.set_sensitive(True)
        self.heaviside.set_active(True)
        self.linear.set_sensitive(True)

    def _statusDefault(self):
        contexto = self.status.get_context_id(self.dir_context[0])
        self.status.push(contexto,self.dir_context[0])
        contexto = self.statusFile.get_context_id(self.dir_context_path[0])
        self.statusFile.push(contexto, self.dir_context_path[0])

    """
    Descricao: Thread que recebe um dicionario de status,
    altera-o conforme o parametro e dorme por 2 segundos.
    Depois volta ao estado pronto.
    """
    def _statusDinamico(self, dic):
        contexto = self.status.get_context_id(dic)
        self.status.push(contexto, dic)
        time.sleep(2)
        self.status.pop(contexto)
        self._fontColor("black")

    def _statusPathFile(self, caminho):
        self.novoContexto = self.statusFile.get_context_id(self.dir_context_path[1])
        self.statusFile.push(self.novoContexto, caminho)

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

        self._setStoreDados(self.targets)
        self._setListPesosBias()

        self._desativarFases()
        self.butOpenSimulador.set_sensitive(True)
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

        self._setStoreDados(self.targets)

        self._desativarFases()
        self.butOpenSimulador.set_sensitive(True)

        self._setListPesosBias()
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
        try:
            t = self.listaNeuronios.get_text().split(',')
            for i in xrange(len(t)):
                if int(t[i]) > 10:
                    raise


            if self.inputs:
                strTamEntradas = str(len(self.inputs[0]))
                strTamEntradas += ","
                strTamEntradas += self.listaNeuronios.get_text()

                terminal.Terminal().subprocessTerminal(strTamEntradas)

            else:
                lista = self.listaNeuronios.get_text()
                terminal.Terminal().subprocessTerminal(lista)
        except:
            trace = traceback.format_exc()
            file("trace.log","a").write(trace)
            #p.terminate()


    def sobre(self,widget):
        sobre.Sobre()

    #terminal VTE
    def ativarTerminal(self, widget):
        self.t.terminalVTE()

    def _desativarFases(self):
        self.fase1.set_sensitive(False)
        self.fase2.set_sensitive(False)
        self.fase3.set_sensitive(False)
        self.fase4.set_sensitive(False)
        self.fase5.set_sensitive(False)
        self.fase6.set_sensitive(False)

    def _ativarFases(self):
        self.fase1.set_sensitive(True)
        self.fase2.set_sensitive(True)
        self.fase3.set_sensitive(True)
        self.fase4.set_sensitive(True)
        self.fase5.set_sensitive(True)
        self.fase6.set_sensitive(True)



    #Método para retornar ao estado inicial. Isso pode ser feito toda vez que
    #se deseja iniciar uma nova arquitetura com um novo treinamento.
    def limpar(self, widget):
        #desativar botoes
        self.butCriarRNA.set_sensitive(False)
        self.butTreinar.set_sensitive(False)
        self.butOpenSimulador.set_sensitive(False)
        self.butSimular.set_sensitive(False)
        self.butGraficoTreinar.set_sensitive(False)
        self.butGraficoSimulador.set_sensitive(False)
        self.butSaveFast.set_sensitive(False)
        self.menuSaveAs.set_sensitive(False)
        self.switchAnimacao.set_sensitive(False)

        self._ativarFases()

        self.modelStore.clear()
        self.modelStoreErro.clear()
        self.modelStoreDados.clear()
        self.modelStorePesos.clear()
        self.modelStoreRA.clear()
        self.modelStoreBias.clear()
        self.modelStoreSSE_MSE.clear()

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
        self.statusFile.pop(self.novoContexto)
        c = self.statusFile.get_context_id(self.dir_context_path[0])
        self.statusFile.push(c, self.dir_context_path[0])



    '''
    Descrição:
    Esse método abre uma janela de diálogo padrão do Gtk+ a fim de criar e
    armazenar um arquivo .net. Esse arquivo contém dados relacionados à RNA
    criada.
    Utilização: o evento apenas será gerado se houver uma RNA criada.
    '''
    def salvar(self, widget):
        try:
            self.dialog = Gtk.FileChooserDialog("Selecione o local e informe o nome do arquivo",
                                     None,
                                     Gtk.FileChooserAction.SAVE,
                                    (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                     Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            response = self.dialog.run()
            if response == Gtk.ResponseType.OK:
                nome = self.dialog.get_filename()+".net"
                self.net.save(nome)
                thread.start_new_thread(self._statusDinamico,(self.dir_context[16],))
                #altera status para nome do arquivo
                self.statusFile.pop(self.novoContexto)
                self._statusPathFile(str(self.dialog.get_filename()))


            self.dialog.destroy()

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

                self._setListPesosBias()
                self.storeRA.append([str(self.net.trainf)])

                #altera status para nome do arquivo
                self.statusFile.pop(self.novoContexto)
                self._statusPathFile(str(dialog.get_filename()))

                self._desativarFases()

                thread.start_new_thread(self._statusDinamico,(self.dir_context[17],))
                self.butOpenSimulador.set_sensitive(True)



        except:
            self._fontColor("red")
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
            intervalo = [[-10, 10] for i in xrange(len(self.inputs[0]))]

            #validar rede - nao pode ter saida > 1
            s =  self.listaNeuronios.get_text().split(',')
            if s[-1] == '1':
                #criar a rede neural artificial
                rede = rna.Rede(intervalo, self.linear.get_active(),
                                        self.heaviside.get_active(),
                                        self.tangente.get_active(),
                                        self.sigmoide.get_active(),
                                                self.listaNeuronios)
                self.net = rede.criarRede()


                self._setListPesosBias()

                #ativar fase do treinamento
                self.butTreinar.set_sensitive(True)
                self.butGraficoTreinar.set_sensitive(True)
                if self.epocas.get_value_as_int() <= 100:
                    self.switchAnimacao.set_sensitive(True)
                else:
                    self.switchAnimacao.set_sensitive(False)

                #status
                thread.start_new_thread(self._statusDinamico,(self.dir_context[9],))

                thread.start_new_thread(self.desenharArquitetura, (widget,))
            else:
                self._fontColor("red")
                thread.start_new_thread(self._statusDinamico,(self.dir_context[15],))

        except:
            self._fontColor("red")
            thread.start_new_thread(self._statusDinamico,(self.dir_context[6],))
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            #print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)

    def carregarSpinner(self):
        contexto = self.status.get_context_id(self.dir_context[11])
        self.status.push(contexto, self.dir_context[11])
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
            self._setListPesosBias()


            self.butSaveFast.set_sensitive(True)
            self.menuSaveAs.set_sensitive(True)
            self.butSimular.set_sensitive(True)
            self.butOpenSimulador.set_sensitive(True)
            self.butGraficoSimulador.set_sensitive(True)

            self.status.pop(self.status.get_context_id(self.dir_context[11]))


            if len(self.errors) < self.epocas.get_value_as_int():
                thread.start_new_thread(self._statusDinamico,(self.dir_context[1],))
            else:
                thread.start_new_thread(self._statusDinamico,(self.dir_context[2],))

            if self.switchAnimacao.get_active() and self.switchAnimacao.get_sensitive():
                self._animarErro()


        except:
            self._fontColor("red")
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

                self.inputs = novaf

                #converter para matriz por causa do RNA
                self.targets = [[self.targets[i]]
                                        for i in xrange(len(self.targets))]

                self._setStoreDados(self.targets)

                self.butCriarRNA.set_sensitive(True)

                thread.start_new_thread(self._statusDinamico,
                                                (self.dir_context[12],))

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
            self._fontColor("red")
            thread.start_new_thread(self._statusDinamico,
                                            (self.dir_context[13],))
            trace = traceback.format_exc()
            file("trace.log","a").write(trace)
            return None


    def tratarDadosSimulacao(self, widget):
        try:
            caminho = self.butOpenSimulador.get_filename()
            novaf = self.extrair_dados(caminho)

            if novaf and self.net.ci == len(novaf[0]):
                self.inputSimulador = novaf
                self.butSimular.set_sensitive(True)
            else:
                self._fontColor("red")
                thread.start_new_thread(self._statusDinamico,
                                                (self.dir_context[14],))
        except:
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            print "Ocorreu um erro: \n",trace
            #salva em arquivo
            file("trace.log","a").write(trace)


    def _setStoreDados(self, targets ):
        targets = [float(targets[i][j])
                        for i in xrange(len(targets)) for j in xrange(1)]

        #incluir storeDados da entrada e alvo
        for i in xrange(len(targets)):
            self.storeDados.append((str(self.inputs[i]),
                                        float(targets[i])) )


    '''
    Descrição:
    Método privado para configurar e inserir os dados na tela.
    '''
    def _setListPesosBias(self):
        pesos = self.net.layers[0].np['w']
        pesos = [[str(pesos[i][j])] for i in xrange(len(pesos))
                                        for j in xrange(len(pesos[0]))]
        for i in xrange(len(pesos)):
            self.storePesos.append(pesos[i])


        bias = self.net.layers[0].np['b']
        bias = [[str(bias[i])] for i in xrange(len(bias))]
        for i in range(len(bias)):
            self.storeBias.append(bias[i])


    def _setListSim(self, entradas, target):#tabela da simulacao
            sse = 0
            for i in xrange(len(self.saidaSimulador)):
                erroQuad = (float(self.saidaSimulador[i]) - target[i])**2
                sse += erroQuad
                self.store.append((str(entradas[i]),
                                    target[i],
                                    float(self.saidaSimulador[i]),
                                    erroQuad,
                                 ))

            #incluir SSE e MSE na saida da simulacao
            mse = sse / len(target)
            self.storeSSE_MSE.append((sse,mse))


    def simular(self, widget):
        try:
            if self.butOpenSimulador.get_filename():
                self.saidaSimulador = self.net.sim(self.inputSimulador)
                numTargets = [0 for i in xrange(len(self.inputSimulador)) ]
                self._setListSim(self.inputSimulador, numTargets)
            else:
                self.saidaSimulador = self.net.sim(self.inputs)
                numTargets = [float(self.targets[i][j])
                        for i in xrange(len(self.targets)) for j in xrange(1)]
                self._setListSim(self.inputs, numTargets)

            #self.feedStatus.gerarStatus(self.feedStatus.contexto_simulacao)
            thread.start_new_thread(self._statusDinamico,(self.dir_context[3],))

        except:
            self._fontColor("red")
            #self.feedStatus.gerarStatus(self.feedStatus.contexto_erroSim)
            thread.start_new_thread(self._statusDinamico,(self.dir_context[8],))
            #pega a excecao gerada
            trace = traceback.format_exc()
            #imprime
            print "Ocorreu um erro: \n",trace
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

        #variaveis da 2 Fase
        self.delta = builder.get_object("radioDelta")
        self.gd = builder.get_object("radioGD")
        self.gdm = builder.get_object("radioGDM")
        self.gdx = builder.get_object("radioGDX")
        self.gda = builder.get_object("radioGDA")
        self.rprop = builder.get_object("radioRPROP")
        self.bfgs = builder.get_object("radioBFGS")

        #variaveis 3 Fase
        self.listaNeuronios = builder.get_object("listaNeurons")
        self.epocas = builder.get_object("spinEpocas")
        self.objetivo = builder.get_object("spinObjetivo")
        self.show = builder.get_object("spinShow")
        self.taxaAprendizado = builder.get_object("spinTaxaAprendizado")
        self.impulso = builder.get_object("spinImpulso")
        self.taxaRegularizacao = builder.get_object("spinRegularizacao")
        self.taxaIncremento = builder.get_object("spinTaxaIncremento")
        self.taxaDecremento = builder.get_object("spinTaxaDecremento")


        #variaveis da 4 Fase
        self.heaviside = builder.get_object("radioHeaviside")
        self.linear = builder.get_object("radioLinear")
        self.tangente = builder.get_object("radioTangente")
        self.sigmoide = builder.get_object("radioSigmoide")


        #variavel da 5 Fase
        self.butCriarRNA = builder.get_object("butCriarRede")

        #variaveis 6 Fase
        self.butTreinar = builder.get_object("butTreinar")
        self.butGraficoTreinar = builder.get_object("butGrafico")
        self.switchAnimacao = builder.get_object("switch1")

        #variaveis 7 Fase
        self.butOpenSimulador = builder.get_object("butOpenSimulador")
        self.butSimular = builder.get_object("butSimular")
        self.butGraficoSimulador = builder.get_object("butGraficoSimulador")

        #liststore
        self.store = builder.get_object("liststore1")
        self.storeErro = builder.get_object("liststore2")
        self.storeDados = builder.get_object("liststore3")
        self.storePesos = builder.get_object("liststore4")
        self.storeBias = builder.get_object("liststore5")
        self.storeRA = builder.get_object("liststore6")
        self.storeSSE_MSE = builder.get_object("liststore7")

        #fases
        self.fase1 = builder.get_object("fase1")
        self.fase2 = builder.get_object("fase2")
        self.fase3 = builder.get_object("fase3")
        self.fase4 = builder.get_object("fase4")
        self.fase5 = builder.get_object("fase5")
        self.fase6 = builder.get_object("fase6")
        self.fase7 = builder.get_object("fase7")

        #textview
        self.modelStore = builder.get_object("treeview1").get_model()
        self.modelStoreErro = builder.get_object("treeview2").get_model()
        self.modelStoreDados = builder.get_object("treeview3").get_model()
        self.modelStorePesos = builder.get_object("treeview4").get_model()
        self.modelStoreBias = builder.get_object("treeview5").get_model()
        self.modelStoreRA = builder.get_object("treeview6").get_model()
        self.modelStoreSSE_MSE = builder.get_object("treeview7").get_model()

        #variaveis do toolbar
        self.butSaveFast = builder.get_object("butSaveFast")
        self.menuSaveAs = builder.get_object("menuSaveAs")

        #spinner
        self.spinner = builder.get_object("spinner1")


if __name__ == "__main__":
    Interface()
    Gtk.main()
