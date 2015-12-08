#!/usr/bin/env python
# -*- coding: utf-8 -*-
#autor Taylan Branco Meurer
#algoritmo para efetuar classificacao apos treino da rede adaline 


#import matplotlib.pyplot as plt
import pylab 
    
#****************************************************************************
# Variaveis globais

#pesos ou sinapses para as entradas e bias
w = [1,1,1,1,1]

plotx = []
ploty = []


#entradas
x2 = [[-0.6508,	0.1097,	4.0009,-1],
     [-1.4492,	0.8896,	4.4005,-1],
     [2.0850,	0.6876,	12.0710,-1],
     [0.2626,	1.1476,	7.7985,-1],
     [0.6418,	1.0234,	7.0427,-1],
	 [0.2569,	0.6730,	8.3265,-1],
     [1.1155,	0.6043,	7.4446,-1],
     [0.0914,	0.3399,	7.0677,-1],
     [0.0121,	0.5256,	4.6316,-1],
     [-0.0429,	0.4660,	5.4323,-1],
     [0.4340,	0.6870,	8.2287,-1],
     [0.2735,	1.0287,	7.1934,-1],
     [0.4839,	0.4851,	7.4850,-1],
     [0.4089,	-0.1267,	5.5019,-1],
     [1.4391,	0.1614,	8.5843,-1],
     [-0.9115,	-0.1973,	2.1962,-1],
     [0.3654,	1.0475,	7.4858,-1],
     [0.2144,	0.7515,	7.1699,-1],
     [0.2013,	1.0014,	6.5489,-1],
     [0.6483,	0.2183,	5.8991,-1],
     [-0.1147,	0.2242,	7.2435,-1],
     [-0.7970,	0.8795,	3.8762,-1],
     [-1.0625,	0.6366,	2.4707,-1],
     [0.5307,	0.1285,	5.6883,-1],
     [-1.2200,	0.7777,	1.7252,-1],
     [0.3957,	0.1076,	5.6623,-1],
     [-0.1013,	0.5989,	7.1812,-1],
     [2.4482,	0.9455,	11.2095,-1],
     [2.0149,	0.6192,	10.9263,-1],
     [0.2012,	0.2611,	5.4631,-1]]
     
#entrada
x =   [[0.4329, -1.3719, 	0.7022, 	-0.8535,  -1], 
            [0.3024, 	0.2286, 	0.8630, 	2.7909,  -1], 
            [0.1349, 	-0.6445, 	1.0530, 	0.5687,  -1], 
            [0.3374, 	-1.7163, 	0.3670, 	-0.6283,  -1], 
            [1.1434, 	-0.0485, 	0.6637, 	1.2606,  -1], 
            [1.3749, 	-0.5071, 	0.4464, 	1.3009,  -1], 
            [0.7221, 	-0.7587, 	0.7681, 	-0.5592,  -1], 
            [0.4403, 	-0.8072, 	0.5154, 	-0.3129,  -1], 
            [-0.5231, 	0.3548, 	0.2538, 	1.5776,  -1], 
            [0.3255, 	-2.0000, 	0.7112	, -1.1209,  -1], 
            [0.5824, 	1.3915, 	-0.2291, 	4.1735,  -1], 
            [0.1340, 	0.6081, 	0.4450, 	3.2230,  -1], 
            [0.1480, 	-0.2988, 	0.4778, 	0.8649,  -1], 
            [0.7359, 	0.1869	, -0.0872, 	2.3584,  -1], 
            [0.7115, 	-1.1469, 	0.3394, 	0.9573,  -1], 
            [0.8251, 	-1.2840, 	0.8452, 	1.2382,  -1], 
            [0.1569, 	0.3712, 	0.8825, 	1.7633,  -1], 
            [0.0033, 	0.6835, 	0.5389, 	2.8249,  -1], 
            [0.4243, 	0.8313, 	0.2634, 	3.5855,  -1], 
            [1.0490, 	0.1326, 	0.9138, 	1.9792,  -1], 
            [1.4276, 	0.5331, 	-0.0145, 	3.7286,  -1], 
            [0.5971, 	1.4865, 	0.2904, 	4.6069,  -1], 
            [0.8475, 	2.1479, 	0.3179, 	5.8235,  -1], 
            [1.3967, 	-0.4171, 	0.6443, 	1.3927,  -1], 
            [0.0044, 	1.5378	, 0.6099, 	4.7755,  -1], 
            [0.2201, 	-0.5668, 	0.0515, 	0.7829,  -1], 
            [0.6300, 	-1.2480, 	0.8591, 	0.8093,  -1], 
            [-0.2479, 	0.8960, 	0.0547, 	1.7381,  -1], 
            [-0.3088, 	-0.0929, 	0.8659, 	1.5483,  -1], 
            [-0.5180, 	1.4974, 	0.5453, 	2.3993,  -1], 
            [0.6833,  0.8266, 	0.0829, 	2.8864,  -1], 
            [0.4353, 	-1.4066, 	0.4207, 	-0.4879,  -1], 
            [-0.1069, 	-3.2329, 	0.1856, 	-2.4572,  -1], 
            [0.4662, 	0.6261, 	0.7304, 	3.4370,  -1], 
            [0.8298, 	-1.4089, 	0.3119, 	1.3235,  -1]]

