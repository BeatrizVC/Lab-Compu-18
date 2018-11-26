# Beatriz Vadillo Cortes
# MUIT - Computacion en Red: Practica 1

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import runtime
from flask import Flask, render_template, request, redirect 

app = Flask(__name__)

# Mostramos los datos por patalla y esperamos un umbral
@app.route('/', methods=['GET', 'POST'])
def show_data():
	# Mostramos datos
	if request.method == 'GET':
		# Datos de la primera noticia
		[titular, meneos, clics, date] = runtime.check()
		# Datos de las dos medias
		[mmedia, bmedia] = runtime.f_media()
		return render_template('data.html',date=str(date),titulo=str(titular),meneos=str(meneos),clics=str(clics),mmedia=str(mmedia),bmedia=str(bmedia))
	# Se fija el umbral
	if request.method == 'POST':
		umbral = request.form['umbral']
		umbral = int(umbral)
		noticia = runtime.f_umbral(umbral)
		return render_template('data2.html',umbral=str(umbral), noticia=str(noticia))

# Mostramos las graficas
@app.route('/graf')
def show_graficas():
	return render_template('data3.html')

if __name__ == '__main__':
	# Se llama a la funcion que arranca el timer
	runtime.bucle()
	app.debug=True
	app.run(host='0.0.0.0')