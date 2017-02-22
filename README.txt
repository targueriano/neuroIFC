Para instalar em uma distribuição Debian ou derivada (Ubuntu, etc):

	No diretório do pacote .deb:  # dpkg -i neuro-ifc_1.0.16_amd64.deb

	Se ele retornar uma mensagem de erro, comentando sobre dependências, o apt consegue resolver com o seguinte comando:

	# apt-get -f install

	Se tudo correr bem, basta executar 'neuro-ifc' de qualquer lugar do terminal ou procurar o app no menu de aplicações de sua distribuição.
