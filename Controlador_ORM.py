import sys
import re
import Modelo_ORM as Modelo
from peewee import *
from datetime import datetime


##############################################################
######     				Validadores     				######
##############################################################


# Metodo que recoge un String y valida tanto la longitud como la presencia de caracteres no deseados
#	@param 'string': Cadena de caracteres a ser validada
#	@param 'length': variable de tipo 'int' que determina la longitud máxima de la cadena proporcionada
#	@param 'constraint': variable de tipo 'bool' que determina si se debe restringir la presencia de numeros o no en la cadena
#	@return 'newStr': variable de tipo 'String' con el valor anterior, pero saneado
def validarString(string, length, constraint = False):
	newStr = string.strip()										# eliminamos los espacios en blanco
	for attempt in range(5):									# 'for' que delimita los intentos a 5
		if ((len(newStr) >= 1) and (len(newStr) <= length)):	# 'if' que comprueba si se cumple la longitud estipulada
			if constraint:										# 'if' en caso de que se indique que no deben haber números
				pattern = re.compile("[A-Za-z]")				# Patron establecido a cumplirse (Solo letras de 'A' hasta 'Z', sin ser 'Case Sensitive')
				match = pattern.match(newStr)					# variable que comprueba si hay "Match" con el patron anteriormente establecido
				if match:
					return newStr
				else:
					print(f"\nEntrada invalida: unicamente valores alfabéticos admitidos\nPruebe de nuevo: ")
					newStr = str(input()).strip()
			else:
				return newStr									# En caso de aceptar cadenas con números, retornamos el valor sin utilizar el patrón y la 'regex'
		else:
			print(f"\nEntrada invalida: minimo un caracter, maximo {length} caracteres\nPruebe de nuevo: ")
			newStr = str(input()).strip()						# En caso de no resultar valida, pedimos por teclado una nueva cadena
	print("-" * 20, "Operacion Cancelada", "-" * 20)


# Método que recoge un String, para eliminar caracteres en blanco, y lo convierte a un Integer o Float
#	@param 'x': Input del usuario a ser validado
#	@param 'decimales': variable de tipo 'bool' que determina si la conversión es a 'Int' o 'Float'. Por defecto 'False'
#	@return 'z': variable de tipo 'Int' o 'Float' con el valor introducido por teclado, pero saneado y formateado
def validarInteger(x, decimales = False):
	for attempt in range(5):
		y = x.strip()			# eliminamos los posibles espacios vacios al inicio y final
		try:
			if not decimales:
				z = int(y)		# tratamos de castear el valor proporcionado a la variable 'z'
				return z		# de ser posible, se retorna la variable 'z'
			else:
				z = float(y)
				return z
		except ValueError:
			print("\nEntrada no valida: introduzca exclusivamente numeros entre 0 y 9\nPruebe de nuevo: ")
			x = input()			# de no ser posible la conversión, volvemos a pedir una cifra
	print("\nOperacion cancelada\n")


# Método que valida un String, elimina los posible espacios vacios, y transforma su contenido a uno de tipo 'date'
# 	@param 'dateStr': String con el contenido de la fecha
# 	@return 'Date': variable datetime, (unicamente con la parte 'date') con la fecha introducida
def validarDate(dateStr):
	for attempt in range(5):
		dateStr.strip()
		try:
			date = datetime.strptime(dateStr, "%d/%m/%Y")	# Indicamos el formato en el que está escrita la fecha en el String
			return date.date()
		except ValueError:
			print("\nEntrada no valida: introduzca una fecha en formato (dd/MM/yyyy)\nPruebe de nuevo: ")
			dateStr = input()
	print("\nOperacion cancelada\n")


# Metodo de tipo 'bool' destinado a comprobar una seleccion de tipo (S/N)
#	@return True: En caso de ser una respuesta afirmativa
#	@return False: En caso de ser una respuesta negativa
def confirmarOperacion():
	while True:										# Bucle infinito hasta completar la pregunta
		opcion = (str(input().strip().lower()))
		if (opcion == "s"):
			return True
		elif (opcion == "n"):
			return False
		else:
			print("\nOperacion no reconocida")


# Metodo que recoge una cadena y comprueba que contenga las caracteristicas de un DNI
#	@param 'dni': Input del usuario. Cadena con el DNI a comprobar
#	@return 'dni': Dni introducido validado
def validarDNI(dni):
	for attempt in range(5):
		pattern = re.compile("[0-9]{8}[A-Z]")	# Patron establecido a cumplirse (8 numeros de 0 a 9 y una sola letra mayuscula de la A a la Z)
		match = pattern.match(dni)				# variable que comprueba si hay "Match" con el patron anteriormente establecido

		if not match:
			print("\nFormato de DNI no valido. Pruebe con 8 numeros y una letra")
			newStr = str(input())		# Pedimos otra cadena para comprobarla nuevamente
			dni = newStr.strip()		# eliminamos los posibles campos vacios
			match = pattern.match(dni)	# Comprobamos de nuevo
		else:
			return dni


