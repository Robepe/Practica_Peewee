import pymysql
import json
import logging
from peewee import *


# Funcion para acceder a la configuración del conector ('user', 'password', ...)
#	@return 'data': diccionario con las claves/valor de la configuración
def getDBconfig():
	config = open('config.json')
	data = json.load(config)
	config.close()

	return data


# Funcion que crea la conexion a la Base de Datos, creando la Base de Datos en caso de no existir
#	@return db: variable que almacena la conexión a la Base de datos (MySQLDatabase)
def conectarDB():
	# Creamos la base de datos
	config = getDBconfig()
	conn = pymysql.connect(user = config['user'],
					password = config['password'],
					host = config['host'],
					port = int(config['port']))

	conn.cursor().execute("CREATE DATABASE IF NOT EXISTS CentroFormacion")
	conn.close()

	# Asignamos a la variable 'db' la conexión a la base de datos
	db = MySQLDatabase(database = config['database'],
				user = config['user'],
				password = config['password'],
				host = config['host'],
				port = int(config['port']))

	return db


db = conectarDB()		# Asignamos la conexion de la Base de datos a la variable DB.


##############################################################
######     					Clases     					######
##############################################################


# Clase que define el modelo Peewee para conectar a la base de datos
class BaseModel(Model):
		class Meta:
			database = db

# Clase que hereda del modelo, y representa la tabla 'alumno' en la BBDD
# modificaciones presentes:
#		* max_length: delimita la longitud máxima de la cadena de texto
#		* unique	: establece si el valor de un campo ha de ser 'unico'
#		* null		: establece si el valor de un campo puede ser 'null'
class Alumno(BaseModel):
	expedienteAlumn = PrimaryKeyField()
	nombreAlumn = CharField(max_length=25)
	apellidosAlumn = CharField(max_length=50)
	nombre_completo = CharField(max_length=51, unique = True)
	telefonoAlumn = CharField(max_length=9, unique = True)
	direccionAlumn = CharField(max_length=50, null=True)
	fechaAlumn = DateField()

# Clase que hereda del modelo, y representa la tabla 'profesor' en la BBDD
class Profesor(BaseModel):
	idProfe = PrimaryKeyField()
	nombreProfe = CharField(max_length=25)
	apellidosProfe = CharField(max_length=50)
	nombre_completo = CharField(max_length=51)
	telefonoProfe = CharField(max_length=9, unique = True)
	direccionProfe = CharField(max_length=50)
	dniProfe = CharField(max_length=10, unique = True)

# Clase que hereda del modelo, y representa la tabla 'curso' en la BBDD
# modificaciones presentes:
#		* backref	: define una relación inversa, permitiendo acceder a los registros de la tabla secundaria
#		* on_delete	: establece el 'modus operandi' en caso de eliminar el registro al que hace referencia el valor.
#					  En este caso, si el profesor al que hace referencia la FK es eliminado, el valor será 'Null'
#		* default	: establece el valor por defecto en caso de estar vacio (Null)
class Curso(BaseModel):
	idCurso = PrimaryKeyField()
	nombreCurso = CharField(max_length=25)
	descripcionCurso = CharField(max_length=50)
	id_Profesor = ForeignKeyField(Profesor, backref='cursos', null=True, on_delete='SET NULL', default=None)

# Clase que hereda del modelo, y representa la tabla 'matricula' en la BBDD
# modificaciones presentes:
#		* backref	: define una relación inversa, permitiendo acceder a los registros de la tabla secundaria
#		* on_delete	: establece el 'modus operandi' en caso de eliminar el registro al que hace referencia el valor.
#					  En este caso, si el profesor al que hace referencia la FK es eliminado, el valor será 'Null'
#		* default	: establece el valor por defecto en caso de estar vacio (Null)
class Matricula(BaseModel):
	id_Alumno = ForeignKeyField(Alumno, backref='matriculas', on_delete='CASCADE')
	id_Curso = ForeignKeyField(Curso, backref='matriculas',on_delete='CASCADE')
	class Meta:
		primary_key = CompositeKey('id_Alumno', 'id_Curso')


# Muestra sentencias SQL que se ejecutan por debajo por pantalla
#	@param 'db': conexión válida a la base de datos
def iniciarLogger(db):
	logger = logging.getLogger('peewee')
	logger.addHandler(logging.StreamHandler())
	logger.setLevel(logging.DEBUG)


# Método dedicado a la creación de las tablas de la BBDD
#	@param 'db': conexión válida a la base de datos
def createTables(db):
	db.create_tables([Alumno, Profesor, Curso, Matricula])


# Método que inserta 5 cursos predefinidos a la tabla 'curso'
#	@param 'db': conexión válida a la base de datos
def addCursos(db):
	Curso.get_or_create(nombreCurso = "DAM", descripcionCurso = "Desarrollo de Aplicaciones Multiplataforma")
	Curso.get_or_create(nombreCurso = "DAW", descripcionCurso = "Desarrollo de Aplicaciones Web")
	Curso.get_or_create(nombreCurso = "ISC", descripcionCurso = "Grado Ingenieria Informatica")
	Curso.get_or_create(nombreCurso = "MIT", descripcionCurso = "Grado Ciber Seguridad")
	Curso.get_or_create(nombreCurso = "IT", descripcionCurso = "Grado en Telecomunicaciones")

