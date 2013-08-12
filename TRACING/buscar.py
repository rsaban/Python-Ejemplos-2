#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import conexion
from actualizar import actualizarSeguimiento
import datetime
import time
from anadir import anadirSeguimiento

class Find:
	
	def __init__(self):
		#Obtenemos la ruta de la carpeta donde se encuentra el glade
		pathname = os.path.dirname(sys.argv[0])
		ruta = os.path.abspath(pathname) + "/GUI/"
		pantallaPrincipal = ruta + "busqueda.glade"
		
		builder= gtk.Builder()
		builder.add_from_file(pantallaPrincipal)
					
		self.ventana = builder.get_object("Busqueda")
		self.tbBusqueda = builder.get_object("tbBusqueda")
		self.lsBusqueda = builder.get_object("lsBusqueda")

		self.btBuscar = builder.get_object("btBuscar")
		self.btVer = builder.get_object("btVer")

		self.tvBusqueda = builder.get_object("tvBusqueda")

		#obtenemos los radiobutton
		self.rbExpdte = builder.get_object("rbExpdte")
		self.rbNombre = builder.get_object("rbNombre")
		
		#Obtenemos el msgbox
		self.msgbox = builder.get_object("msgbox")
		self.lbMensaje = builder.get_object("lbMensaje")
		self.btMsgboxAceptar = builder.get_object("btMsgBoxAceptar")


		dict = {"on_btBuscar_clicked": self.btBuscarClick, 
				"on_btVer_clicked": self.btVerClick,
				"on_btMsgBoxAceptar_clicked": self.btMsgBoxAceptarClick,
				"on_btNuevoInforme_clicked": self.btNuevoInformeClick
				}
		builder.connect_signals(dict)

	def btBuscarClick(self, widget):
		self.lsBusqueda.clear()

		peticion = self.tbBusqueda.get_text()

		c = conexion.db
		cursor = c.cursor()

		if self.rbExpdte.get_active() == True:
			try:
				query = "SELECT DEPENDIENTE.Expdte, DEPENDIENTE.Nombre, INFORMES.FechaInforme FROM DEPENDIENTE, INFORMES WHERE DEPENDIENTE.Expdte = \"" + peticion + "\" AND INFORMES.Expdte = DEPENDIENTE.Expdte"  
				cursor.execute(query)
			except Exception, e:
				raise e

		elif self.rbNombre.get_active() == True:
			try:
				query = "SELECT DEPENDIENTE.Expdte, DEPENDIENTE.Nombre, INFORMES.FechaInforme FROM DEPENDIENTE, INFORMES WHERE DEPENDIENTE.Nombre LIKE \"%" + peticion + "%\" AND INFORMES.Expdte = DEPENDIENTE.Expdte" 
				cursor.execute(query)
			except Exception, e:
				raise e
		
		encontrado = cursor.fetchall()
		
		if len(encontrado) != 0:
			for i in range(len(encontrado)):
				self.lsBusqueda.append(encontrado[i])
		else:
			self.msgbox.show()
			self.lbMensaje.set_text("No se encontraron resultados")
			return

		cursor.close()


	def btVerClick(self, widget):
		
		tv = self.tvBusqueda	
		selection = tv.get_selection()
		model, treeiter = selection.get_selected()
		if treeiter != None:
			x = model[treeiter][0]
			y = model[treeiter][1]
			z = model[treeiter][2]
		
			c = conexion.db
			cursor = c.cursor()

			try:
				query = "SELECT CENTRO.TipoCentro, CENTRO.Tipologia, CENTRO.NombreCentro, INFORMES.Observaciones, INFORMES.IdInforme FROM CENTRO, DEPENDIENTE, INFORMES WHERE DEPENDIENTE.Expdte = \"" + x + "\" AND INFORMES.FechaInforme = \"" + z + "\" AND DEPENDIENTE.Expdte=INFORMES.Expdte AND CENTRO.IdCentro = DEPENDIENTE.IdCentro" 
				cursor.execute(query)
			except Exception, e:
				raise e

			dato = cursor.fetchone()
	
			tipo = dato[0]
			tipologia = dato[1]
			nombrec = dato[2]
			observ = dato[3]
			informe = dato[4]
	

			#enviamos todo a la ficha
			actualizarSeguimiento().cargarDatos(x, y, tipo, tipologia, nombrec, observ, z, informe)

			self.ventana.hide()

		else:
			self.msgbox.show()
			self.lbMensaje.set_text("No hay nada seleccionado")


	def btMsgBoxAceptarClick(self, widget):
		self.msgbox.hide()
		
	def btNuevoInformeClick(self, widget):
		tv = self.tvBusqueda	
		selection = tv.get_selection()
		model, treeiter = selection.get_selected()
		if treeiter != None:
			x = model[treeiter][0]
			y = model[treeiter][1]
			z = model[treeiter][2]
		
		
			c = conexion.db
			cursor = c.cursor()

			try:
				query = "SELECT CENTRO.TipoCentro, CENTRO.Tipologia, CENTRO.NombreCentro FROM CENTRO, DEPENDIENTE WHERE DEPENDIENTE.Expdte = \"" + x + "\" AND CENTRO.IdCentro = DEPENDIENTE.IdCentro" 
				cursor.execute(query)
			except Exception, e:
				raise e

			dato = cursor.fetchone()
	
			tipo = dato[0]
			tipologia = dato[1]
			nombrec = dato[2]

	

			#enviamos todo a la venana Anadir
			anadirSeguimiento().cargarDatos(x, y, tipo, tipologia, nombrec)

			self.ventana.hide()

		else:
			self.msgbox.show()
			self.lbMensaje.set_text("No hay nada seleccionado")