#!/bin/python3.5
import os

tipo=int(input("Digite 1 para Ceasar\nDigite 2 para viginere\n"))
nomeArquivo=input("Digite o nome do arquivo:")
if tipo == 1:
	if os.path.isfile(nomeArquivo):
		#abrir arquivo e ler palavra
		arquivo = open(nomeArquivo, encoding="utf8")
		palavraCifrada = arquivo.readline().strip()
		arquivo.close()

		#deixar todos os itens da palavra misuculos e retira todos os espaços em branco
		palavraCifrada = palavraCifrada.lower()
		palavraCifrada = palavraCifrada.replace(" ","")

		if palavraCifrada:

			#inicio um array com palavras que serão criadas no brute force.
			#a primeira palavra do array sera então a palavra lida no arquivo a cima
			grupoPalavras = []
			grupoPalavras.append( [palavraCifrada] )

			#transformar a string em um grupo de letras
			letrasCifradas = list(palavraCifrada)

			#loop que somara as letras no grupo e tentara todas possibilidades
			for i in range(25):
				for j in range(len(letrasCifradas)):
					#se a letra atual for igua a z então ela se torna a
					if ord(letrasCifradas[j]) == 122:
						letrasCifradas[j] = 'a'
					#senão some uma letra e continue o fluxo do loop	
					else:
						letrasCifradas[j] = chr(ord(letrasCifradas[j])+1)

				#adicionamos a palavra alterada no grupo de palavras
				grupoPalavras.append([''.join(letrasCifradas)])

			#escrevemos em um arquivo quebrando a linha a cada palavra do grupo escrita
			arquivo= open(palavraCifrada+"_possibilidades", 'w')
			for k in grupoPalavras:
				#print(''.join(k))	
				arquivo.write(''.join(k))
				arquivo.write("\n")
			arquivo.close()
		
			#agora comparamos os dois arquivos com o objetivos e achamos as palavras iguais
			#SCRIPT GENERICO DE COMPARAÇÂO https://stackoverflow.com/questions/19007383/compare-two-different-files-line-by-line-in-python
			with open(palavraCifrada+"_possibilidades", encoding="utf8") as file1:
				with open('dicionario', encoding="utf8") as file2:
					same = set(file1).intersection(file2)

			same.discard('\n')

			with open('Resultado', 'w') as file_out:
				for line in same:
					file_out.write(line)

			print("#########################################\nResultados salvos no arquivos 'Resultado'\n#########################################")

		else:
			print("arquivo sem conteudo valido")
	else:
		print("Arquivo não existe")

elif tipo == 2:

	if os.path.isfile(nomeArquivo):
		#abrir arquivo e ler palavra
		arquivo = open(nomeArquivo, encoding="utf8")
		palavraCifrada = arquivo.readline().strip()
		arquivo.close()

		#deixar todos os itens da palavra misuculos e retira todos os espaços em branco
		palavraCifrada = palavraCifrada.lower()
		palavraCifrada = palavraCifrada.replace(" ","")

		if palavraCifrada:

			#separamos as palavras em grupoPalavras de 3 mas o script foi feito para se adaptar a qualquer tipo de
 			#tamanho de chave
			grupoPalavras = [palavraCifrada[i:i+3] for i in range(0, len(palavraCifrada), 3)]
			

			#inicia um malha de viginere
			matriz=[]
			lista=[]

			for y in range(26):
				inicial=97+y
				contador=0
				for x in range(26):
					if (contador+inicial) == 123:
						contador = 0
						inicial = 97
						lista.append(chr(inicial+contador))
					else:
						lista.append(chr(inicial+contador))
					contador+=1
				matriz.append(lista)
				#print(matriz[y])#DESCOMENTE ESSA LINHA PARA VER A MALHA
				lista=[]

				#variaveis 'globais'
				resultado=0
				resultado2=[]
				entrou=False
				fim=[]

				#SEGUE ABAIXO ESTA OBRA PRIMA

			#GERA TODAS AS POSSIBILIDADES DOS grupoPalavras QUE FORAM SEPARADOS
			for i in range(len(grupoPalavras)):
				grupoPalavras[i]=list(grupoPalavras[i])
				for j in range(len(grupoPalavras[i])):
					grupoPalavras[i][j]=matriz[ord(grupoPalavras[i][j])-97]
					for h in range(len(grupoPalavras[i][j])):
						grupoPalavras[i][j][h]=list(grupoPalavras[i][j][h])


			#atribui um grupo de ceasar para cada letra
				for k in range(len(grupoPalavras[i])):
					if resultado == 0:
						resultado = grupoPalavras[i][k]
					else:
						for l in range(len(resultado)):
			
							sub=[]
							for j in range(len(grupoPalavras[i][k])):
								palavra=resultado[l]+grupoPalavras[i][k][j]
								sub.append([''.join(palavra)])
							resultado2.extend(sub)
						entrou=True
					if entrou:
						resultado=resultado2
						resultado2=[]

				#juntas todas as possibilidades
				if fim != []:
					cont=0
					cont2=0
					for x in range(len(fim[0])):

						palavra2=fim[0][x][0]+resultado[cont][0]
						palavra2=''.join(palavra2)
						fim[0][x][0] = palavra2
						#print(cont)
						if cont2 == (len(fim[0])/len(resultado)-1):
							cont2 =0
							cont=cont+1
							
						else:
							cont2=cont2+1
				else:
					fim.append(resultado)
				resultado=0
				entrou=False

			#organizamos as variavies resultantes
			fim=fim[0]
			fim2=[]
			for x in fim:
				fim2.append(x[0])
			fim2=sorted(fim2)
			#print(fim)

			#escrevemos em um arquivo quebrando a linha a cada palavra do grupo escrita
			arquivo= open(palavraCifrada+"_possibilidades", 'w')
			for k in fim:
				#print(''.join(k))	
				arquivo.write(''.join(k))
				arquivo.write("\n")
			arquivo.close()

			#agora comparamos os dois arquivos com o objetivos e achamos as palavras iguais
			#SCRIPT GENERICO DE COMPARAÇÂO https://stackoverflow.com/questions/19007383/compare-two-different-files-line-by-line-in-python
			with open(palavraCifrada+"_possibilidades", encoding="utf8") as file1:
				with open('dicionario', encoding="utf8") as file2:
					same = set(file1).intersection(file2)

			same.discard('\n')

			with open('Resultado', 'w') as file_out:
				for line in same:
					file_out.write(line)


			print("#########################################\nResultados salvos no arquivos 'Resultado'\n#########################################")

		else:
			print("arquivo sem conteudo valido")
	else:
		print("Arquivo não existe")
else:
	print("opcao invalida")
