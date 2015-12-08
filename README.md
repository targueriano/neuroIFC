# neuroIFC
Repositório para guardar o programa neuroIFC
####################################################################################################################################################
O presente trabalho consiste num software livre construído em python e GTK+ com a finalidade de treinar a rede neural artificial (RNA) através de dados inseridos numa planilha de um documento de padrão aberto. Uma vez treinado, permitir à rede a devida classifição dos dados não conhecidos. Essa classificação ocorrerá também a partir da leitura de um documento de padrão Open Document Spreadsheets. O resultado da classificação será  escrito  no próprio arquivo selecionado pelo usuário. Esse programa tem como finalidade auxiliar no aprendizado de RNAs. Ele foi construído com o uso da linguagem de programação Python e da biblioteca gráfica GTK+.

Para atingir a finalidade do programa, os passos necessários são os seguintes, respectivamente: 
1. Selecionar a rede: perceptron ou adaline;
2. Incluir o valor da precisão desejada;
3. Incluir os valores para taxa de aprendizado e número de iterações;
4. Selecionar arquivo (.ods) contendo os seguintes dados: entradas, bias, desejados. Por exemplo: 
5. Clicar no botão treinar para iniciar o aprendizado;
6. Selecionar arquivo (.ods) contendo os seguintes dados: entradas e bias;
7. Por último, clicar no botão classificar para realizar a classificação dos dados presentes no arquivo. 

##############################################################Notas Pessoais###########################################################################
A versão 1.0 não trata as exceções e o text_entry do bias não serve para nada, pois o valor do bias deve estar inserido na planilha junto com as entradas e os valores desejados. Esse programa faz parte de um artigo final para uma disciplina de IA-RNA. Espero dar continuidade ao projeto e melhorá-lo nas próximas versões, corrigindo bugs e incluindo novos recursos, por exemplo leitura de arquivos .xlsx. É o meu segundo projeto criado com GTK+ e python, então se as soluções estiverem longe de ser decentes, perdoem minha falta de experiência e falta de conhecimento técnico. 
