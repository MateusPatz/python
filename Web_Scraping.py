#!/bin/python3.5
import http.client
from html.parser import HTMLParser
import re
import time

def testeDominio(site):


	if "https://" in site:
		site=site.replace("https://", "")
		
		conexao = http.client.HTTPSConnection(site, timeout=15)
		conexao.request("GET", "/")
		conteudo = conexao.getresponse()
		if conteudo.status == 200:
			return conteudo.read()
		#else:
			#print(conteudo.status)
		#	print("")
		conexao.close()

	elif "http://" in site:
		site=site.replace("http://", "")
		conexao = http.client.HTTPConnection(site, timeout=15)
		conexao.request("GET", "/")
		conteudo = conexao.getresponse()
		if conteudo.status == 200:
			return conteudo.read()
		#else:
			#print(conteudo.status)
		#	print("")
		conexao.close()

	else:
		conexao = http.client.HTTPConnection(site, timeout=15)
		conexao.request("GET", "/")
		conteudo = conexao.getresponse()
		#print(conteudo.status)
		if conteudo.status == 200:
			#print("HTTP -", site)
			return conteudo.read()

		else:
			conexao.close()
			conexao = http.client.HTTPSConnection(site, timeout=15)
			conexao.request("GET", "/")
			conteudo = conexao.getresponse()
			if conteudo.status == 200:
				#print("HTTPS -", site)
				return conteudo.read()

			else:
				#print("Voce pode tentar:")
				#print(conteudo.msg)
				#print(conteudo.status)
				#print("Tente colocar o mesmo site com/sem 'www.'")
				return False

def funHTML_inicial(site):

	if re.match(r"(https://www\.|http://www\.|www\.)+.*", site):
		html = testeDominio(site)
		if html == False or html == None:
			site = re.sub(r"(https://www\.|http://www\.|www\.)+", "", site)
			#print("tentando sem www - ", site)
			html = testeDominio(site)

	else:
		html = testeDominio(site)
		if html == False or html == None:
			site = "www."+site
			#print("Tentando com WWW - ",site)
			html = testeDominio(site)
	return html

def funLimpaDominio(site):
	siteRaiz = site
	siteLimpo= siteRaiz
	#filtro site
	if re.match(r"(https://www\.|http://www\.|https://|http://)+.*", siteRaiz):
		siteLimpo = re.sub(r"(https://www\.|http://www\.|https://|http://)+", "", siteRaiz)
		if re.match(r".*\..*\/", siteLimpo):
			siteLimpo = re.sub(r"\/.*", "", siteLimpo)
	#print(siteRaiz)
	#print(siteLimpo)
	return siteLimpo

def funFiltroHtml(html):
	class MyHTMLParser(HTMLParser):
		#Criamos um grupo para adicionar links filtrados
		def __init__(self):
			HTMLParser.__init__(self)
			self.valores=[]

		def handle_starttag(self, tag, attrs):
			#Filtro de Html seguindo padrão da Documentação Oficial com algumas alterações
			if tag == "a":
				for name, value in attrs:
					#pegar o conteudo do href quando não for vazio ou "#"
					if name == "href" and (value != "" and value != "#" and not value.endswith(".pdf") and not value.endswith(".png")):
						self.valores.append(value)

	#Criamos um objeto HTMLParser
	filtro = MyHTMLParser()

#	filtro.feed(html.decode("utf-8"))
	#try:
	filtro.feed(html)
	#except TypeError:
	#	pass
	listaLink = filtro.valores
	#print(listaLink)
	#for i in range(len(listaLink)):
		#print(i,"-", listaLink[i])
		#print("")
	return(listaLink)

def conexaoLinks(link, siteInicial, siteLimpo):


	if "https://" in link:
#		link=link.replace("https://", "")
		link = re.sub(r".*%s"%siteLimpo, "", link)
		conexao = http.client.HTTPSConnection(siteInicial, timeout=15)
		conexao.request("GET", link)
		conteudo = conexao.getresponse()
		if conteudo.status == 200:
			return conteudo.read()
		#else:
			#print(conteudo.status)
		#	print("")
		conexao.close()

	elif "http://" in site:
