import os.path
import string
import time
from os import scandir
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy

sufijo_entrada = "entrada.txt"
sufijo_salida = "salida.txt"
# carpeta_problemas = "problemas"
carpeta_problemas = "C:\\Users\\laura\\PycharmProjects\\TFG\\problemas"


# Inspeccionar el contenido de la carpeta "problemas" y devolver una lista con los nombres de las subcarpetas
def lista_problemas():
    carpetas = []
    with scandir(carpeta_problemas) as problemas:
        for file in problemas:
            if file.is_dir():
                carpetas.append(file.name)
    return carpetas


# print(lista_problemas())


# Lee los datos del problema de la carpeta "id", que se encuentra dentro de la carpeta "problemas"
# Devuelve un diccionario con las siguientes claves:
# 'id': nombre de la carpeta, pasado como parámetro -- 'menor'
# 'title': primera línea de problema.txt -- 'Encuentra el menor elemento'
# 'body': segunda línea de problema.txt -- 'Encuentra el menor elemento en una lista que no está ordenada y devuélvelo'
# 'funcion': nombre de la función que el usuario tiene que crear (tercera línea de problema.txt) -- 'menor'
# 'aumentar': cuarta línea - n.º del parámetro que debe aumentar su tamaño (si es 0, es que no hay nada que aumentar)
# 'tipo_param': a partir de la línea 5 - tipo de cada parámetro (uno en cada línea)
# (con un espacio para indicar el tipo dentro de una tupla o lista) (añadir sorted si está ordenada)
def lee_problema(id):
    problemas = lista_problemas()
    for pr in problemas:
        if id == pr:
            path = os.path.join(carpeta_problemas, id, "problema.txt")
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


# Devuelve una entrada aleatoria del tipo indicado y de tamaño n
def entrada_aleatoria(tipo, n):
    if tipo == 'str':  # string de letras minúsculas - ¿Añado mayúsculas?
        return '"' + ''.join(random.choice(string.ascii_lowercase) for _ in range(n)) + '"'
    elif tipo == 'int':
        return str(random.randint(10 ** (n - 1), (10 ** n) - 1))
    elif tipo.startswith('list'):
        resultado = []
        if tipo.removeprefix('list ').startswith('str'):
            for _ in range(n):  # str de 10 letras minúsculas
                resultado.append('"' + ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + '"')
        elif tipo.removeprefix('list ').startswith('int'):
            for _ in range(n):  # int entre 0 y 100
                resultado.append(str(random.randint(0, 100)))
        if tipo.endswith('sorted'):
            resultado.sort()
        return '[' + ', '.join(resultado) + ']'
    elif tipo.startswith('tuple'):
        resultado = []
        if tipo.removeprefix('tuple ').startswith('str'):
            for _ in range(n):  # str de 10 letras minúsculas
                resultado.append('"' + ''.join(random.choice(string.ascii_lowercase) for _ in range(10)) + '"')
        elif tipo.removeprefix('tuple ').startswith('int'):
            for _ in range(n):  # int entre 0 y 100
                resultado.append(str(random.randint(0, 100)))
        return '(' + ', '.join(resultado) + ')'
    return ''


# Evalúa la función con entradas cada vez más grandes
def tiempo_complejidad(dic_problema, fichero, tams_entrada):
    # leo la función
    with open(fichero, 'r') as fichero:
        exec(fichero.read())
    funcion = dic_problema['funcion']
    aumentar = int(dic_problema['aumentar'])
    tipo_entrada = dic_problema['tipo_param']

    tams = [0]  # ¿debería inicializar con el tamaño de entrada de la prueba?
    tiempos = [0.]  # ¿debería calcular el tiempo con tamaño 0 o inicializar con el tiempo de la prueba?

    while tiempos[-1] < 0.1 and tams[-1] < 500:  # ¿Cuándo paro?
        print('sigo', tams[-1], tiempos[-1])
        # aumento tamaño del parametro que toca - ¿siempre es el mismo aumento?
        if aumentar != 0:
            tams_entrada[aumentar - 1] = tams[-1] + 5
            tams.append(tams_entrada[aumentar - 1])
        # evaluo 10 veces con ese tamaño
        tiempo_pruebas = []
        for _ in range(10):
            # creo otra prueba aleatoria
            entrada = []
            for i in range(len(tipo_entrada)):
                entrada.append(entrada_aleatoria(tipo_entrada[i], tams_entrada[i]))
            # evaluo
            entrada_str = ', '.join(entrada)
            tiempoini = time.perf_counter()
            eval(funcion + '(' + entrada_str + ')')
            tiempo_pruebas.append(time.perf_counter() - tiempoini)

        tiempos.append(sum(tiempo_pruebas) / 10)

    return tams, tiempos


# Familias de funciones para el orden de complejidad
def constante(x, a):
    return a


def lineal(x, a, b):
    return a + b * x


