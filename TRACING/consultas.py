#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import sys
from anadir import anadirSeguimiento
from buscar import Find
import conexion
import time
import datetime

class consultasSeguimientos:
	
	def __init__(self):
		#Obtenemos la ruta de la carpeta donde se encuentra el glade
		pathname = os.path.dirname(sys.argv[0])
		ruta = os.path.abspath(pathname) + "/GUI/"
		pantallaPrincipal = ruta + "consultas.glade"
		
		builder= gtk.Builder()
		builder.add_from_file(pantallaPrincipal)

		self.hbox1 = builder.get_object("hbox1")
		self.rbPorCentro = builder.get_object("rbPorCentro")
		self.rbPorFecha = builder.get_object("rbPorFecha")
		self.cbxTipo = builder.get_object("cbxTipo")
		self.cbxTipologia = builder.get_object("cbxTipologia")
		self.cbxCentro = builder.get_object("cbxCentro")
		self.lsTipo = builder.get_object("lsTipo")
		self.lsTipologia = builder.get_object("lsTipologia")
		self.lsCentro = builder.get_object("lsCentro")
		self.lsResultadoConsulta = builder.get_object("lsResultadoConsulta")
		self.cbxGrupo = builder.get_object("cbxGrupo")
		self.lsGrupo = builder.get_object("lsGrupo")
		self.hbuttonbox2 = builder.get_object("hbuttonbox2")
		self.tbRegRecuperados = builder.get_object("tbRegRecuperados")

		#Obtenemos el msgbox
		self.msgbox = builder.get_object("msgbox")
		self.lbMensaje = builder.get_object("lbMensaje")
		self.btMsgboxAceptar = builder.get_object("btMsgBoxAceptar")




		dict = {"on_rbPorCentro_toggled": self.rbPorCentroActivate,
				"on_rbPorFecha_toggled": self.rbPorFechaActivate,
				"on_cbxTipo_changed": self.cbxTipoChanged,
				"on_cbxTipologia_changed": self.cbxTipoChanged,
				"on_btConsultar_clicked": self.btConsultarClick,
				"on_btMsgBoxAceptar_clicked": self.btMsgBoxAceptar
				}
		builder.connect_signals(dict)


	def rbPorCentroActivate(self,widget):
		self.hbox1.show()
		self.hbuttonbox2.hide()

	def rbPorFechaActivate(self, widget):
		self.hbox1.hide()
		self.hbuttonbox2.show()

		
	def cbxTipoChanged(self, widget):
		self.lsCentro.clear()

		tipologia = self.cbxTipologia.get_active_text()
		tipo = self.cbxTipo.get_active_text()

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

	def btConsultarClick(self, widget):
		self.lsResultadoConsulta.clear()
		tipologia = self.cbxTipologia.get_active_text()
		tipo = self.cbxTipo.get_active_text()
		centro = self.cbxCentro.get_active_text()
		grupo = self.cbxGrupo.get_active_text()

		if self.rbPorCentro.get_active() == True:
			if centro == None:
				self.msgbox.show()
				self.lbMensaje.set_text("Seleccione el centro")
			else:

				queryPorCentro = "SELECT DEPENDIENTE.Expdte, DEPENDIENTE.Nombre, INFORMES.FechaInforme, CENTRO.NombreCentro FROM DEPENDIENTE, INFORMES, CENTRO WHERE CENTRO.NombreCentro = \'" + centro + "' AND CENTRO.TipoCentro = \'" + tipo + "' AND CENTRO.Tipologia = \'" + tipologia + "' AND CENTRO.IdCentro = INFORMES.IdCentro AND CENTRO.IdCentro=DEPENDIENTE.IdCentro AND DEPENDIENTE.Expdte = INFORMES.Expdte ORDER BY DEPENDIENTE.Expdte ASC"

				c = conexion.db
				cursor = c.cursor()

				try:
					cursor.execute(queryPorCentro)
				except Exception, e:
					raise e

				resultado = cursor.fetchall()

				if len(resultado) != 0:
					for i in range(len(resultado)):
						self.lsResultadoConsulta.append(resultado[i])

				queryPorCentroCount = "SELECT COUNT(*) FROM DEPENDIENTE, INFORMES, CENTRO WHERE CENTRO.NombreCentro = \'" + centro + "' AND CENTRO.TipoCentro = \'" + tipo + "' AND CENTRO.Tipologia = \'" + tipologia + "' AND CENTRO.IdCentro = INFORMES.IdCentro AND CENTRO.IdCentro=DEPENDIENTE.IdCentro AND DEPENDIENTE.Expdte = INFORMES.Expdte"

				try:
					cursor.execute(queryPorCentroCount)
				except Exception, e:
					raise e

				contado = cursor.fetchone()[0]

				self.tbRegRecuperados.set_text(str(contado))


		elif self.rbPorFecha.get_active() == True:
			
			today = datetime.date.today()

			queryPorFecha = "SELECT DEPENDIENTE.Expdte, DEPENDIENTE.Nombre, INFORMES.FechaInforme, CENTRO.NombreCentro FROM INFORMES, DEPENDIENTE, CENTRO WHERE CENTRO.Grupo = \'" + grupo + "' AND INFORMES.Expdte = DEPENDIENTE.Expdte AND DEPENDIENTE.Estado = 'Alta' AND CENTRO.IdCentro = INFORMES.IdCentro AND INFORMES.FechaInforme <= DATE_SUB(CURDATE(), INTERVAL 180 DAY) ORDER BY CENTRO.NombreCentro ASC"

			c = conexion.db
			cursor = c.cursor()

			try:
				cursor.execute(queryPorFecha)
			except Exception, e:
				raise e

			resultado = cursor.fetchall()

			if len(resultado) != 0:
				for i in range(len(resultado)):
					self.lsResultadoConsulta.append(resultado[i])

			queryPorCentroCount = "SELECT COUNT(*) FROM INFORMES, DEPENDIENTE, CENTRO WHERE CENTRO.Grupo = \'" + grupo + "' AND INFORMES.Expdte = DEPENDIENTE.Expdte AND DEPENDIENTE.Estado = 'Alta' AND CENTRO.IdCentro = INFORMES.IdCentro AND INFORMES.FechaInforme <= DATE_SUB(CURDATE(), INTERVAL 180 DAY)"

			try:
				cursor.execute(queryPorCentroCount)
			except Exception, e:
				raise e

			contado = cursor.fetchone()[0]

			self.tbRegRecuperados.set_text(str(contado))

	def btMsgBoxAceptar(self, widget):
		self.msgbox.hide()