#		link=link.replace("http://", "")
		link = re.sub(r".*%s"%siteLimpo, "", link)
		conexao = http.client.HTTPConnection(siteInicial, timeout=15)
		conexao.request("GET", link)
		conteudo = conexao.getresponse()
		if conteudo.status == 200:
			return conteudo.read()
		#else:
			#print(conteudo.status)
		#	print("")
		conexao.close()

	else:
		link = re.sub(r".*%s"%siteLimpo, "", link)
		conexao = http.client.HTTPConnection(siteInicial, timeout=15)
		conexao.request("GET", link)
		conteudo = conexao.getresponse()
		#print(conteudo.status)
		if conteudo.status == 200:
			#print("HTTP -", siteInicial)
			return conteudo.read()

		else:
			conexao.close()
			link = re.sub(r".*%s"%siteLimpo, "", link)
			conexao = http.client.HTTPSConnection(siteInicial, timeout=15)
			conexao.request("GET", link)
			conteudo = conexao.getresponse()
			if conteudo.status == 200:
				#print("HTTPS -", siteInicial)
				return conteudo.read()

			else:
				#print("Voce pode tentar:")
				#print(conteudo.msg)
				#print(conteudo.status)
				#print("Tente colocar o mesmo site com/sem 'www.'")
				return False


def funLimpaLink(siteLimpo, listaExemplo):
	listaLimpa=[]
	#limpeza da lista de links
	filtroSubDominioWWW = r".*(www\.)+.*(\."+re.escape(siteLimpo)+")+.*"
	#print(filtroSubDominioWWW)
	filtroSubDominioSemWWW = r".*(\."+re.escape(siteLimpo)+")+.*"
	#print(filtroSubDominioSemWWW)
	for i in listaExemplo:
		if siteLimpo in i:
			if "www" in i:
				#se o valor em i não estiver nao ser encontrado pelo filtro etão podemos adicionar na lista
				if re.match(filtroSubDominioWWW, i) == None:
					#print("pode", i)
					listaLimpa.append(i)
				#else:
					#print("nao pode", i)
				#	print("")
			else:
				if re.match(filtroSubDominioSemWWW, i) == None:
					#print("pode", i)#print())
					listaLimpa.append(i)
				#else:
					#print("nao pode", i)
				#	print("")
		else:	
			#print("invalido")
			if "http" in i or "www" in i:
				pass
				#print("NAO PODE", i)
			#	print("")
			else:
				if re.match(r"\/?[\w\-\#\&]+\.?[a-z]?\/?", i):
					#print("Pode SIM", i)
					listaLimpa.append(i)
				else:
					pass
					#print("NAO PODE", i)
					#print("")
	
	return listaLimpa

def conexaoLinks(link, siteInicial, siteLimpo):

	caminho = re.sub(r".*%s"%siteLimpo, "", link)
	#print(a)
	conexao = http.client.HTTPConnection(siteInicial)#, )#timeout=15)
	conexao.request("GET", caminho)
	conteudo = conexao.getresponse()
	#print(conteudo.status)
	if conteudo.status == 200:
		#print("HTTP -", siteLimpo)
		return conteudo.read()

	else:
		conexao.close()
		conexao = http.client.HTTPSConnection(siteInicial)#, )#timeout=15)
		conexao.request("GET", caminho)
		conteudo = conexao.getresponse()
		if conteudo.status == 200:
			#print("HTTPS -", siteLimpo)
			return conteudo.read()

		else:
			print("Nõ")

def filtroEmail(html):
	emails = re.findall(r'[a-z0-9"\_]+[\-_\.\+]*[\_a-z0-9"]+\@[a-z0-9"\[]+[a-zA-Z0-9\_\[\.\-]*\.[a-z0-9A-Z\]]+', html)

#	for i in emails:
		#print(i)

	return emails