def cuadratica(x, a, b):
    return a + b * x ** 2


def polinomial(x, a, b, c):
    return a + b * x ** c


def linearlogaritmica(x, a):
    return a * x * np.log1p(x)


def logaritmica(x, a, b):
    return a + b * np.log1p(x)


funciones = (constante, lineal, cuadratica, polinomial, logaritmica, linearlogaritmica)


# Comprueba qué función de las familias de funciones es más próxima a los datos tamaño-tiempo que tenemos
def funcion_complejidad(x, y, funcs=funciones):
    x, y = np.array(x), np.array(y)
    valores_opt = []
    residuos = []
    for f in funcs:
        popt = scipy.optimize.curve_fit(f, x, y)[0]
        valores_opt.append(popt)
        # print('popt ', popt)
        residuos.append(sum(abs(y - f(x, *popt))))
    res_min = np.min(np.array(residuos))
    print(residuos)
    pos_min = residuos.index(res_min)
    fun_min = funcs[pos_min]
    val_min = valores_opt[pos_min]
    print('min', fun_min, val_min)
    return fun_min, val_min, res_min


# Pinta la gráfica de tamaño-tiempo junto con la función aproximada
def pinta_grafica(tams, tiempos):
    f, params, res = funcion_complejidad(tams, tiempos)
    plt.plot(tams, tiempos, '.-')
    ftams = f(np.array(tams), *params)
    plt.plot(tams, ftams, '--')
    plt.savefig('grafica.png')
    plt.show()


# - Leer el fichero cuya ruta es "fichero" y es la definición de una función en Python,
# cuyo nombre viene definido por la clave 'funcion' del diccionario lee_problema(id)
# - Ejecutar la función con cada uno de los ficheros de prueba que hay en el directorio del problema
# - Comprobar si la salida coincide con la esperada
# - Devolver una lista que contenga cadenas con el resultado de cada prueba.
# (Si la prueba es correcta, el contenido será OK y su tiempo de ejecución.) (Y la gráfica tiempo-tamaño de entrada)
# (Si la prueba es incorrecta, el contenido es: entrada, salida obtenida, salida esperada.)
#
# Los ficheros xxxxxxx.entrada.txt contienen un parámetro de entrada en cada línea
# Los ficheros xxxxxxx.salida.txt contienen la salida esperada en la primera línea
def evalua_problema(id, fichero):
    dic_problema = lee_problema(id)
    funcion = dic_problema['funcion']
    with open(fichero, 'r') as fich:
        exec(fich.read())
    pruebas, resultados = [], []
    with scandir(os.path.join(carpeta_problemas, id)) as carpeta:
        for file in carpeta:
            if file.is_file() and file.name.endswith(sufijo_entrada):
                pruebas.append((file.path, file.path[:-len(sufijo_entrada)] + sufijo_salida))
    for prueba in pruebas:
        with open(prueba[0], 'r') as e:
            entrada = e.read().split('\n')
            # Quitamos el argumento vacío que surge si hay una línea vacía al final
            if entrada[-1] == '' and len(entrada) > len(dic_problema['tipo_param']):
                entrada = entrada[:-1]
            entrada_str = ', '.join(entrada)
            tiempoini = time.perf_counter()
            salidareal = eval(funcion + '(' + entrada_str + ')')
            tiempototal = time.perf_counter() - tiempoini
        with open(prueba[1], 'r') as s:
            salidaesperada = eval(s.read())
        if salidareal == salidaesperada:
            resultados.append('OK' + ', ' + str(tiempototal))
            # calculo los tamaños de entrada - ¿solo lo necesito si algún valor se queda fijo?
            tams_entrada = []
            for i in range(len(entrada)):
                print(entrada)
                tipo = dic_problema['tipo_param'][i]
                if tipo in ['str', 'int']:
                    tams_entrada.append(len(entrada[i]))
                elif tipo == 'float':
                    parte_entera, parte_decimal = entrada[i].split('.')
                    tams_entrada.append([len(parte_entera), len(parte_decimal)])
                elif tipo.startswith('list') or tipo.startswith('tuple'):
                    tams_entrada.append([len(eval(entrada[i])), len(str(eval(entrada[i])[0]))])
            # calculo el tiempo para entradas cada vez mayores - ¿y si aumentar == 0?
            print(tams_entrada)
            tams, tiempos = tiempo_complejidad(dic_problema, fichero, tams_entrada)
            pinta_grafica(tams, tiempos)
        else:
            resultados.append('(' + entrada_str + ')' + ', ' + str(salidaesperada) + ', ' + str(salidareal))
    return resultados


# print(evalua_problema('alfabetica', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-alfabetica.py'))
# print(evalua_problema('menorque', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-menorque.py'))
# evalua_problema('ordenar', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-ordenar-sort.py')
# evalua_problema('buscar', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-buscar-unoauno-inefi.py')
# evalua_problema('palindromo', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-palindromo-inefi.py')