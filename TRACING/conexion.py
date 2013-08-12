#!/usr/bin/env python

import MySQLdb

db_host = 'localhost'
usuario = 'root'
clave= 'toor'
base_de_datos= 'tracing'
	

db = MySQLdb.connect(host=db_host, user=usuario, passwd=clave, db=base_de_datos)