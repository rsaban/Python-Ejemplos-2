#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import conexion


class altasBajas:
	
	def __init__(self):
		#Obtenemos la ruta de la carpeta donde se encuentra el glade
		pathname = os.path.dirname(sys.argv[0])
		ruta = os.path.abspath(pathname) + "/GUI/"
		pantallaPrincipal = ruta + "estadoResidentes.glade"
		
		builder= gtk.Builder()
		builder.add_from_file(pantallaPrincipal)

		self.estadoResidentes = builder.get_object("estadoResidentes")
		self.tbExpdte = builder.get_object("tbExpdte")
		self.cbxCentro = builder.get_object("cbxCentro")
		self.cbxEstado = builder.get_object("cbxEstado")
		self.lsCentro = builder.get_object("lsCentro")
		self.lsEstado = builder.get_object("lsEstado")

		dict = {"on_btAceptar_clicked": self.btAceptarClick,
				"on_btVer_clicked": self.btVerClick,
				"on_cbxCentro_changed": self.cbxCentroChanged
				}
		builder.connect_signals(dict)

	def btAceptarClick(self, widget):
		centro = self.cbxCentro.get_active_text()
		estado = self.cbxEstado.get_active_text()
		expdte = self.tbExpdte.get_text()

		queryActualizar = "UPDATE DEPENDIENTE, CENTRO SET DEPENDIENTE.Estado =" + "'" + estado +"' WHERE DEPENDIENTE.Expdte = \"" + expdte + "\" AND CENTRO.IdCentro = DEPENDIENTE.IdCentro AND CENTRO.NombreCentro = \'" + centro + "'"  

		c = conexion.db
		cursor = c.cursor()

		try:
			cursor.execute(queryActualizar)
			c.commit()
			self.estadoResidentes.hide()
		except Exception, e:
			raise e


	def btVerClick(self, widget):
		expdte = self.tbExpdte.get_text()

		queryCentro = "SELECT CENTRO.NombreCentro FROM CENTRO, DEPENDIENTE WHERE DEPENDIENTE.Expdte = \"" + expdte + "\" AND CENTRO.IdCentro = DEPENDIENTE.IdCentro" 

		c = conexion.db
		cursor = c.cursor()

		try:
			cursor.execute(queryCentro)
		except Exception, e:
			raise e

		resultado = cursor.fetchall()

		if len(resultado) != 0:
			for i in range(len(resultado)):
				self.lsCentro.append(resultado[i])

	def cbxCentroChanged(self, widget):
		expdte = self.tbExpdte.get_text()
		centro = self.cbxCentro.get_active_text()

		queryEstado = "SELECT DEPENDIENTE.Estado FROM CENTRO, DEPENDIENTE WHERE DEPENDIENTE.Expdte = \"" + expdte + "\" AND CENTRO.IdCentro = DEPENDIENTE.IdCentro AND CENTRO.NombreCentro = \'" + centro + "'" 

		c = conexion.db
		cursor = c.cursor()

		try:
			cursor.execute(queryEstado)
		except Exception, e:
			raise e

		resultado = cursor.fetchone()

		for posicion, elemento in enumerate(self.lsEstado):
			f = elemento[0]
			if f == resultado[0]:
				self.cbxEstado.set_active(posicion)