#respostas esperadas
d = [1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1]

#taxa de aprendizado
taxa_aprendizado = 0

#************************************************************************************
# Funcao para plotar grafico
#************************************************************************************
def plotGrafico():
	# plotx == erro medio quadratico
	# ploty == epocas
	
        pylab.plot(ploty,plotx)
        pylab.ylabel('Erro Quadratico Medio')
        pylab.xlabel('Epoca')
        pylab.title('Adaline')
        pylab.grid(True)
        pylab.show()
            
	pass	
#************************************************************************************

#***********************************************************************************
# Metodo para classificar apos aprendizado
#***********************************************************************************
def classificar(entrada):
		soma = 0
		for i in range(0,len(w)):
			print(entrada[i])
			soma += entrada[i] * w[i]
		
		#funcao de transferencia
		if soma >= 0:
			return 1
		else:
			return -1
#**********************************************************************************
#**********************************************************************************
# Metodo para inserir valores desejados
#***********************************************************************************
def desejados():
	d = []
	for i in range(len(x)):
		aux2 = float(raw_input("d= "))
		d.append(aux2)
	
	return d
#***********************************************************************************


#**********************************************************************************
# Metodo para inserir entradas
#**********************************************************************************	   
def entrada():
	x = []
	tam = int(raw_input("Número de entradas: ")) #colunas	   
	qtd	= int(raw_input("Quantidade de amostras: ")) #linhas
	b = int(raw_input("Bias: "))
	
	for i in range(qtd):
		x.append([])
		for j in range(tam):
			aux = float(raw_input("x= "))
			x[i].append(aux)
		x[i].append(b) 
			
	return x
#***********************************************************************************

#***********************************************************************************
# Mostrar entradas
#***********************************************************************************
def mostrarEntradas():
	print("******************************")
	print("Entradas  >>>>>>>>>   Desejado")
	for i in range(len(x)):
		print("---------------------------------------")
		print(x[i]),
		print("| "),
		print(d[i])
	
	print(len(x))
		
	pass
#********************************************************************************
# Metodo para inserir pesos
#********************************************************************************			
def pesos():
	w = []
	qtdPesos = int(raw_input("Quantidade de pesos: "))
	for i in range(qtdPesos):
		p = float(raw_input("w= "))
		w.append(p)
	return w
#*********************************************************************************

def funcao_ativacao(x, w,  linha):        
    u = 0
    for j in range(0, len(w[linha])):
        u += x[linha][j] * w[j]
    
    if u >= 0:
        return 1
    else:
        return (-1)
    
