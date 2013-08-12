#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
import conexion
import datetime


class anadirSeguimiento:
	
	def __init__(self):
		#Obtenemos la ruta de la carpeta donde se encuentra el glade
		pathname = os.path.dirname(sys.argv[0])
		ruta = os.path.abspath(pathname) + "/GUI/"
		pantallaPrincipal = ruta + "anadir.glade"
		
		builder= gtk.Builder()
		builder.add_from_file(pantallaPrincipal)
		self.ventanaAnadirSeguimiento = builder.get_object("AnadirSeguimiento")
		self.ventanaAnadirCentro = builder.get_object("AnadirCentro")
		self.cbxDia = builder.get_object("cbxDia")
		self.cbxMes = builder.get_object("cbxMes")
		self.cbxAno = builder.get_object("cbxAno")
		self.lsDia = builder.get_object("lsDia")
		self.lsAno = builder.get_object("lsAno")
		self.lsCentro = builder.get_object("lsCentro")
		self.cbxNombreCentro = builder.get_object("cbxNombreCentro")
		self.cbxTipologiaCentro = builder.get_object("cbxTipologiaCentro")
		self.cbxGrupo = builder.get_object("cbxGrupo")
		self.cbxTipoCentro = builder.get_object("cbxTipoCentro")
		self.tbExpdte = builder.get_object("tbExpdte")
		self.tbNombre = builder.get_object("tbNombre")
		self.tbObservaciones = builder.get_object("tbObservaciones")
		self.lsTipoCentro = builder.get_object("lsTipoCentro")
		self.lsTipologiaCentro = builder.get_object("lsTipologiaCentro")

	
		#Obtenemos el msgbox
		self.msgbox = builder.get_object("msgbox")
		self.lbMensaje = builder.get_object("lbMensaje")
		self.btAceptarMsgBox = builder.get_object("btAceptarMsgBox")
		self.msgbox.hide()

		#Cargamos los comobox(liststore) del dia y el ano
		for x in range(0, 31):
			self.lsDia.append([str(x+1)])

		for y in range (2006, 2100):
			self.lsAno.append([str(y)])

		#Ponemos el primer item de dia y mes activo y el ano 2013
		self.cbxAno.set_active(0)
		self.cbxMes.set_active(0)
		self.cbxDia.set_active(0)

		#elementos de la ventana anadir centro
		self.cbxAnadirTipoCentro = builder.get_object("cbxAnadirTipoCentro")
		self.cbxAnadirTipologiaCentro = builder.get_object("cbxAnadirTipologiaCentro")
		self.tbAnadirNombreCentro = builder.get_object("tbAnadirNombreCentro")

			
		dict = {"on_btAnadirCentro_clicked": self.btMostrarAnadirCentroClick,
				"on_btAceptarAnadirCentro_clicked": self.btAnadirCentroClick,
				"on_cbxTipologiaCentro_changed": self.cbxTipologiaCentroChanged,
				"on_cbxTipoCentro_changed": self.cbxTipologiaCentroChanged,
				"on_btAceptar_clicked": self.btAceptarClick,
				"on_btAceptarMsgBox_clicked": self.btAceptarMsgBoxClick,
				"on_AnadirCentro_delete_event": self.deleteAnadir
				}
		builder.connect_signals(dict)


	def btMostrarAnadirCentroClick(self, widget):
		self.ventanaAnadirCentro.show()

	def deleteAnadir(self, widget, data=None):
		self.ventanaAnadirCentro.hide()
		self.cbxAnadirTipoCentro.set_active(0)
		self.cbxAnadirTipologiaCentro.set_active(0)
		self.tbAnadirNombreCentro.set_text("")
		self.cbxGrupo.set_active(0)
		return True


	#Anadimos un nuevo Centro
	def btAnadirCentroClick(self, widget):
		#obtenemos los valores
		tipo = self.cbxAnadirTipoCentro.get_active_text()
		tipologia = self.cbxAnadirTipologiaCentro.get_active_text()
		nombre = self.tbAnadirNombreCentro.get_text()
		grupo = self.cbxGrupo.get_active_text()


		#hacemos el insert
		c = conexion.db
		cursor = c.cursor()

		queryInsertCentro = "INSERT INTO CENTRO (NombreCentro, TipoCentro, Tipologia, Grupo) VALUES (" + "'" + nombre + "', '" + tipo + "', '" + tipologia + "', '" + grupo + "')"

		try:
			cursor.execute(queryInsertCentro)
			c.commit()
			self.msgbox.show()
			self.lbMensaje.set_text("Centro grabado con exito. Vuelva a seleccionar el Tipo de Centro y Tipologia para visualizar el nuevo centro")
			self.btAceptarMsgBox.set_label("Aceptar")
		except Exception, e:
			raise e

		cursor.close


	def cbxTipologiaCentroChanged(self, widget):
		self.lsCentro.clear()

		tipologia = self.cbxTipologiaCentro.get_active_text()
		tipo = self.cbxTipoCentro.get_active_text()

		query = "SELECT NombreCentro FROM CENTRO WHERE Tipologia =" + "'" + tipologia + "' AND TipoCentro =" + "'" + tipo + "'"
		c = conexion.db
		cursor = c.cursor()
		
		try:
			cursor.execute(query)
		except Exception, e:
			raise e

		encontrado = cursor.fetchall()

		if len(encontrado) != 0:
			for i in range(len(encontrado)):
				self.lsCentro.append(encontrado[i])


	def btAceptarClick(self, widget):
		centroSeleccionado = self.cbxNombreCentro.get_active_text()
		if centroSeleccionado == None:
			self.msgbox.show()
			self.lbMensaje.set_text("El nombre del centro es obligatorio")
			self.btAceptarMsgBox.set_label("Aceptar")
			return

		expdte = self.tbExpdte.get_text()
		if expdte == "" or expdte.isspace() == True:
			self.msgbox.show()
			self.lbMensaje.set_text("El numero de expediente es obligatorio")
			self.btAceptarMsgBox.set_label("Aceptar")
			return
		nombreDep = self.tbNombre.get_text()
		observaciones = self.tbObservaciones.get_buffer()
		obs = observaciones.get_text(*observaciones.get_bounds())

		dia = self.cbxDia.get_active_text()
		elementoCombo = self.cbxMes.get_active()
		mes = elementoCombo + 1
		ano = self.cbxAno.get_active_text()

		fecha = str(dia) + "/" + str(mes) + "/" + str(ano)
		day = datetime.datetime.strptime(fecha, '%d/%m/%Y')
		date = day.strftime('%Y-%m-%d')

		queryCentro = "SELECT IdCentro FROM CENTRO WHERE NombreCentro =" + "'" + centroSeleccionado + "'"


		c = conexion.db
		cursor = c.cursor()

		try:
			cursor.execute(queryCentro)
		except Exception, e:
			raise e
		
		resultado = cursor.fetchone()
		centroID = resultado[0]

		#comprobamos si existe el dependiente y en el centro elegido
		queryDepen = "SELECT * FROM DEPENDIENTE WHERE Expdte=" + "'" + expdte + "' AND IdCentro='" + str(centroID) + "'" 
		try:
			cursor.execute(queryDepen)
		except Exception, e:
			raise e
		expdteExiste = cursor.fetchone()

		#sql para insertar
		queryInsertDepend = "INSERT INTO DEPENDIENTE (Expdte, Nombre, IdCentro, Estado) VALUES (" + "'" + expdte + "', '" + nombreDep + "', '" + str(centroID) + "', 'Alta')"
		queryInsertInforme = "INSERT INTO INFORMES (FechaInforme, Observaciones, IdCentro, Expdte) VALUES (" + "'" + date + "', '" + obs + "', '" + str(centroID) + "', '" + expdte + "')"

		try:
			#si no existe el dependiente, se crea, si existe, se graba solo el informe
			if expdteExiste == None:
				cursor.execute(queryInsertDepend)
					
			cursor.execute(queryInsertInforme)
						
			c.commit()
			self.msgbox.show()
			self.lbMensaje.set_text("Seguimiento grabado con exito.")
			self.btAceptarMsgBox.set_label("Ok")
		except Exception, e:
			raise e

		cursor.close()

	def btAceptarMsgBoxClick(self, widget):
		if self.btAceptarMsgBox.get_label() == "Ok":
			self.msgbox.hide()
			self.ventanaAnadirSeguimiento.hide()
		else:
			self.msgbox.hide()
			self.ventanaAnadirCentro.hide()
			self.cbxAnadirTipoCentro.set_active(0)
			self.cbxAnadirTipologiaCentro.set_active(0)
			self.tbAnadirNombreCentro.set_text("")
			self.cbxGrupo.set_active(0)

	def cargarDatos(self, *argv):

		self.tbExpdte.set_text(argv[0])
		self.tbNombre.set_text(argv[1])

		for posicion, elemento in enumerate(self.lsTipoCentro):
			f = elemento[0]
			if f == argv[2]:
				self.cbxTipoCentro.set_active(posicion)

		for posicion, elemento in enumerate(self.lsTipologiaCentro):
			f = elemento[0]
			if f == argv[3]:
				self.cbxTipologiaCentro.set_active(posicion)

		for posicion, elemento in enumerate(self.lsCentro):
			f = elemento[0]
			if f == argv[4]:
				self.cbxNombreCentro.set_active(posicion)

