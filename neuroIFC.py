#!/usr/bin/env python
# -*- coding: utf-8 -*-
# autor Taylan Branco Meurer
# algoritmo para executar neuroIFC


from gi.repository import Gtk
# from ODSReader import *
from pyexcel_ods import get_data
from pyexcel_ods import save_data
import json
import random
import pylab
from collections import OrderedDict


class NeuroIFC(object):
    # construtor
    def __init__(self):
        gladefil = "neuroIFC.glade"
        builder = Gtk.Builder()
        builder.add_from_file(gladefil)
        self.win = builder.get_object("window1")
        self.about = builder.get_object("aboutdialog1")
        self.selectEntradas = builder.get_object("fileEntradas")
        self.select_testes = builder.get_object("fileTestes")
        self.precisao = builder.get_object("textErro")
        self.max_it = builder.get_object("textIteracoes")
        self.taxa = builder.get_object("textTaxa")
        self.epocas = builder.get_object("textEpocas")
        self.peso_inicial = builder.get_object("textPesosIniciais")
        self.peso_final = builder.get_object("textPesosFinais")
        self.radio_ada = builder.get_object("radioAdaline")
        self.radio_percep = builder.get_object("radioPerceptron")
        self.status = builder.get_object("statusbar1")
        #variaveis para a rede neural
        self.x = []
        self.w = []
        self.d = []
       
        self.win.show()
        builder.connect_signals({"gtk_main_quit":Gtk.main_quit,
                                 "on_butTreinar_clicked":self.treinamento,
                                 "on_fileEntradas_file_set":self.dadosEntradas,
                                 "on_butClassificar_clicked":self.classifica,
                                 "on_fileTestes_file_set":self.dadosTestes,
                                 "on_sair_activate": Gtk.main_quit,
                                 "on_saveAs_activate":self.save,
                                 "on_about_dialog_activate":self.aboutWindow,
                                 "on_statusbar1_text_popped":Gtk.Statusbar})
        
        
    
    
    def treinamento(self, widget):
        x = self.x
        w = self.w
        max_it = self.max_it.get_text()
        max_it = int(max_it)

        d = self.d

        taxa_aprendizado = self.taxa.get_text()
        taxa_aprendizado = float(taxa_aprendizado)
   
        precisao = self.precisao.get_text()
        precisao = float(precisao)
        #antes verifica qual radio esta selecionado
        if self.radio_percep.get_active():
            percetron = Perceptron()
            epo_ini_fim = percetron.treinar(x, w, max_it, d, taxa_aprendizado)
            if epo_ini_fim[0] == -1:
                epo_ini_fim = ["Non","Non", "Non"]
                print "Nao foi possivel aprender!"
            
                
        else:
            adaline = Adaline()
            epo_ini_fim = adaline.treinar(x, w, max_it, d, taxa_aprendizado,precisao)
        
        self.epocas.set_text(str(epo_ini_fim[0]))
        self.peso_inicial.set_text(str(epo_ini_fim[1]))
        self.peso_final.set_text(str(epo_ini_fim[2]))

    def dadosEntradas(self, widget):
        caminho = self.selectEntradas.get_filename()
        
        
        novaf = self.extrair_dados(caminho)
        tam = len(novaf[0])-1
        self.w = [i*random.randint(0,9) for i in range(1,tam+1)]
        
        for i in range(len(novaf)):
            self.d.append(novaf[i][-1])
            novaf[i].remove(novaf[i][-1])
        
        self.x = novaf
        
    def extrair_dados(self, caminho):
        data = get_data(caminho)
        chave = False
        lista = json.dumps(data)
        
        for i in range(len(lista)):
            if lista[i] == '[' and chave == False:
                inicio = i+1
                chave = True
            if lista[i] == '}':
                fim = i-1
                
        lista =  lista[inicio:fim]
        #print lista
        
        nova = []
        #new_lista = [float(i) for i in lista]
        chave1 = False
        chave2 = False
        for x in range(len(lista)):
            if lista[x] == '[':
                inicio = x
                chave1 = True
            if lista[x] == ']':
                fim = x
                chave2 = True
                
            if chave1 and chave2:
                lis = lista[inicio+1:fim]
                for i in range(len(lis)):
                    if lis[i] == ',':
                        list = lis.replace(lis[i],'')
                
                nova.append(list)
                chave1 = False
                chave2= False
        
               
        novaf = []
        for i in range(len(nova)):
            g = "".join(nova[i])#de lista para string
            g = g.split() #de string para lista 
            f = [float(a) for a in g] #listcomp para converter string em float
            novaf.append(f)#gera a nova lista aninhada em float
        
        #preciso dos pesos iniciais
        return novaf
    
        
    def dadosTestes(self,widget):
        caminho = self.select_testes.get_filename()
        novaf = self.extrair_dados(caminho)
        self.x = novaf
        
        
    
    
    def classifica(self,widget):
        caminho = self.select_testes.get_filename()
        data = OrderedDict()
        adaline = Adaline()
        w = self.w
        x = self.x
        lista = adaline.classificar(w, x)
        
        data.update({"Sheet 1": lista})
        save_data(caminho, data)
    
        
    
    def save(self, widget):
        pass
    
    def aboutWindow(self,widget):
        self.about.run()
        self.about.hide()
    
    
    

