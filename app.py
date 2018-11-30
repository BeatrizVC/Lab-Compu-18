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
	# Datos de la primera noticia
	[titular, meneos, clics, date] = runtime.check()
	# Datos de las dos medias
	[mmedia, bmedia] = runtime.f_media()
	if request.method == 'GET':
		return render_template('data.html',date=str(date),titulo=str(titular),meneos=str(meneos),clics=str(clics),mmedia=str(mmedia),bmedia=str(bmedia))
	# Se fija el umbral
	if request.method == 'POST':
		umbral = request.form.get("umbral")
		[noticia, error] = runtime.f_umbral(umbral)
		if len(error) != 0:
			return render_template('data.html',date=str(date),titulo=str(titular),meneos=str(meneos),clics=str(clics),mmedia=str(mmedia),bmedia=str(bmedia), error=str(error))
		if len(noticia) == 0:
			mensaje='No se han encontrado noticias que superen el umbral de clics indicado'
			return render_template('data2.html',umbral=str(umbral), mensaje=str(mensaje))
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