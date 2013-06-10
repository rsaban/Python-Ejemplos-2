#!/usr/bin/env python

import gtk
import os
import sys
import MySQLdb
import conexion
from Crypto.Cipher import ARC4

class main:
	
	def __init__(self):
		#Obtenemos la ruta de la carpeta donde se encuentra el glade
		pathname = os.path.dirname(sys.argv[0])
		ruta = os.path.abspath(pathname) + "/GUI/"
		form1 = ruta + "form1.glade"
		
		builder= gtk.Builder()
		builder.add_from_file(form1)
		
		self.tbBuscar = builder.get_object("tbBuscar")
		self.tbId = builder.get_object("tbId")
		self.tbNombre = builder.get_object("tbNombre")
		self.tbApellidos = builder.get_object("tbApellidos")
		self.tbSexo = builder.get_object("tbSexo")
		self.tbLocalidad = builder.get_object("tbLocalidad")


		dict = {"on_btGuardar_clicked": self.btGuardarClick,
				"on_btBuscar_clicked": self.btBuscarClick,
				"gtk_main_quit": self.Salir}
		builder.connect_signals(dict)

	def btGuardarClick(self,widget):
		
		iden = self.tbId.get_text()
		nombre = self.tbNombre.get_text()
		apellidos = self.tbApellidos.get_text()
		sexo = self.tbSexo.get_text()
		localidad = self.tbLocalidad.get_text()

		encriptar = ARC4.new('01234567')
		cosa_encriptada = encriptar.encrypt(localidad)

		c = conexion.db

		cursor = c.cursor()
		
		query= "INSERT INTO Usuarios (Id, Nombre, Apellidos, Sexo, Localidad) VALUES (" + "'" + iden + "', '" + nombre + "', '" + apellidos + "', '" + sexo + "', '" + cosa_encriptada + "')"
		try:
			cursor.execute(query)
		
			c.commit()			

		except Exception, e:
			raise e
			
		cursor.close

	def btBuscarClick(self, widget):
		buscar = self.tbBuscar.get_text()

		c = conexion.db
			
		cursor = c.cursor()

		query = "SELECT * FROM Usuarios WHERE Id = " + "'" + buscar + "'"
		try:
			cursor.execute(query)
		except Exception, e:
			c.rollback()

		
		encontrado = cursor.fetchone()

		self.tbId.set_text(str(encontrado[0]))
		self.tbNombre.set_text(encontrado[1])
		self.tbApellidos.set_text(encontrado[2])
		self.tbSexo.set_text(encontrado[3])
		
		desencriptar = ARC4.new('01234567')
		cosa_desencriptada = desencriptar.decrypt(encontrado[4])

		self.tbLocalidad.set_text(cosa_desencriptada)

		cursor.close

	def Salir(self, widget, data=None):
		gtk.main_quit()

		
if __name__=="__main__":
	main()
	gtk.main()