#Fim da funcao de ativacao ***********************************************************
#***************************************************************************************************
# funcao do erro quadratico medio
#****************************************************************************************************
def erro_eqm(w):
    erro = 0
    for i in range(0, len(x)):
        u = 0
        for j in range(0,len(x[i]) ):
            u += x[i][j]*w[j]
            
        erro += (d[i] - u)**2 
    
    
    erro = erro/len(x)
    return erro
#***************************************************************************************************
#*******************************************************************************************************
# Funcao para treinar uma rede adaline 
#****************************************************************************************************
def treinar(x,w, max_it, d, taxa_aprendizado):
            precisao = float(raw_input("precisao: "))
            epoca = 1
            w_old = list(w)
            erro_ant = precisao*2
            erro_atual = 1
            
            while (abs(erro_atual - erro_ant) > precisao and max_it > epoca ):
                erro_ant = erro_eqm(w)
           
                print("Epoca "+str(epoca)+"----------------------------------")
                for i in range(0,len(x)): #todas as amostras
                    soma = 0
                    # para calcular a saida do perceptron, cada entrada de x eh multiplicada
                    # pelo seu peso w correspondente
                    #funcao de ativacao
                    for j in range(0,len(x[i])):
                        soma += x[i][j] * w[j]
                    if soma >= 0:
                        y = 1
                    else:
                        y = -1
                    for j in range(0,len(w)):
                        w[j] = w[j] + (taxa_aprendizado * (d[i] - y) * x[i][j] )
                    
                #endfor-----------------------------------------------------------        
                epoca += 1
                erro_atual = erro_eqm(w)
				
				#adicionar dados para variaveis de grafico
                plotx.append(erro_atual)
                ploty.append(epoca)
				
                print("Erro anterior >>>>> "),
                print(erro_ant)
                print("Erro atual >>>>> "),
                print(erro_atual)
                print("Diferença >>>>> "), 
                print(abs(erro_atual-erro_ant))
                
                
                
            #fim do while
            print("#######################################################")
            print("Épocas >>>>> "), 
            print(epoca-1)
            print("Precisão >>>>> "),
            print(precisao)
            print("Peso Inicial >>>>> "), 
            print(w_old)
            print("Peso atual >>>>> "), 
            print(w)
            print("Taxa de aprendizado >>>>> "), 
            print(taxa_aprendizado)
            plotGrafico()
    #*********************************************************************************

#*********************************************************************************
# programa principal - Menu
#********************************************************************************	
chave = True
while chave:
	print("################ADALINE#####################")
	print("--------------------------------------------")
	print("1 - Inserir entradas")
	print("2 - Inserir pesos")
	print("3 - Inserir valores desejados")
	print("4 - Treinar rede")
	print("5 - Classificar")
	print("6 - Mostrar pesos")
	print("7 - Mostrar entradas")
	print("8 - Sair")
	choice = int(raw_input(">>>> "))
	
	if choice == 1:
		x = entrada()
	elif choice == 2:
		w = pesos()
	elif choice == 3:
		d = desejados()
	elif choice == 4:
		max_it = int(raw_input("Quantidade máxima de iterações: "))
		taxa_aprendizado = float(raw_input("Taxa de aprendizado: "))
		treinar(x,w, max_it, d, taxa_aprendizado)
	elif choice == 5:
		num_x = raw_input("Informe a quantidade de entradas >>>>>> ")
		novo = []
		print("<<<<< Informe as novas entradas, incluindo bias >>>>>")
		for i in range(0,int(num_x)):
			a = float(raw_input("x= ")) 	
			novo.append(a)
		y = classificar(novo)
		#imprime resposta
		if y == 1:
			print("Válvula B")
		else:
			print("Válvula A")
		
	elif choice == 6:
		print("*****PESOS*******")
		print(w)
			
	elif choice == 7:
		mostrarEntradas()
	elif choice == 8:
		chave = False
	
#END####################################################################



    
    
    
    
