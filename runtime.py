# Beatriz Vadillo Cortes
# MUIT - Computacion en Red: Practica 1

import urllib, re, json, ssl, numpy
import time as t 
import threading as thr 
from pymongo import * 
from beebotte import *

gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
# Conexion con servidores de Beebotte
bclient = BBT("XWwwkSrM4bmcjd0E87Q7DIUW", "sBcJaNY4DRBhmzHyLy3CSTTX6LF1nzj8")
mclient = MongoClient('localhost',27017)
# Acceso a la base de datos de MongoDB
db = mclient.noticias_db
# Acceso a la coleccion de MongoDB
results = db.results

# Se llama a la funcion que arranca el timer
def bucle():
	database()

# Funcion que extrae los datos de la web
def check():
	# Fecha y hora actual
	wdate = t.strftime("%y/%m/%d - %X")
	# Web que se quiere analizar
	wtexto = urllib.urlopen('https://www.meneame.net', context = gcontext).read()
	# Titular, meneos y clics de la primera noticia
	wtitular = re.search('<a\s*href=".*?"\s*class="l:\d*"\s*>(.*?)<\/a>',wtexto).group(1)
	wmeneos = int(re.search('(\d+)<\/a>\s*meneos',wtexto).group(1))
	wclics = int(re.search('(\d+)\s*clics',wtexto).group(1))
	return wtitular, wmeneos, wclics, wdate

# Funcion que almacena los valores en las bases de datos
def database():
	# Obtener datos de la web
	[wtitular, wmeneos, wclics, wdate] = check()
	# Se guardan los datos en un diccionario
	dic_noticia = {'Titular': wtitular, 'Meneos': wmeneos, 'Clics': wclics, 'Fecha': wdate}

	# Base de datos Beebotte	
	bclient.write("compu", "Titulo", wtitular)
	bclient.write("compu", "Meneos", wmeneos)
	bclient.write("compu", "Clics", wclics)
	bclient.write("compu", "Date", wdate)
	
	# Base de datos MongoDB
	resultado = results.insert_one(dic_noticia)	
	# Iteracion cada 2 minutos
	thr.Timer(120.0, database).start()

# Funcion que calcula el umbral
def f_umbral(wumbral = None):
	# Se ordena el contenido de la base de datos por actualidad
	data_act = results.find().sort('Fecha', DESCENDING)
	n = 0
	error=""
	aux = ""
	noticia = ""

	# Se recorren las entradas ya ordenadas de la base de datos
	for entry in data_act:
		titular = entry['Titular']
		# Se comprueba que el umbral sea numero y positivo
		if wumbral < 0 or wumbral.isdigit()==False:
			error = 'El valor del umbral debe ser un numero mayor que cero'
			break
		# Si el numero de clics supera el umbral y no esta repetida la noticia se cogen los datos
		elif entry['Clics'] > int(wumbral) and aux!=titular:
			n = n+1
			numero=str(n)
			meneos = str(entry['Meneos'])
			clics = str(entry['Clics'])
			mdate = entry['Fecha']
			if n>10:
				break
			# Se crea una cadena que contiene la tabla de noticias a pasarle a la web para que se visualice correctamente
			noticia = noticia + '<tr><td>'+ numero +'</td> <td>'+ titular +'</td> <td>'+ meneos +'</td><td>'+ clics +'</td><td>'+ mdate +'</td></tr>' 
			aux = titular
	return noticia, error

# Funcion que calcula la media de ambas bases de datos
def f_media():
	# En MongoDB 
	m_clics = []	
	# Se ordena por el valor de clics
	data_m = results.find().sort('Clics', DESCENDING)
	# Se almacena el valor de cada clic en un array
	for entry in data_m:
		m_clics.append(entry['Clics'])
	# Se calcula la media
	m_media = numpy.mean(m_clics)
	m_media = ("%.2f" % m_media)

	# En Beebotte
	b_clics = []
	# Se leen los valores de los clics (fijando un limite)
	data_b = bclient.read("compu", "Clics", limit=1000)
	# Se almacena el valor de cada clic en un array
	for entry in data_b:
		b_clics.append(entry['data'])
	# Se calcula la media
	b_media = numpy.mean(b_clics)
	b_media = ("%.2f" % b_media)
	return m_media, b_media