class Adaline(object):
    global plotx 
    global ploty 
    
    
    def treinar(self, x, w, max_it, d, taxa_aprendizado, precisao):
            plotx = []
            ploty = []
            epoca = 1
            w_old = list(w)
            erro_ant = precisao * 2
            erro_atual = 1
            
            while (abs(erro_atual - erro_ant) > precisao and max_it > epoca):
                erro_ant = self.erro_eqm(w, x, d)
           
                print("Epoca " + str(epoca) + "----------------------------------")
                for i in range(0, len(x)):  # todas as amostras
                    soma = 0
                    # para calcular a saida do perceptron, cada entrada de x eh multiplicada
                    # pelo seu peso w correspondente
                    # funcao de ativacao
                    for j in range(0, len(x[i])):
                        soma += x[i][j] * w[j]
                    if soma >= 0:
                        y = 1
                    else:
                        y = -1
                    for j in range(0, len(w)):
                        w[j] = w[j] + (taxa_aprendizado * (d[i] - y) * x[i][j])
                    
                #endfor-----------------------------------------------------------        
                epoca += 1
                erro_atual = self.erro_eqm(w, x, d)
                
                # adicionar dados para variaveis de grafico
                plotx.append(erro_atual)
                ploty.append(epoca)
                
                print("Erro anterior >>>>> "),
                print(erro_ant)
                print("Erro atual >>>>> "),
                print(erro_atual)
                print("Diferença >>>>> "),
                print(abs(erro_atual - erro_ant))
                
                
                
            # fim do while
            print("#######################################################")
            print("Épocas >>>>> "),
            print(epoca - 1)
            print("Precisão >>>>> "),
            print(precisao)
            print("Peso Inicial >>>>> "),
            print(w_old)
            print("Peso atual >>>>> "),
            print(w)
            print("Taxa de aprendizado >>>>> "),
            print(taxa_aprendizado)
            self.plotGrafico(plotx,ploty)
            
            
            epo_ini_fim = [epoca-1, w_old, w]
            return epo_ini_fim 
    #*********************************************************************************
    
    #***************************************************************************************************
    # funcao do erro quadratico medio
    #****************************************************************************************************    
    def erro_eqm(self,w, x, d):
        erro = 0
        
        for i in range(0, len(x)):
            u = 0
            for j in range(0, len(x[i])):
                u += x[i][j] * w[j]
            
            erro += (d[i] - u) ** 2 
    
    
        erro = erro / len(x)
        return erro
    #***************************************************************************************************

    
    #************************************************************************************
    # Funcao para plotar grafico
    #************************************************************************************
    def plotGrafico(self, plotx, ploty):
        
        # plotx == erro medio quadratico
        # ploty == epocas
        pylab.plot(ploty, plotx)
        pylab.ylabel('Erro Quadratico Medio')
        pylab.xlabel('Epoca')
        pylab.title('Adaline')
        pylab.grid(True)
        pylab.show()
    #************************************************************************************

    def classificar(self, w, x):
        soma = 0.0
        lista = []
        aux = []
        print x
        print w
        
        for i in range(len(x)):
            for j in range(len(w)):
                soma += x[i][j] * w[j]
                aux.append(x[i][j])
                
            if soma >= 0:
                aux.append(1)
            else:
                aux.append(-1)
            lista.append(aux)
            aux = []
            
        return lista
        
        

    

class Perceptron(object):
    global plotx
    global ploty
    #*********************************************************************************
    # Metodo para treinar rede neural artificial perceptron simples
    #*********************************************************************************
    def treinar(self,x,w, max_it, d, taxa_aprendizado):
        #inicio do algoritmo
        w_old = list(w)
        for k in range(1,max_it):
            acertos = 0
            
            for i in range(0,len(x)):
                soma = 0
                # para calcular a saida do perceptron, cada entrada de x eh multiplicada
                # pelo seu peso w correspondente
                #funcao de ativacao
                for j in range(0,len(x[i])):
                    soma += x[i][j] * w[j]
                
                #funcao de transferencia
                if soma >= 0:
                    y = 1
                else:
                    y = -1
                
                #atualiza os pesos caso a saida nao seja a desejada
                if y == d[i]:
                    #qdo acertos for igual ao numero de amostras, o loop para
                    acertos+=1
                else:
                    for j in range(0,len(w)):
                        w[j] = w[j] + (taxa_aprendizado * (d[i]-y) * x[i][j] )
                    #bias = bias + taxa_aprendizado * d[i]
                    
                
            #condicao para termino do treinamento
            if acertos == len(x):
                print("Funcionalidade aprendida com "+str(k)+" épocas\n")
                ep_wi_wf = [k,w_old, w]
                return ep_wi_wf
                
        return [-1,-1,-1]
        
    
    #*********************************************************************************

    
    
if __name__ == "__main__":
    app = NeuroIFC()
    Gtk.main()
    
    
