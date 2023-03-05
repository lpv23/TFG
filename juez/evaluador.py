import os.path
import time
from os import scandir

sufijo_entrada = "entrada.txt"
sufijo_salida = "salida.txt"
carpeta_problemas = "problemas"


# Inspeccionar el contenido de la carpeta "problemas" y devolver una lista con los nombres de las subcarpetas
def lista_problemas():
    carpetas = []
    with scandir(carpeta_problemas) as problemas:
        for file in problemas:
            if file.is_dir():
                carpetas.append(file.name)
    return carpetas


# print(lista_problemas())


# Lee los datos del problemas de la carpeta "id", que se encuentra dentro de la carpeta "problemas"
# Devuelve un diccionario con las siguientes claves:
# 'id': nombre de la carpeta, pasado como parámetro -- 'menor'
# 'title': primera línea de problema.txt -- 'Encuentra el menor elemento'
# 'body': segunda línea de problema.txt -- 'Encuentra el menor elemento en una lista que no está ordenada y devuélvelo'
# 'funcion': nombre de la función que el usuario tiene que crear (tercera línea de problema.txt) -- 'menor'
# 'aumentar': cuarta linea - nº del parámetro que debe aumentar su tamaño (si es 0, es que no hay nada que aumentar)
# 'tipo_param': a partir de la linea 5 - tipo de cada parámetro (uno en cada línea)
# (con un espacio para indicar el tipo dentro de una tupla o lista) (añadir sorted si está ordenada)
def lee_problema(id):
    problemas = lista_problemas()
    for pr in problemas:
        if id == pr:
            path = os.path.join(carpeta_problemas, id, "problema.txt")
            print(path)
            with open(path, 'r') as fichero:
                lineas = fichero.read().split('\n')
            if len(lineas) >= 5:
                return {'id': pr,
                        'title': lineas[0],
                        'body': lineas[1],
                        'funcion': lineas[2],
                        'aumentar': lineas[3],
                        'tipo_param': lineas[4:]}
    return {}


# print(lee_problema('alfabetica'))


# - Leer el fichero cuya ruta es "fichero" y es la definición de una función en Python,
# cuyo nombre viene definido por la clave 'funcion' del diccionario lee_problema(id)
# - Ejecutar la función con cada uno de los ficheros de prueba que hay en el directorio del problema
# - Comprobar si la salida coincide con la esperada
# - Devolver una lista que contenga cadenas con el resultado de cada prueba.
# (Si la prueba es correcta, el contenido será OK y su tiempo de ejecución.)
# (Si la prueba es incorrecta, el contenido es: entrada, salida obtenida, salida esperada.)
#
# Los ficheros xxxxxxx.entrada.txt contienen un parámetro de entrada en cada línea
# Los ficheros xxxxxxx.salida.txt contienen la salida esperada en la primera línea
def evalua_problema(id, fichero):
    funcion = lee_problema(id)['funcion']
    with open(fichero, 'r') as fichero:
        exec(fichero.read())
    pruebas, resultados = [], []
    with scandir(os.path.join(carpeta_problemas, id)) as carpeta:
        for file in carpeta:
            if file.is_file() and file.name.endswith(sufijo_entrada):
                pruebas.append((file.path, file.path[:-len(sufijo_entrada)] + sufijo_salida))
    for prueba in pruebas:
        with open(prueba[0], 'r') as e:
            entrada = e.read().split('\n')
            if entrada[-1] == '':  # Quitamos el argumento vacío que surge si hay una línea vacía al final
                entrada = ', '.join(entrada[:-1])
            else:
                entrada = ', '.join(entrada)
            tiempoini = time.perf_counter()
            salidareal = eval(funcion + '(' + entrada + ')')
            tiempototal = time.perf_counter() - tiempoini
        with open(prueba[1], 'r') as s:
            salidaesperada = eval(s.read())
        if salidareal == salidaesperada:
            resultados.append('OK' + ', ' + str(tiempototal))
        else:
            resultados.append('(' + entrada + ')' + ', ' + str(salidaesperada) + ', ' + str(salidareal))
    return resultados

# print(evalua_problema('alfabetica', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-alfabetica.py'))
# print(evalua_problema('menorque', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-menorque.py'))