def filtroNumeros(html):
	numerosSujo = re.findall(r"[\+\(]?\d+[\(\d\)\ \-\.]*[\d]+", html)

	numerosLimpo = []

	for i in numerosSujo:
		teste = re.sub(r"[\+\ \-\(\)]", "", i)
		if not (len(str(teste)) > 13 or len(str(teste)) < 8):
			if re.search(r"[\(|\)]+", i) != None:
				numerosLimpo.append(i)

#	for i in numerosLimpo:
		#print(i)
	return numerosLimpo

siteInicial = input("Digite o site que deseja \"varrer\":")

siteLimpo = funLimpaDominio(siteInicial)

htmlInicial = funHTML_inicial(siteInicial)
htmlInicial = htmlInicial.decode("utf-8")

lista_links = []
arquivo = open("lista_links", "w")
arquivo2 = open("lista_emails", "w")
arquivo3 = open("lista_numeros", "w")

lista_emails = []

lista_numeros = []

if htmlInicial != False:
	#primeiros links
	lista_links = funFiltroHtml(htmlInicial)
	lista_links = list(set(lista_links))
	lista_links = funLimpaLink(siteLimpo, lista_links)
	#print(lista_links)

	lista_emails = filtroEmail(htmlInicial)#.decode("utf-8"))

	lista_numeros = filtroNumeros(htmlInicial)#.decode("utf-8"))

	lista_links = list(set(lista_links).difference(lista_emails))
	lista_links = list(set(lista_links).difference(lista_numeros))
	#print(len(lista_links))
	#print(lista_links)
	tamanhoLista = len(lista_links)
	i = 0
	while i < tamanhoLista:
		#a = a +1
		print(lista_links[i])
#		if lista_links[i].endswith("pdf"):
		
		html = conexaoLinks(lista_links[i],siteInicial,siteLimpo)
		if html:# != False or html != None:# or not html == None:
			#print(html, "aaaaaaaa")
			#print(len(lista_links))
			try:
				html = html.decode("utf-8")
				b = True
			
			except UnicodeDecodeError:
				print("Formatação invalida")
				b = False
				pass
			
			if b:
				listaTemporariaLinks = funFiltroHtml(html)
				listaTemporariaLinks = list(set(listaTemporariaLinks))
				listaTemporariaLinks = funLimpaLink(siteLimpo, listaTemporariaLinks)

				listaTemporariaEmails = filtroEmail(html)#.decode("utf-8"))
				listaTemporariaNumeros = filtroNumeros(html)#.decode("utf-8"))

				listaTemporariaLinks = list(set(listaTemporariaLinks).difference(listaTemporariaEmails))
				listaTemporariaLinks = list(set(listaTemporariaLinks).difference(listaTemporariaNumeros))
				listaTemporariaLinks = list(set(listaTemporariaLinks).difference(lista_links))

				listaTemporariaEmails = list(set(listaTemporariaEmails).difference(lista_emails))

				listaTemporariaNumeros = list(set(listaTemporariaNumeros).difference(lista_numeros))

				lista_links = lista_links + listaTemporariaLinks
				lista_emails = lista_emails + listaTemporariaEmails
				lista_numeros = lista_numeros + listaTemporariaNumeros
				#time.sleep(15)
				tamanhoLista = len(lista_links)
				for a in listaTemporariaLinks:
					arquivo.write(a)
					arquivo.write("\n")
				arquivo.flush()

				for b in listaTemporariaEmails:
					arquivo2.write(b)
					arquivo2.write("\n")
				arquivo2.flush()

				for c in listaTemporariaNumeros:
					arquivo3.write(c)
					arquivo3.write("\n")
				arquivo3.flush()

		i = i + 1
	print(len(lista_links))
	print(len(lista_emails))
	print(lista_emails)
	print(len(lista_numeros))

	
	arquivo.close()

	arquivo2.close()

	arquivo3.close()	

else:
	print("site invalido")

#lista_link.append(siteInicial)

#print(html)


