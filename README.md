# Práctica Peewee

## Tabla de contenidos
- [Práctica Peewee](#práctica-peewee)
  - [Tabla de contenidos](#tabla-de-contenidos)
  - [Descripción](#descripción)
  - [Configuración](#configuración)
  - [Anotaciones](#anotaciones)

## Descripción
En este documento tratamos de esclarecer los módulos necesarios para el correcto funcionamiento de nuestra aplicación.

</br>

## Configuración
La configuración a la base de datos se encuentra presente en el fichero **'config.json'** en la carpeta del proyecto, con la siguiente disposición:

```json
{
        "host": "localhost",
        "user": "root",
        "password": "",
        "port": "3306",
        "database": "CentroFormacion_ORM"
}
```

Desde aquí, extraeremos la información necesaria para instanciar la conexión a nuestra base de datos, de manera que dichos datos **no estén presentes de manera explícita** en nuestro código, incrementando de esta manera la seguridad de éste.

</br>

## Anotaciones
Se han omitido algunos comentarios en el código en aquellas estructuras de control o métodos que conservan un formato/estructura muy similar, comentando la primera aparición, pero no las siguientes, reduciendo así una posible 'aglomeración' de palabras en pantalla. (Ejemplo: Menús).

</br>

Se ha introducido el uso de **'exit()'**, perteneciente al módulo **'sys'** al finalizar el programa. De esta manera nos aseguramos que el programa no pueda permanecer en ejecución al simplemente cerrar el bucle del menú principal (como anteriormente se indicó en una corrección de una práctica anterior).

