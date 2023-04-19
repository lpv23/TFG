import os.path
import string
import time
from os import scandir
import random
import matplotlib.pyplot as plt
import numpy as np
import scipy
import sympy

sufijo_entrada = "entrada.txt"
sufijo_salida = "salida.txt"
carpeta_problemas = "problemas"
# carpeta_problemas = "C:\\Users\\laura\\PycharmProjects\\TFG\\problemas"

# VARIABLES GLOBALES
ejec_min = 50  # número de ejecuciones mínimas con tamaños diferentes
tiempo_total_max = 120  # tiempo total máximo del programa
# tiempo_extra = 120 # tiempo extra para calcular ptos intermedios si ha llegado al tiempo_total_max y no a las ejec_min
tiempo_max = 0.5  # tiempo máximo por ejecución
aumento_tam = 500  # aumento de tamaño
factor_aum = 10  # factor por el que se multiplica el aumento_tam si vemos que se queda muy constante
t_min_entre_ejec = 1e-3  # tiempo mínimo que debe haber entre ejecuciones para no considerarse constante
max_veces_cte = 4  # si se alcanza t_min_entre_ejec max_veces_cte, se calculan los puntos intermedios
pruebas_por_tam = 10  # pruebas que debe hacer por cada tamaño (con entradas diferentes)
residuo_max_t = 10  # si la aproximación tiene un residuo mayor, no aparece en la gráfica

ops_max = 5e6
ops_min_entre_ejec = 1000
residuo_max_oe = 5e7


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
    if tipo == 'str':  # string de letras minúsculas
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
    elif tipo == 'int':
        return random.randint(10 ** (n - 1), (10 ** n) - 1)
    elif tipo.startswith('list'):
        resultado = []
        if tipo.removeprefix('list ').startswith('str'):
            for _ in range(n):  # str de 10 letras minúsculas
                resultado.append(''.join(random.choice(string.ascii_lowercase) for _ in range(10)))
        elif tipo.removeprefix('list ').startswith('int'):
            for _ in range(n):  # int entre 0 y el doble del tamaño
                resultado.append(random.randint(0, n * 2))
        if tipo.endswith('sorted'):
            resultado.sort()
        elif tipo.endswith('reversed'):
            resultado.reverse()
        return resultado
    elif tipo.startswith('tuple'):
        resultado = []
        if tipo.removeprefix('tuple ').startswith('str'):
            for _ in range(n):  # str de 10 letras minúsculas
                resultado.append(''.join(random.choice(string.ascii_lowercase) for _ in range(10)))
        elif tipo.removeprefix('tuple ').startswith('int'):
            for _ in range(n):  # int entre 0 y el doble del tamaño
                resultado.append(random.randint(0, n * 2))
        return tuple(resultado)
    return ''


def contador_lineas(funcion):
    tab = '    '
    cont = 'contador_de_lineas_para_calcular_oe_complejidad'
    lista = funcion.split('\n')
    lista.insert(1, tab + 'global ' + cont)
    i = 2
    while i < len(lista):
        linea = lista[i]
        num_esp = 0
        for c in linea:
            if c == ' ':
                num_esp += 1
            else:
                break
        num_tabs = num_esp // 4
        linea = linea.lstrip()
        # No contamos la línea si está vacía ni si es un else ni si es un comentario
        # ¡¡De momento tampoco contamos los elif!!
        if linea == '' or linea.startswith('else:') or linea.startswith('elif ') or linea.startswith('#'):
            i += 1
        # Si es un while o for contamos una vez antes (para la vez que ya no entre, pero compruebe la condición)
        # y una vez después para que lo cuente cada vez que entra
        elif linea.startswith('while ') or linea.startswith('for '):
            lista.insert(i + 1, tab * (num_tabs + 1) + cont + ' += 1')
            lista.insert(i, tab * num_tabs + cont + ' += 1')
            i += 3
        else:
            lista.insert(i, tab * num_tabs + cont + ' += 1')
            i += 2
    print('\n'.join(lista))
    return '\n'.join(lista)


