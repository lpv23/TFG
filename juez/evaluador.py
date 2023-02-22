from os import scandir


# Inspeccionar el contenido de la carpeta "problemas" y devolver una lista con los nombres de las subcarpetas
def lista_problemas():
    dirlist = []
    with scandir('C:\\Users\\laura\\PycharmProjects\\TFG\\problemas') as dir:
        for file in dir:
            if file.is_dir():
                dirlist.append(file.name)
    return dirlist


print(lista_problemas())


# Lee los datos del problemas de la carpeta "id", que se encuentra dentro de la carpeta "problemas"
# Devuelve un diccionario con las siguientes claves:
# 'id': nombre de la carpeta, pasado como parámetro -- 'menor
# 'title': primera línea de problema.txt -- 'Encuentra el menor elemento'
# 'body': segunda línea de problema.txt -- 'Encuentra el menor elemento en una lista que no está ordenada y devuélvelo'
# 'funcion': nombre de la función que el usuario tiene que crear (tercera línea de problema.txt) -- 'menor'
def lee_problema(id):
    problemas = lista_problemas()
    for pr in problemas:
        if id == pr:
            path = 'C:\\Users\\laura\\PycharmProjects\\TFG\\problemas\\' + id + '\\problema.txt'
            with open(path, 'r') as fichero:
                lineas = fichero.read().split('\n')[:3]
            return {'id': pr,
                    'title': lineas[0],
                    'body': lineas[1],
                    'funcion': lineas[2]}
    return {}


print(lee_problema('alfabetica'))


# - Leer el fichero cuya ruta es "fichero" y es la definición de una función en Python,
# cuyo nombre viene definido por la clave 'funcion' del diccionario lee_problema(id)
# - Ejecutar la función con cada uno de los ficheros de prueba que hay en el directorio del problema
# - Comprobar si la salida coincide con la esperada
# - Devolver una cadena, que contenga en cada línea el resultado de cada prueba. Si la prueba es correcta,
# el contenido será OK y su tiempo de ejecución. Si la prueba es incorrecta, el contenido es: entrada, salida obtenida, salida espera.
#
# Los ficheros xxxxxxx.entrada.txt contienen un parámetro de entrada en cada línea
# Los ficheros xxxxxxx.salida.txt contienen la salida esperada en la primera línea
def evalua_problema(id, fichero):
    path = 'C:\\Users\\laura\\PycharmProjects\\TFG\\problemas\\' + id + '\\' + fichero + '.txt'
    dic = lee_problema(id)

    return "Resultado de la evaluación"
