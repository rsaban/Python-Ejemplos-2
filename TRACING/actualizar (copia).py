#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import conexion
import subprocess


class actualizarSeguimiento:
	
	def __init__(self):
		#Obtenemos la ruta de la carpeta donde se encuentra el glade
		pathname = os.path.dirname(sys.argv[0])
		ruta = os.path.abspath(pathname) + "/GUI/"
		pantallaPrincipal = ruta + "actualizar.glade"

		builder= gtk.Builder()
		builder.add_from_file(pantallaPrincipal)
					
		self.ventanaActualizar = builder.get_object("Actualizar")
		self.lbExpdte = builder.get_object("lbExpdte")
		self.lbNombre = builder.get_object("lbNombre")
		self.lbTipoCentro = builder.get_object("lbTipoCentro")
		self.lbTipologia = builder.get_object("lbTipologia")
		self.lbCentro = builder.get_object("lbCentro")
		self.lbFecha = builder.get_object("lbFecha")
		self.lbIdInforme = builder.get_object("lbIdInforme")
		
		self.tbObservaciones = builder.get_object("tbObservaciones")
		
		#Obtenemos el msgbox
		self.msgbox = builder.get_object("msgbox")
		self.lbMensaje = builder.get_object("lbMensaje")
		self.btAceptarMsgBox = builder.get_object("btAceptarMsgBox")
		self.msgbox.hide()
		
		#Obtenemos el selector de archivos
		self.selectorArchivos = builder.get_object("selectorArchivos")

		dict = {"on_btActualizar_clicked":self.btActualizarClick,
				"on_btAceptarMsgBox_clicked": self.btAceptarMsgBoxClick,
				"on_btPDF_clicked": self.btPDFClick,
				"on_btVerPDF_clicked": self.btVerPDFClick
				}
		builder.connect_signals(dict)

	def cargarDatos(self, *argv):

		self.lbExpdte.set_text(argv[0])
		self.lbNombre.set_text(argv[1])
		self.lbTipoCentro.set_text(argv[2])
		self.lbTipologia.set_text(argv[3])
		self.lbCentro.set_text(argv[4])

 		textbuffer = self.tbObservaciones.get_buffer() 
 		textbuffer.set_text(argv[5]) 

		self.lbFecha.set_text(argv[6])

		self.lbIdInforme.set_text(str(argv[7]))

	def btActualizarClick(self, widget):
		observaciones = self.tbObservaciones.get_buffer()
		obs = observaciones.get_text(*observaciones.get_bounds())
		informeConsultado = self.lbIdInforme.get_text()

		queryActualizar = "UPDATE INFORMES SET Observaciones =" + "'" + obs +"' WHERE IdInforme ='" + informeConsultado + "'"

		c = conexion.db
		cursor = c.cursor()

		try:
			cursor.execute(queryActualizar)
			c.commit()
			self.msgbox.show()
			self.lbMensaje.set_text("Seguimiento actualizado con exito.")
			self.btAceptarMsgBox.set_label("Aceptar")
		except Exception, e:
			raise e



	def btAceptarMsgBoxClick(self, widget):
		self.msgbox.hide()
		self.ventanaActualizar.hide()

	def btPDFClick(self, widget):
		informeConsultado = self.lbIdInforme.get_text()
		respt = self.selectorArchivos.run()
		self.selectorArchivos.hide()
		if respt == -5:
			pdfSeleccionado = open(self.selectorArchivos.get_filename())
			pdfBin = pdfSeleccionado.read()
			pdfSeleccionado.close()

			queryInsertarPDF = "UPDATE INFORMES SET PDF = %s WHERE IdInforme =\'" + informeConsultado + "'"
			c = conexion.db
			cursor = c.cursor()

			try:
				cursor.execute(queryInsertarPDF, (pdfBin, ))
				c.commit()
				self.msgbox.show()
				self.lbMensaje.set_text("PDF adjuntado con exito.")
				self.btAceptarMsgBox.set_label("Aceptar")
			except Exception, e:
				raise e
				c.rollback

			cursor.close()

			self.selectorArchivos.hide()

	def btVerPDFClick(self, widget):
		informeConsultado = self.lbIdInforme.get_text()

		queryVerPDF = "SELECT PDF FROM INFORMES WHERE IdInforme = \'" + informeConsultado + "'"

		c = conexion.db
		cursor = c.cursor()

		try:
			cursor.execute(queryVerPDF)
		except Exception, e:
			raise e

		data = cursor.fetchone()[0]
		


		#Este de aqui abajo te genera el pdf
		fout = open('salida.pdf', 'wb')
		fout.write (data)

		os.system("evince salida.pdf &")