# Evalúa la función con entradas cada vez más grandes y guarda los tiempos y ¿líneas?
def evalua_complejidad_t(dic_problema, fichero, tams_entrada):
    global aumento_tam
    # leo la función
    with open(fichero, 'r') as fichero:
        exec(fichero.read())
    funcion = eval(dic_problema['funcion'])
    aumentar = int(dic_problema['aumentar'])
    tipo_entrada = dic_problema['tipo_param']

    # inicializo tamaños y tiempos
    tams = [1]
    if aumentar != 0:
        tams_entrada[aumentar - 1] = tams[-1]
    tiempos = []
    aum = 1
    veces_cte = 0  # se cuenta las que son seguidas
    tiempo_inicial = time.perf_counter()

    # evalúo la función con tamaños cada vez mayores y guardo el tiempo
    while tiempos == [] or (tiempos[-1] < tiempo_max and veces_cte < max_veces_cte):
        # aumento tamaño del parámetro que toca
        if len(tiempos) >= 2 and abs(tiempos[-1] - tiempos[-2]) < t_min_entre_ejec:
            aum *= factor_aum
            print('aumento', aum)
            veces_cte += 1
        else:
            veces_cte = 0

        if aumentar != 0 and tiempos != []:
            tams_entrada[aumentar - 1] = tams[-1] + aumento_tam * aum
            tams.append(tams_entrada[aumentar - 1])

        # evalúo pruebas_por_tam veces con ese tamaño
        tiempo_pruebas = []
        for _ in range(pruebas_por_tam):
            # creo otra prueba aleatoria
            entrada = []
            for i in range(len(tipo_entrada)):
                entrada.append(entrada_aleatoria(tipo_entrada[i], tams_entrada[i]))
            # evalúo y cuento el tiempo
            tiempoini = time.perf_counter()
            funcion(*entrada)
            tiempo_pruebas.append(time.perf_counter() - tiempoini)
            # si el tiempo de una ya supera el máximo, salgo del bucle y descartamos el tamaño
            if tiempo_pruebas[-1] > tiempo_max:
                tams.pop()
                # si antes solo ha hecho una prueba, que vuelva a empezar pero aumentando la cuarta parte
                if len(tams) == 1:
                    aumento_tam = aumento_tam // 4
                    return evalua_complejidad_t(dic_problema, fichero, tams_entrada)
                break
        # guardo el tiempo medio si ha hecho todas las ejecuciones
        if len(tiempo_pruebas) == pruebas_por_tam:
            tiempos.append(sum(tiempo_pruebas) / pruebas_por_tam)
        else:
            break

        if time.perf_counter() - tiempo_inicial >= tiempo_total_max:
            if len(tams) >= ejec_min:
                return tams, tiempos
            break

        print('sigo', tams[-1], tiempos[-1])

    while len(tiempos) < ejec_min:

        print('añadiendo puntos intermedios...')

        for j in range(1, len(tams) * 2 - 1, 2):
            tams.insert(j, (tams[j - 1] + tams[j]) // 2)

            if aumentar != 0:
                tams_entrada[aumentar - 1] = tams[j]

            tiempo_pruebas = []
            for _ in range(pruebas_por_tam):
                entrada = []
                for i in range(len(tipo_entrada)):
                    entrada.append(entrada_aleatoria(tipo_entrada[i], tams_entrada[i]))
                tiempoini = time.perf_counter()
                funcion(*entrada)
                tiempo_pruebas.append(time.perf_counter() - tiempoini)
                if tiempo_pruebas[-1] > tiempo_max:
                    tams.pop(j)
                    break
            if len(tiempo_pruebas) == pruebas_por_tam:
                tiempos.insert(j, sum(tiempo_pruebas) / pruebas_por_tam)
            else:
                break

            print('sigo', tams[j], tiempos[j])

            if len(tiempos) >= ejec_min:
                break
            # si sobrepasa tiempo_total_max + tiempo_extra, calcula con tamaños más pequeños
            # if time.perf_counter() - tiempo_inicial >= tiempo_total_max + tiempo_extra:
            #     break

    return tams, tiempos


contador_de_lineas_para_calcular_oe_complejidad = 0


def evalua_complejidad_oe(dic_problema, fichero, tams_entrada):
    global contador_de_lineas_para_calcular_oe_complejidad, aumento_tam
    # leo la función con el contador de oe añadido
    with open(fichero, 'r') as fich:
        exec(contador_lineas(fich.read()))
    funcion = eval(dic_problema['funcion'])
    aumentar = int(dic_problema['aumentar'])
    tipo_entrada = dic_problema['tipo_param']

    # inicializo tamaños y operaciones elementales
    tams = [1]
    if aumentar != 0:
        tams_entrada[aumentar - 1] = tams[-1]
    ops = []
    aum = 1
    veces_cte = 0  # se cuenta las que son seguidas
    tiempo_inicial = time.perf_counter()

    # evalúo la función con tamaños cada vez mayores y guardo las operaciones elementales
    while ops == [] or (ops[-1] < ops_max and veces_cte < max_veces_cte):
        # aumento tamaño del parámetro que toca
        if len(ops) >= 2 and abs(ops[-1] - ops[-2]) < ops_min_entre_ejec:
            aum *= factor_aum
            print('aumento', aum)
            veces_cte += 1
        else:
            veces_cte = 0

        if aumentar != 0 and ops != []:
            tams_entrada[aumentar - 1] = tams[-1] + aumento_tam * aum
            tams.append(tams_entrada[aumentar - 1])

        # evalúo pruebas_por_tam veces con ese tamaño
        ops_pruebas = []
        for _ in range(pruebas_por_tam):
            # creo otra prueba aleatoria
            entrada = []
            for i in range(len(tipo_entrada)):
                entrada.append(entrada_aleatoria(tipo_entrada[i], tams_entrada[i]))
            # evalúo y cuento las oe
            contador_de_lineas_para_calcular_oe_complejidad = 0
            funcion(*entrada)
            ops_pruebas.append(contador_de_lineas_para_calcular_oe_complejidad)
            # si las oe de una ya supera el máximo, salgo del bucle y descartamos el tamaño
            if ops_pruebas[-1] > ops_max:
                tams.pop()
                # si antes solo ha hecho una prueba, que vuelva a empezar pero aumentando la cuarta parte
                if len(tams) == 1:
                    aumento_tam = aumento_tam // 4
                    return evalua_complejidad_oe(dic_problema, fichero, tams_entrada)
                break
        # guardo las oe medias si ha hecho todas las ejecuciones
        if len(ops_pruebas) == pruebas_por_tam:
            ops.append(sum(ops_pruebas) / pruebas_por_tam)
        else:
            break

        if time.perf_counter() - tiempo_inicial >= tiempo_total_max:
            if len(tams) >= ejec_min:
                return tams, ops
            break

        print('sigo', tams[-1], ops[-1])

    while len(ops) < ejec_min:

        print('añadiendo puntos intermedios...')

        for j in range(1, len(tams) * 2 - 1, 2):
            tams.insert(j, (tams[j - 1] + tams[j]) // 2)

            if aumentar != 0:
                tams_entrada[aumentar - 1] = tams[j]

            ops_pruebas = []
            for _ in range(pruebas_por_tam):
                entrada = []
                for i in range(len(tipo_entrada)):
                    entrada.append(entrada_aleatoria(tipo_entrada[i], tams_entrada[i]))
                contador_de_lineas_para_calcular_oe_complejidad = 0
                funcion(*entrada)
                ops_pruebas.append(contador_de_lineas_para_calcular_oe_complejidad)
                if ops_pruebas[-1] > ops_max:
                    tams.pop(j)
                    break
            if len(ops_pruebas) == pruebas_por_tam:
                ops.insert(j, sum(ops_pruebas) / pruebas_por_tam)
            else:
                break

            print('sigo', tams[j], ops[j])

            if len(ops) >= ejec_min:
                break
            # si sobrepasa tiempo_total_max + tiempo_extra, calcula con tamaños más pequeños
            # if time.perf_counter() - tiempo_inicial >= tiempo_total_max + tiempo_extra:
            #     break

    return tams, ops


# Familias de funciones para el orden de complejidad
def constante(x, a):
    try:
        return [a] * len(x)
    except TypeError:
        return a


def lineal(x, a, b):
    return a + b * x


def cuadratica(x, a, b):
    return a + b * x ** 2


def polinomial(x, a, b, c):
    return a + b * x ** c


def cuasilineal(x, a, b):
    if type(x) == sympy.Symbol:
        return a + b * x * sympy.log(x, 2)
    return a + b * x * np.log2(x)


def logaritmica(x, a, b):
    if type(x) == sympy.Symbol:
        return a + b * sympy.log(x, 2)
    return a + b * np.log2(x)


def exponencial(x, a, b):
    return a + b * 2 ** x


funciones = (constante, lineal, cuadratica, polinomial, logaritmica, cuasilineal, exponencial)


# Comprueba qué función de las familias de funciones es más próxima a los datos tamaño-tiempo que tenemos
def funciones_complejidad(x, y, funcs=funciones):
    x, y = np.array(x), np.array(y)
    funcs = list(funcs)
    valores_opt = []
    residuos = []
    fx = []
    for f in funcs:
        try:
            popt = scipy.optimize.curve_fit(f, x, y)[0]
            valores_opt.append(popt)
            fx.append(f(x, *popt))
            residuos.append(sum(abs(y - fx[-1])))
        except RuntimeError:
            funcs.remove(f)
    print('funciones: ', funcs)
    print('residuos: ', residuos)
    return funcs, valores_opt, residuos, fx


# Pinta la gráfica de tamaño-tiempo junto con la función aproximada y junto con todas las aproximaciones calculadas
def pinta_graficas(x, y, complejidad):
    funcs, val_opt, residuos, fx = funciones_complejidad(x, y)
    res_min = np.min(np.array(residuos))
    pos_min = residuos.index(res_min)
    f_min = funcs[pos_min]
    val_min = val_opt[pos_min]
    # si es una polinomial pero con exponente casi 0, 1 o 2, quitamos polinomial
    if f_min == polinomial and round(val_min[-1], 1) in [0, 1, 2]:
        [_.pop(pos_min) for _ in [funcs, val_opt, residuos, fx]]
        res_min = np.min(np.array(residuos))
        pos_min = residuos.index(res_min)
        f_min = funcs[pos_min]
        val_min = val_opt[pos_min]

    plt.plot(x, y, '.-', label=complejidad)

    x_symbol = sympy.Symbol('x')
    f_str = f_min(x_symbol, *val_min)
    plt.plot(x, fx[pos_min], '--', label=f_str)
    plt.legend(loc='lower right')
    titulo = 'La complejidad es de orden ' + f_min.__name__
    if f_min.__name__ == 'polinomial':
        titulo += ' con exp ' + str(round(val_min[-1], 4))
    plt.title(titulo)
    plt.tight_layout()
    plt.savefig('grafica_mejor.png')
    plt.show()

    plt.plot(x, y, '.-', label=complejidad)
    for i in range(len(funcs)):
        if (complejidad == 'tiempo' and residuos[i] <= residuo_max_t) or \
                (complejidad == 'operaciones' and residuos[i] <= residuo_max_oe):
            # f_str = funcs[i](x_symbol, *val_opt[i])
            nombre = funcs[i].__name__
            if nombre == 'polinomial':
                nombre += '\nexp=' + str(round(val_opt[i][-1], 3))
            plt.plot(x, fx[i], '--',
                     label='\n'.join([nombre, 'res=' + str(round(residuos[i], 3))]))
    plt.legend(bbox_to_anchor=(1.05, 1.05), loc='upper left')
    plt.tight_layout()
    plt.title('Gráfica con todas las aproximaciones.')
    plt.savefig('grafica_todas.png')
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
def evalua_problema(id, fichero, complejidad=''):
    dic_problema = lee_problema(id)
    with open(fichero, 'r') as fich:
        exec(fich.read())
    funcion = eval(dic_problema['funcion'])

    # Comprueba el resultado de todas las pruebas
    pruebas, resultados = [], []
    with scandir(os.path.join(carpeta_problemas, id)) as carpeta:
        for file in carpeta:
            if file.is_file() and file.name.endswith(sufijo_entrada):
                pruebas.append((file.path, file.path[:-len(sufijo_entrada)] + sufijo_salida))
    todo_correcto = True
    for prueba in pruebas:
        with open(prueba[0], 'r') as e:
            entrada = e.read().split('\n')
            # Quitamos el argumento vacío que surge si hay una línea vacía al final
            if entrada[-1] == '' and len(entrada) > len(dic_problema['tipo_param']):
                entrada = entrada[:-1]
            entrada = [eval(_) for _ in entrada]
            tiempoini = time.perf_counter()
            salidareal = funcion(*entrada)
            tiempototal = time.perf_counter() - tiempoini
        with open(prueba[1], 'r') as s:
            salidaesperada = eval(s.read())
        if salidareal == salidaesperada:
            resultados.append('OK' + ', ' + str(tiempototal))
        else:
            todo_correcto = False
            resultados.append('(' + ', '.join(entrada) + ')' + ', ' + str(salidaesperada) + ', ' + str(salidareal))

    if todo_correcto and len(pruebas) > 0 and complejidad != '':
        # Calculamos los tamaños de entrada - ¿solo lo necesito si algún valor se queda fijo?
        tams_entrada = []
        for i in range(len(entrada)):
            tipo = dic_problema['tipo_param'][i]
            if tipo in ['str', 'int']:
                tams_entrada.append(len(str(entrada[i])))
            elif tipo == 'float':
                parte_entera, parte_decimal = entrada[i].split('.')
                tams_entrada.append([len(parte_entera), len(parte_decimal)])
            elif tipo.startswith('list') or tipo.startswith('tuple'):
                tams_entrada.append(len(entrada[i]))
        # calculo la complejidad para entradas cada vez mayores - ¿y si aumentar == 0?
        if complejidad == 'T':
            tams, tiempos = evalua_complejidad_t(dic_problema, fichero, tams_entrada)
            pinta_graficas(tams, tiempos, 'tiempo')
        elif complejidad == 'OE':
            tams, ops = evalua_complejidad_oe(dic_problema, fichero, tams_entrada)
            pinta_graficas(tams, ops, 'operaciones')
    return resultados


# print(evalua_problema('alfabetica', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-alfabetica.py'))
# print(evalua_problema('menorque', 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros\\solucion-menorque.py'))


# base = 'C:\\Users\\laura\\PycharmProjects\\TFG\\otros'
base = 'otros'

# EJEMPLOS PALÍNDROMO
# evalua_problema('palindromo', os.path.join(base, 'solucion-palindromo-efi.py'), 'T')
# evalua_problema('palindromo', os.path.join(base, 'solucion-palindromo-inefi.py'), 'OE')

# EJEMPLOS ORDENAR
# evalua_problema('ordenar', os.path.join(base, 'solucion-ordenar-burbuja.py'), 'T')
# evalua_problema('ordenar', os.path.join(base, 'solucion-ordenar-insercion.py'), 'T')
# evalua_problema('ordenar', os.path.join(base, 'solucion-ordenar-seleccion.py'), 'OE')
# evalua_problema('ordenar', os.path.join(base, 'solucion-ordenar-sort.py'), 'OE')

# EJEMPLOS BUSCAR
# evalua_problema('buscar', os.path.join(base, 'solucion-buscar-binaria.py'), 'OE')
# evalua_problema('buscar', os.path.join(base, 'solucion-buscar-unoauno.py'), 'OE')
# evalua_problema('buscar', os.path.join(base, 'solucion-buscar-unoauno-inefi.py'), 'OE')
# evalua_problema('buscar', os.path.join(base, 'solucion-buscar-in.py'), 'T')

# EJEMPLOS EXPONENCIAL # aumento muy pequeño
# evalua_problema('potencias2', os.path.join(base, 'solucion-potencias2-efi.py'), 'T')
# evalua_problema('potencias2', os.path.join(base, 'solucion-potencias2-inefi.py'), 'T')
