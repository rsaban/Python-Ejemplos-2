#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
from anadir import anadirSeguimiento
from buscar import Find
from consultas import consultasSeguimientos
from estadoResidentes import altasBajas


class main:
	
	def __init__(self):
		#Obtenemos la ruta de la carpeta donde se encuentra el glade
		pathname = os.path.dirname(sys.argv[0])
		ruta = os.path.abspath(pathname) + "/GUI/"
		pantallaPrincipal = ruta + "main.glade"
		
		builder= gtk.Builder()
		builder.add_from_file(pantallaPrincipal)

			
		dict = {"on_btAnadir_clicked": self.btAnadirClick,
				"on_btBuscar_clicked": self.btBuscarClick,
				"on_btConsultar_clicked":self.btConsultarClick,
				"on_btEstado_clicked": self.btEstadoClick,
				"gtk_main_quit": self.Salir}
		builder.connect_signals(dict)


	def btAnadirClick(self, widget):
		anadirSeguimiento()

	def btBuscarClick(self, widget):
		Find()

	def btConsultarClick(self, widget):
		consultasSeguimientos()

	def btEstadoClick(self, widget):
		altasBajas()

	def Salir(self, widget, data=None):
		if os.path.exists("salida.pdf"):
			os.remove("salida.pdf")
		gtk.main_quit()

	
if __name__=="__main__":
	main()
	gtk.main()


		