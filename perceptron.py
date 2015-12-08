#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#autor Taylan Branco Meurer
#algoritmo para efetuar classificacao apos treino da rede perceptron simples



#****************************************************************************
# Variaveis globais

#pesos ou sinapses para as entradas e bias
w = [1,1,1,1]

#entradas
x = [[-0.6508,	0.1097,	4.0009,-1],
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
#respostas esperadas
d = [-1.0000,-1.0000,-1.0000,1.0000,1.0000,-1.0000,1.0000,-1.0000,1.0000,1.0000,-1.0000,1.0000,-1.0000,-1.0000,-1.0000,-1.0000,1.0000,
		1.0000,1.0000,1.0000,-1.0000,1.0000,1.0000,1.0000,1.0000,-1.0000,-1.0000,1.0000,-1.0000,1.0000]


#max de iteracoes
max_it = 0

#taxa de aprendizado
taxa_aprendizado = 0



#****************************************************************************


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

#*********************************************************************************
# Metodo para treinar rede neural artificial perceptron simples
#*********************************************************************************
def treinar(x,w, max_it, d, taxa_aprendizado):
	#inicio do algoritmo
	for k in range(1,max_it):
	    acertos = 0
	    print("Epoca "+str(k)+"----------------------------------")
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
				
		    #imprime resposta
		    if y == 1:
				print("Classe P2")
		    else:
				print("Classe P1")
			
	    #condicao para termino do treinamento
	    if acertos == len(x):
			print("Funcionalidade aprendida com "+str(k)+" épocas\n")
			return w
			
	return -1
	
	
#*********************************************************************************
	
#*********************************************************************************
# programa principal - Menu
#********************************************************************************	
chave = True
while chave:
	print("################PERCEPTRON DE UMA CAMADA#####################")
	print("-------------------------------------------------------------")
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
		pesoVelho = list(w)
		saida = treinar(x,w, max_it, d, taxa_aprendizado)
		if saida == -1:
			print("Não foi capaz de aprender")
		else:
			print("Aprendizado realizado com sucesso!")
		
		print("-------------------------------------------------------------------------------------------------")
		print("Pesos iniciais >>>>>>> "),
		print(pesoVelho)
		print("-------------------------------------------------------------------------------------------------")
		print("Pesos finais >>>>>>> "),
		print(w)
		print("-------------------------------------------------------------------------------------------------")
		print("Taxa de aprendizado >>>>>>> "),
		print(taxa_aprendizado)
		print("")
		
	elif choice == 5:
		novo = []
		print("<<<<< Informe as novas entradas, incluindo bias >>>>>")
		for i in range(0,4):
			a = float(raw_input("x= ")) 	
			novo.append(a) 
		y = classificar(novo)
		#imprime resposta
		if y == 1:
			print("Classe P2")
		else:
			print("Classe P1")
		
	elif choice == 6:
		print("*****PESOS*******")
		print(w)
			
	elif choice == 7:
		mostrarEntradas()
	elif choice == 8:
		chave = False
	
#END####################################################################


	