# Método que recoge dos Strings, y los combina en una sola cadena
# 	@param name: Nombre del objeto (alumno o profesor) introducido
# 	@param surname: Apellido del objeto introducido
# 	@return String que auna ambas cadenas anteriores
def getFullName(name, surname):
	return (f"{name} {surname}")


##############################################################
######     					Alumno     					######
##############################################################

# Método destinado a la creación de objetos Alumno y su inserción en su tabla de la BBDD
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def addAlumno(Modelo):
	finish = False			# Bucle para permitir la repetición del proceso
	while not finish: 		# Introducimos los datos de un objeto 'Alumno'
		nameAlumno = validarString(str(input("\nIntroduce el nombre del Alumno: ")), 25, True)
		surnameAlumno = validarString(str(input("\nIntroduce los apellidos del Alumno: ")), 50, True)
		telAlumno = validarInteger(input("\nIntroduce el telefono del Alumno: "))
		dirAlumno = validarString(str(input("\nIntroduce la dirección del Alumno: ")), 50, True)
		dateAlumno = validarDate(input("\nIntroduce la fecha del Alumno: "))

		print(f"\nNombre completo: {getFullName(nameAlumno, surnameAlumno)}\nTelefono: {telAlumno}\nDireccion: {dirAlumno}\nFecha de nacimiento: {dateAlumno.strftime('%d/%m/%Y')}")
		print("\n¿Desea guardar al alumno? (S/N)")
		confirm = confirmarOperacion()				# Pedimos confirmación para almacenar el Alumno
		if confirm:
			try:		# Creamos el Alumno con los datos proporcionados
				Modelo.Alumno.create(nombreAlumn = nameAlumno, apellidosAlumn = surnameAlumno, nombre_completo = getFullName(nameAlumno, surnameAlumno), telefonoAlumn = telAlumno, direccionAlumn = dirAlumno, fechaAlumn = dateAlumno)
				print("\nAlumno guardado correctamente")
			except IntegrityError as error:		# En caso de error (Redundancia, Integridad, etc) mostramos un mensaje de error, junto a la descripción proporcinada por Peewee
				print(f"\nOperacion Abortada\nSe ha producido un error de tipo: {error}")
		else:
			print("\nOperacion cancelada")		# En caso de no confirmar
		
		print("\n¿Desea añadir otro alumno? (S/N)")	# Preguntamos al usuario si desea finalizar el alta o repetir el proceso para introducir otro alumno distinto
		confirm = confirmarOperacion()
		if not confirm:
			finish = True
		
# Método destinado a la eliminación de objetos Alumno de la tabla 'alumno'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def removeAlumno(Modelo):
	finish = False
	while not finish:
		showAlumnos(Modelo)			# Mostramos el listado de Alumnos
		opt = validarInteger(input("\nIntroduce el expediente del Alumno a eliminar: "))

		try:
			alumno = Modelo.Alumno.get_by_id(opt)						# Seleccionamos un alumno por ID (expedienteAlumn)
			print("\n¿Seguro que desea eliminar este alumno? (S/N)")
			confirm = confirmarOperacion()
			if confirm:
				alumno.delete_instance()								# Eliminamos el alumno seleccionado
				print("\nAlumno eliminado correctamente")
			else:
				print("\nOperacion cancelada")
		except DoesNotExist:		# En caso de no encontrar un Alumno con el ID proporcionado, recogemos la excepción
			print(f"\nNo se ha encontrado ningun alumno con expediente '{opt}'")
		
		print("\n¿Desea eliminar otro alumno? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a la modificacion de objetos Alumno de la tabla 'alumno'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def modifyAlumno(Modelo):
	finish = False
	while not finish:
		showAlumnos(Modelo)
		opt = validarInteger(input("\nIntroduce el expediente del Alumno a modificar: "))

		try:
			alumno = Modelo.Alumno.get_by_id(opt)
			done = False		# Variable 'bool' que determina si se ha terminado de modificar un solo alumno
			while not done:
				print("\n1.- Modificar Nombre\n2.- Modificar Apellidos\n3.- Modificar Telefono\n4.- Modificar Direccion\n5.- Modificar Fecha de Nacimiento\n6.- Modificar Todo\n\n0.- Salir")
				try:
					opt = validarInteger(input("\nSeleccione el campo a modificar: "))
					if opt == 1:
						print("\nHa seleccionado: Modificar Nombre\n")
						# Introducimos un nuevo nombre
						newName = validarString(str(input("\nIntroduce el nombre del Alumno: ")), 25, True)
						# Mostramos el alumno con los cambios realizados
						print(f"\nExpediente: {alumno.expedienteAlumn}\nNombre completo: {getFullName(newName, alumno.apellidosAlumn)}\nTelefono: {alumno.telefonoAlumn}\nDireccion: {alumno.direccionAlumn}\nFecha de nacimiento: {alumno.fechaAlumn.strftime('%d/%m/%Y')}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							# Actualizamos y guardamos todos los campos involucrados en la modificación
							alumno.nombreAlumn = newName
							alumno.nombre_completo = getFullName(newName, alumno.apellidosAlumn)
							alumno.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
					# Mantenemos la estructura de la primera opción, cambiando los datos involucrados
					elif opt == 2:
						print("\nHa seleccionado: Modificar Apellidos\n")
						newSurname = validarString(str(input("\nIntroduzca los nuevos apellidos: ")), 50, True)
						print(f"\nExpediente: {alumno.expedienteAlumn}\nNombre completo: {getFullName(alumno.nombreAlumn, newSurname)}\nTelefono: {alumno.telefonoAlumn}\nDireccion: {alumno.direccionAlumn}\nFecha de nacimiento: {alumno.fechaAlumn.strftime('%d/%m/%Y')}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							alumno.apellidosAlumn = newSurname
							alumno.nombre_completo = getFullName(alumno.nombreAlumn, newSurname)
							alumno.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 3:
						print("\nHa seleccionado: Modificar Telefono\n")
						newTel = validarInteger(input("\nIntroduzca el nuevo telefono: "))
						print(f"\nExpediente: {alumno.expedienteAlumn}\nNombre completo: {alumno.nombre_completo}\nTelefono: {newTel}\nDireccion: {alumno.direccionAlumn}\nFecha de nacimiento: {alumno.fechaAlumn.strftime('%d/%m/%Y')}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							alumno.telefonoAlumn = newTel
							alumno.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 4:
						print("\nHa seleccionado: Modificar Direccion\n")
						newDir = validarString(str(input("\nIntroduzca la nueva direccion: ")), 50, True)
						print(f"\nExpediente: {alumno.expedienteAlumn}\n\nNombre completo: {alumno.nombre_completo}\nTelefono: {alumno.telefonoAlumn}\nDireccion: {newDir}\nFecha de nacimiento: {alumno.fechaAlumn.strftime('%d/%m/%Y')}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							alumno.direccionAlumn = newDir
							alumno.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 5:
						print("\nHa seleccionado: Modificar Fecha de Nacimiento\n")
						newDate = validarDate(input("\nIntroduzca la nueva fecha de nacimiento: "))
						print(f"\nExpediente: {alumno.expedienteAlumn}\n\nNombre completo: {alumno.nombre_completo}\nTelefono: {alumno.telefonoAlumn}\nDireccion: {alumno.direccionAlumn}\nFecha de nacimiento: {newDate.strftime('%d/%m/%Y')}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							alumno.fechaAlumn = newDate
							alumno.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
					# La opción '6' auna todos los datos anteriormente utilizados
					elif opt == 6:
						print("\nHa seleccionado: Modificar Todo\n")
						newName = validarString(str(input("\nIntroduce el nombre del Alumno: ")), 25, True)
						newSurname = validarString(str(input("\nIntroduzca los nuevos apellidos: ")), 50, True)
						newTel = validarInteger(input("\nIntroduzca el nuevo telefono: "))
						newDir = validarString(str(input("\nIntroduzca la nueva direccion: ")), 50, True)
						newDate = validarDate(input("\nIntroduzca la nueva fecha de nacimiento: "))
						print(f"\nExpediente: {alumno.expedienteAlumn}\n\nNombre completo: {getFullName(newName, newSurname)}\nTelefono: {newTel}\nDireccion: {newDir}\nFecha de nacimiento: {newDate.strftime('%d/%m/%Y')}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							alumno.nombreAlumn = newName
							alumno.apellidosAlumn = newSurname
							alumno.nombre_completo = getFullName(newName, newSurname)
							alumno.telefonoAlumn = newTel
							alumno.direccionAlumn = newDir
							alumno.fechaAlumn = newDate
							alumno.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 0:							# Salimos del bucle y volvemos al menú anterior
						print("Modificación terminada")
						done = True 
					else:
						print("\nEntrada no valida\n")		# En caso de introducir un valor fuera de los recogidos
						
				except IntegrityError as error:				# En caso de redundancia en los datos, o cambios no permitidos (not null)
					print(f"\nOperacion Abortada\nSe ha producido un error de tipo: {error}")

		except DoesNotExist:								# En caso de que no exista el Alumno
			print(f"\nNo se ha encontrado ningun alumno con expediente '{opt}'")
		
		print("\n¿Desea modificar otro alumno? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a la busqueda de objetos Alumno presentes en la tabla 'alumno'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def searchAlumno(Modelo):
	finish = False
	while not finish:
		opt = validarInteger(input("\nIntroduce el expediente del Alumno a buscar: "))

		try:
			alumno = Modelo.Alumno.get_by_id(opt)

			# Realizamos una query para obtener el id del curso en el que está matriculado el alumno
			query = alumno.matriculas.select(Modelo.Matricula.id_Curso).execute()
			# con ese ID, creamos una lista con los nombres de los cursos
			nombre_cursos = [curso.id_Curso.nombreCurso for curso in query]
			
			# creamos una cadena con los nombres de los cursos separados por ', '. En caso de estar vacia la lista, retornamos "None"
			cursos_impartidos = ", ".join(nombre_cursos) if nombre_cursos else "None"

			print(f"Expediente: {alumno.expedienteAlumn}\n"
				f"Nombre Completo: {alumno.nombre_completo}\n"
				f"Telefono: {alumno.telefonoAlumn}\n"
				f"Direccion: {alumno.direccionAlumn}\n"
				f"Fecha de nacimiento: {alumno.fechaAlumn.strftime('%d/%m/%Y')}\n"
				f"Curso Matriculado: {cursos_impartidos}\n")
		except DoesNotExist:
			print(f"\nNo se ha encontrado ningun alumno con expediente '{opt}'")

		print("\n¿Desea buscar otro Alumno? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a mostrar todos los objetos Alumno presentes en la tabla 'alumno'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def showAlumnos(Modelo):
	for alumno in Modelo.Alumno.select():

		# Realizamos una query para obtener el ID del curso en el que está matriculado el alumno
		query = alumno.matriculas.select(Modelo.Matricula.id_Curso).execute()
		# con ese ID, creamos una lista con los nombres de los cursos
		nombre_cursos = [curso.id_Curso.nombreCurso for curso in query]

		# creamos una cadena con los nombres de los cursos separados por ', '. En caso de estar vacia la lista, retornamos "None"
		cursos_impartidos = ", ".join(nombre_cursos) if nombre_cursos else "None"

		print(f"Expediente: {alumno.expedienteAlumn}\n"
			f"Nombre Completo: {alumno.nombre_completo}\n"
			f"Telefono: {alumno.telefonoAlumn}\n"
			f"Direccion: {alumno.direccionAlumn}\n"
			f"Fecha de nacimiento: {alumno.fechaAlumn.strftime('%d/%m/%Y')}\n"
			f"Curso Matriculado: {cursos_impartidos}\n")


##############################################################
######     					Profesor     				######
##############################################################

# Método destinado a la creación de objetos Profesor y su inserción en su tabla de la BBDD
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
# Nótese que comparte la misma estructura que 'addAlumno'
def addProfesor(Modelo):
	finish = False
	while not finish: 		# Introducimos los datos de un objeto 'Alumno'
		nameProfe = validarString(str(input("\nIntroduce el nombre del Profesor: ")), 25, True)
		surnameProfe = validarString(str(input("\nIntroduce los apellidos del Profesor: ")), 50, True)
		telProfe = validarInteger(input("\nIntroduce el telefono del Profesor: "))
		dirProfe = validarString(str(input("\nIntroduce la dirección del Profesor: ")), 50, True)
		dniProfe = validarDNI(input("\nIntroduce el DNI del Profesor: "))

		print(f"\nNombre completo: {getFullName(nameProfe, surnameProfe)}\nTelefono: {telProfe}\nDireccion: {dirProfe}\nDNI: {dniProfe}")
		print("\n¿Desea guardar al Profesor? (S/N)")
		confirm = confirmarOperacion()
		if confirm:
			try:
				Modelo.Profesor.create(nombreProfe = nameProfe, apellidosProfe = surnameProfe, nombre_completo = getFullName(nameProfe, surnameProfe), telefonoProfe = telProfe, direccionProfe = dirProfe, dniProfe = dniProfe)
				print("\nAlumno guardado correctamente")
			except IntegrityError as error:
				print(f"\nOperacion Abortada\nSe ha producido un error de tipo: {error}")
		else:
			print("\nOperacion cancelada")
		
		print("\n¿Desea añadir otro profesor? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a la eliminación de objetos Alumno de la tabla 'alumno'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
# Nótese que comparte la misma estructura que 'removeAlumnos'
def removeProfesor(Modelo):
	finish = False
	while not finish:
		showProfesores(Modelo)			# Mostramos el listado de Profesores
		opt = validarInteger(input("\nIntroduce el ID del Profesor a eliminar: "))

		try:
			profe = Modelo.Profesor.get_by_id(opt)
			print("\n¿Seguro que desea eliminar este profesor? (S/N)")
			confirm = confirmarOperacion()
			if confirm:
				profe.delete_instance()
				print("\nProfesor eliminado correctamente")
			else:
				print("\nOperacion cancelada")
		except DoesNotExist:
			print(f"\nNo se ha encontrado ningun profesor con ID '{opt}'")
		
		print("\n¿Desea eliminar otro profesor? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a la modificacion de objetos Profesores de la tabla 'profesor'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
# Nótese que mantiene la estructura de 'modifyAlumno'
def modifyProfesor(Modelo):
	finish = False
	while not finish:
		showProfesores(Modelo)
		opt = validarInteger(input("\nIntroduce el ID del Profesor a modificar: "))

		try:
			profe = Modelo.Profesor.get_by_id(opt)
			done = False
			while not done:
				print("\n1.- Modificar Nombre\n2.- Modificar Apellidos\n3.- Modificar Telefono\n4.- Modificar Direccion\n5.- Modificar DNI\n6.- Modificar Todo\n\n0.- Salir")
				try:
					opt = validarInteger(input("\nSeleccione el campo a modificar: "))
					if opt == 1:
						print("\nHa seleccionado: Modificar Nombre\n")
						newName = validarString(str(input("\nIntroduce el nuevo nombre: ")), 25, True)
						print(f"\nID: {profe.idProfe}\nNombre Completo: {getFullName(newName, profe.apellidosProfe)}\nTelefono: {profe.telefonoProfe}\nDireccion: {profe.direccionProfe}\nDNI: {profe.dniProfe}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							profe.nombreProfe = newName
							profe.nombre_completo = getFullName(newName, profe.apellidosProfe)
							profe.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")

					elif opt == 2:
						print("\nHa seleccionado: Modificar Apellidos\n")
						newSurname = validarString(str(input("\nIntroduzca los nuevos apellidos: ")), 50, True)
						print(f"\nID: {profe.idProfe}\nNombre Completo: {getFullName(profe.nombreProfe, newSurname)}\nTelefono: {profe.telefonoProfe}\nDireccion: {profe.direccionProfe}\nDNI: {profe.dniProfe}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							profe.apellidosProfe = newSurname
							profe.nombre_completo = getFullName(profe.nombreProfe, newSurname)
							profe.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 3:
						print("\nHa seleccionado: Modificar Telefono\n")
						newTel = validarInteger(input("\nIntroduzca el nuevo telefono: "))
						print(f"\nID: {profe.idProfe}\nNombre Completo: {profe.nombre_completo}\nTelefono: {newTel}\nDireccion: {profe.direccionProfe}\nDNI: {profe.dniProfe}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							profe.telefonoProfe = newTel
							profe.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 4:
						print("\nHa seleccionado: Modificar Direccion\n")
						newDir = validarString(str(input("\nIntroduzca la nueva direccion: ")), 50, True)
						print(f"\nID: {profe.idProfe}\nNombre Completo: {profe.nombre_completo}\nTelefono: {profe.telefonoProfe}\nDireccion: {newDir}\nDNI: {profe.dniProfe}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							profe.direccionProfe = newDir
							profe.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 5:
						print("\nHa seleccionado: Modificar DNI\n")
						newDNI = validarDNI(input("\nIntroduzca el nuevo DNI: "))
						print(f"\nID: {profe.idProfe}\nNombre Completo: {profe.nombre_completo}\nTelefono: {profe.telefonoProfe}\nDireccion: {profe.direccionProfe}\nDNI: {newDNI}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							profe.dniProfe = newDNI
							profe.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 6:
						print("\nHa seleccionado: Modificar Todo\n")
						newName = validarString(str(input("\nIntroduce el nuevo nombre: ")), 25, True)
						newSurname = validarString(str(input("\nIntroduzca los nuevos apellidos: ")), 50, True)
						newTel = validarInteger(input("\nIntroduzca el nuevo telefono: "))
						newDir = validarString(str(input("\nIntroduzca la nueva direccion: ")), 50, True)
						newDNI = validarDNI(input("\nIntroduzca el nuevo DNI: "))
						print(f"\nID: {profe.idProfe}\nNombre Completo: {getFullName(newName, newSurname)}\nTelefono: {newTel}\nDireccion: {newDir}\nDNI: {newDNI}\n")
						print("\n¿Confirmar cambios? (S/N)")
						confirm = confirmarOperacion()
						if confirm:
							profe.nombreProfe = newName
							profe.apellidosProfe = newSurname
							profe.nombre_completo = getFullName(newName, newSurname)
							profe.telefonoProfe = newTel
							profe.direccionProfe = newDir
							profe.dniProfe = newDNI
							profe.save()
							print("\nCambio guardado correctamente")
						else:
							print("\nOperacion cancelada")
						
					elif opt == 0:							# Salimos del bucle y volvemos al menú anterior
						print("Modificación terminada")
						done = True 
					else:
						print("\nEntrada no valida\n")			# En caso de introducir un valor fuera de los recogidos
				except IntegrityError as error:
					print(f"\nOperacion Abortada\nSe ha producido un error de tipo: {error}")
		except DoesNotExist:
			print(f"\nNo se ha encontrado ningun Profesor con ID '{opt}'")
		
		print("\n¿Desea modificar otro Profesor? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a la busqueda de objetos Profesor de la tabla 'profesor'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
# Nótese que conserva la misma estructura que 'searchAlumno'
def searchProfesor(Modelo):
	finish = False
	while not finish:
		opt = validarInteger(input("\nIntroduce el ID del Profesor a buscar: "))

		try:
			profe = Modelo.Profesor.get_by_id(opt)

			# Realizamos una query para obtener el nombre del curso en el que está asiganado el profesor
			query = profe.cursos.select(Modelo.Curso.nombreCurso).execute()
			# creamos una lista con los nombres de los cursos
			nombre_cursos = [curso.nombreCurso for curso in query]

			# creamos una cadena con los nombres de los cursos separados por ', '. En caso de estar vacia la lista, retornamos "None"
			cursos_impartidos = ", ".join(nombre_cursos) if nombre_cursos else "None"

			print(f"ID: {profe.idProfe}\n"
				f"Nombre Completo: {profe.nombre_completo}\n"
				f"Telefono: {profe.telefonoProfe}\n"
				f"Direccion: {profe.direccionProfe}\n"
				f"DNI: {profe.dniProfe}\n"
				f"Cursos impartido: {cursos_impartidos}\n")

		except DoesNotExist:
			print(f"\nNo se ha encontrado ningun profesor con ID '{opt}'")

		print("\n¿Desea buscar otro profesor? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a mostrar todos los objetos Profesor presentes en la tabla 'profesor'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
# Nótese que conserva la misma estructura que 'showAlumnos'
def showProfesores(Modelo):
	for profe in Modelo.Profesor.select():
		# Realizamos una query para obtener el nombre del curso en el que está asiganado el profesor
		query = profe.cursos.select(Modelo.Curso.nombreCurso).execute()
		# creamos una lista con los nombres de los cursos
		nombre_cursos = [curso.nombreCurso for curso in query]

		# creamos una cadena con los nombres de los cursos separados por ', '. En caso de estar vacia la lista, retornamos "None"
		cursos_impartidos = ", ".join(nombre_cursos) if nombre_cursos else "None"

		print(f"ID: {profe.idProfe}\n"
			f"Nombre Completo: {profe.nombre_completo}\n"
			f"Telefono: {profe.telefonoProfe}\n"
			f"Direccion: {profe.direccionProfe}\n"
			f"DNI: {profe.dniProfe}\n"
			f"Cursos impartido: {cursos_impartidos}\n")


##############################################################
######     					Curso     					######
##############################################################

# Método destinado a asignar profesores al campo perteneciente de la tabla 'Curso' (Curso.id_Profesor)
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def assignProfesor(Modelo):
	finish = False
	while not finish:
		showProfesores(Modelo)						# Mostramos el listado de profesores
		opt = validarInteger(input("\nIntroduce el ID del Profesor a Asignar: "))

		try:
			profe = Modelo.Profesor.get_by_id(opt)	# Seleccionamos el profesor
			showCursos(Modelo)						# Mostramos el listado de cursos
			opt = validarInteger(input("\nIntroduce el ID del Curso impartido: "))
			curso = Modelo.Curso.get_by_id(opt)		# Seleccionamos el Curso
			# Mostramos por pantalla Profesor y Curso
			print(f"\nID: {profe.idProfe}\nNombre completo: {profe.nombre_completo}\nTelefono: {profe.telefonoProfe}\nDireccion: {profe.direccionProfe}\nDNI: {profe.dniProfe}")
			print(f"\nID: {curso.idCurso}\nNombre: {curso.nombreCurso}\nDescripcion: {curso.descripcionCurso}\nProfesor: {curso.id_Profesor}")
			print("\n¿Confirmar asignación? (S/N)")
			confirm = confirmarOperacion()
			if confirm:
				# Asignamos al ID del profesor que imparte el curso, el valor del Profesor designado para dicha tarea
				curso.id_Profesor = profe.idProfe
				curso.save()
				print("\nProfesor asignado correctamente")
			else:
				print("\nOperacion cancelada")

		except DoesNotExist:
			print(f"\nOperación Abortada\nNo se ha encontrado ningun profesor/curso con el ID proporcionado")

		print("\n¿Desea asignar a otro profesor? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a matricular alumnos al campo perteneciente de la tabla 'Matriculas' (Curso.id_Profesor)
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def enrollAlumno(Modelo):
	finish = False
	while not finish:
		showAlumnos(Modelo)						# Mostramos el listado de alumnos
		opt = validarInteger(input("\nIntroduce el ID del Alumno a Matricular: "))

		try:
			alumno = Modelo.Alumno.get_by_id(opt)	# Seleccionamos el alumno
			showCursos(Modelo)						# Mostramos el listado de cursos
			opt = validarInteger(input("\nIntroduce el ID del Curso asignado: "))
			curso = Modelo.Curso.get_by_id(opt)		# Seleccionamos el Curso
			if curso.id_Profesor is not None:		# Estructura 'if' para controlar que el curso tiene un profesor asignado
				# Mostramos por pantalla Alumno y Curso
				print(f"\nExpediente: {alumno.expedienteAlumn}\nNombre completo: {alumno.nombre_completo}\nTelefono: {alumno.telefonoAlumn}\nDireccion: {alumno.direccionAlumn}\nFecha de nacimiento: {alumno.fechaAlumn.strftime('%d/%m/%Y')}")
				print(f"\nID: {curso.idCurso}\nNombre: {curso.nombreCurso}\nDescripcion: {curso.descripcionCurso}\nProfesor: {curso.id_Profesor}")
				print("\n¿Confirmar asignación? (S/N)")
				confirm = confirmarOperacion()
				if confirm:
					# Creamos una entrada en la tabla Matricula, adjuntando el expediente del Alumno y el ID del curso en el que está matriculado
					Modelo.Matricula.create(id_Alumno = alumno.expedienteAlumn, id_Curso = curso.idCurso)
					print("\nAlumno matriculado correctamente")
				else:
					print("\nOperacion cancelada")
			else:
				print("\nNo se admiten matriculaciones hasta que exista un profesor asignado al curso")

		except DoesNotExist:
			print(f"\nOperación Abortada\nNo se ha encontrado ningun alumno/curso con el ID proporcionado")

		print("\n¿Desea matricular otro alumno? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a la busqueda de objetos Profesor de la tabla 'profesor'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def searchCurso(Modelo):
	finish = False
	while not finish:
		opt = validarInteger(input("\nIntroduce el ID del Curso a buscar: "))

		try:
			curso = Modelo.Curso.get_by_id(opt)
			# Realizamos una query para obtener el id del alumno matriculado en el curso seleccionado
			query = curso.matriculas.select(Modelo.Matricula.id_Alumno).execute()
			# conociendo el ID del alumno matriculado, creamos una lista con los nombres de los alumnos
			nombre_alumnos = [matricula.id_Alumno.nombre_completo for matricula in query]

			# creamos una cadena con el nombre del profesor. En caso de estar vacia la lista, retornamos "None"
			prof_nomCompleto = curso.id_Profesor.nombre_completo if curso.id_Profesor else "None"

			# creamos una cadena con los nombres de los alumnos separados por ', '. En caso de estar vacia la lista, retornamos "None"
			alumnos_matriculados = ", ".join(nombre_alumnos) if nombre_alumnos else "None"

			print(f"ID: {curso.idCurso}\n"
				f"Nombre: {curso.nombreCurso}\n"
				f"Descripcion: {curso.descripcionCurso}\n"
				f"Profesor: {prof_nomCompleto}\n"
				f"Alumnado: {alumnos_matriculados}\n")

		except DoesNotExist:
			print(f"\nNo se ha encontrado ningun Curso con ID '{opt}'")

		print("\n¿Desea buscar otro Curso? (S/N)")
		confirm = confirmarOperacion()
		if not confirm:
			finish = True

# Método destinado a mostrar todos los objetos Curso presentes en la tabla 'Curso'
#	@param 'Modelo': Instancia de la clase 'Modelo_ORM', en la que están definidas las clases de la BBDD.
def showCursos(Modelo):
	for curso in Modelo.Curso.select():
		# Realizamos una query para obtener el id del alumno matriculado en el curso seleccionado
		query = curso.matriculas.select(Modelo.Matricula.id_Alumno).execute()
		# conociendo el ID del alumno matriculado, creamos una lista con los nombres de los alumnos
		nombre_alumnos = [matricula.id_Alumno.nombre_completo for matricula in query]

		# creamos una cadena con el nombre del profesor. En caso de estar vacia la lista, retornamos "None"
		prof_nomCompleto = curso.id_Profesor.nombre_completo if curso.id_Profesor else "None"

		# creamos una cadena con los nombres de los alumnos separados por ', '. En caso de estar vacia la lista, retornamos "None"
		alumnos_matriculados = ", ".join(nombre_alumnos) if nombre_alumnos else "None"

		print(f"ID: {curso.idCurso}\n"
			f"Nombre: {curso.nombreCurso}\n"
			f"Descripcion: {curso.descripcionCurso}\n"
			f"Profesor: {prof_nomCompleto}\n"
			f"Alumnado: {alumnos_matriculados}\n")


##############################################################
######     					Menús     					######
##############################################################


# Método que muestra por pantalla el menú y llama a las opciones referentes a la clase 'Alumno'
# Nótese que todos los menús ('Alumno', 'Profesor', 'Curso' y 'Principal') comparten la misma estructura
def submenuAlumno():
	finish = False			# Variable de tipo 'bool' que determina el fin del bucle
	while not finish:			# Bucle para mantenernos dentro del menu en caso de introducir un dato erroneo
		print("\n","-"*40," Menú Alumno ","-"*40)
		print("\nSeleccione una opcion: \n\n1.- Nuevo Alumno\n2.- Eliminar Alumno\n3.- Modificar Alumno\n4.- Buscar Alumno\n5.- Mostrar Alumnos\n\n0.- Atras")
		
		opt = validarInteger(input())				# Introducimos y validamos la opcion deseada
		if opt == 1:
			print("\nHa seleccionado: Nuevo Alumno\n")
			addAlumno(Modelo)
		elif opt == 2:
			print("\nHa seleccionado: Eliminar Alumno\n")
			removeAlumno(Modelo)
		elif opt == 3:
			print("\nHa seleccionado: Modificar Alumno\n")
			modifyAlumno(Modelo)
		elif opt == 4:
			print("\nHa seleccionado: Buscar Alumno\n")
			searchAlumno(Modelo)
		elif opt == 5:
			print("\nHa seleccionado: Mostrar Alumnos\n")
			showAlumnos(Modelo)
		elif opt == 0:								# Salimos del bucle y volvemos al menú anterior
			finish = True 
		else:
			print("\nEntrada no valida\n")			# En caso de introducir un valor fuera de los aceptados/esperados


# Método que muestra por pantalla el menú y llama a las opciones referentes a la clase 'Profesor'
def submenuProfesor():
	finish = False
	while not finish:
		print("\n","-"*40," Menú Profesor ","-"*40)
		print("\nSeleccione una opcion: \n\n1.- Nuevo Profesor\n2.- Eliminar Profesor\n3.- Modificar Profesor\n4.- Buscar Profesor\n5.- Mostrar Profesores\n\n0.- Atras")
		
		opt = validarInteger(input())
		if opt == 1:
			print("\nHa seleccionado: Nuevo Profesor\n")
			addProfesor(Modelo)
		elif opt == 2:
			print("\nHa seleccionado: Eliminar Profesor\n")
			removeProfesor(Modelo)
		elif opt == 3:
			print("\nHa seleccionado: Modificar Profesor\n")
			modifyProfesor(Modelo)
		elif opt == 4:
			print("\nHa seleccionado: Buscar Profesor\n")
			searchProfesor(Modelo)
		elif opt == 5:
			print("\nHa seleccionado: Mostrar Profesores\n")
			showProfesores(Modelo)
		elif opt == 0:
			finish = True 
		else:
			print("\nEntrada no valida\n")


# Método que muestra por pantalla el menú y llama a las opciones referentes a la clase 'Curso'
def submenuCurso():
	finish = False
	while not finish:
		print("\n","-"*40," Menú Curso ","-"*40)
		print("\nSeleccione una opcion: \n\n1.- Asignar Profesor\n2.- Matricular Alumno\n3.- Buscar Curso\n4.- Mostrar Cursos\n\n0.- Atras")
		
		opt = validarInteger(input())
		if opt == 1:
			print("\nHa seleccionado: Asignar Profesor\n")
			assignProfesor(Modelo)
		elif opt == 2:
			print("\nHa seleccionado: Matricular Alumno\n")
			enrollAlumno(Modelo)
		elif opt == 3:
			print("\nHa seleccionado: Buscar Curso\n")
			searchCurso(Modelo)
		elif opt == 4:
			print("\nHa seleccionado: Mostrar Cursos\n")
			showCursos(Modelo)
		elif opt == 0:
			finish = True 
		else:
			print("\nEntrada no valida\n")


# Método que muestra por pantalla el menú principal del programa, desde el cuál se accede al resto de menús
def mainMenu():
	finish = False
	print("\n","*"*40," Centro Formación ","*"*40)
	while not finish:
		print("\n","-"*40," Menu Principal ","-"*40)
		print("\nSeleccione una opcion: \n\n1.- Alumnos\n2.- Profesores\n3.- Cursos\n\n0.- Salir")
		
		opt = validarInteger(input())
		if opt == 1:
			submenuAlumno()
		elif opt == 2:
			submenuProfesor()
		elif opt == 3:
			submenuCurso()
		elif opt == 0:
			print("\n¿Seguro que quiere cerrar el programa? (S/N) :\n")
			confirmacion = confirmarOperacion()							# Pedimos confirmación antes de cerrar el programa
			if confirmacion:
				print("\nHasta la vista\n")
				finish = True
				sys.exit(0)			# Provocamos el cierre del programa, utilizando el argumento '0' para indicar que la salida NO es forzada o causada por un error.
		else:
			print("\nEntrada no valida\n")


conn = Modelo.conectarDB()
#Modelo.iniciarLogger(conn)
Modelo.createTables(conn)
Modelo.addCursos(conn)
mainMenu()
