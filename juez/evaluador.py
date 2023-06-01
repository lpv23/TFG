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

# VARIABLES GLOBALES
ejec_min = 50  # número de ejecuciones mínimas con tamaños diferentes
tiempo_total_max = 120  # tiempo total máximo del programa
tiempo_max = 0.5  # tiempo máximo por ejecución
ops_max = 5e6  # operaciones máximas por ejecución
aumento_tam = 15  # aumento de tamaño
factor_aum = 5  # factor por el que se multiplica el aumento_tam si vemos que se queda muy constante
t_min_entre_ejec = 1e-3  # tiempo mínimo que debe haber entre ejecuciones para no considerarse constante
ops_min_entre_ejec = 1000  # operaciones mínimas que debe haber entre ejecuciones para no considerarse constante
max_veces_cte = 8  # si se alcanza t/ops_min_entre_ejec max_veces_cte, se calculan los puntos intermedios
pruebas_por_tam = 10  # pruebas que debe hacer por cada tamaño (con entradas diferentes)
residuo_max_t = 10  # si la aproximación tiene un residuo mayor, no aparece en la gráfica
residuo_max_oe = 2e7  # si la aproximación tiene un residuo mayor, no aparece en la gráfica


# Inspecciona el contenido de la carpeta "problemas" y devuelve una lista con los nombres de las subcarpetas.
def lista_problemas():
    carpetas = []
    with scandir(carpeta_problemas) as problemas:
        for file in problemas:
            if file.is_dir():
                carpetas.append(file.name)
    return carpetas


# Lee los datos del problema de la carpeta "id", que se encuentra dentro de la carpeta "problemas".
# Devuelve un diccionario con las siguientes claves:
# 'id': nombre de la carpeta, pasado como parámetro -- 'menor'
# 'title': primera línea de problema.txt -- 'Encuentra el menor elemento'
# 'body': segunda línea de problema.txt -- 'Encuentra el menor elemento en una lista que no está ordenada y devuélvelo'
# 'funcion': nombre de la función que el usuario tiene que crear (tercera línea de problema.txt) -- 'menor'
# 'aumentar': cuarta línea - n.º de los parámetros que deben aumentar su tamaño (si es 0, nada aumenta)
# 'tipo_param': a partir de la línea 5 - tipo de cada parámetro (uno en cada línea)
# (con un espacio para indicar el tipo dentro de una tupla o lista)
# (se puede añadir otra característica con un espacio de separación: sorted, reversed, digits, ...)
def lee_problema(id):
    problemas = lista_problemas()
    for pr in problemas:
        if id == pr:
            path = os.path.join(carpeta_problemas, id, "problema.txt")
            with open(path, 'r', encoding='UTF-8') as fichero:
                lineas = fichero.read().split('\n')
            if len(lineas) >= 5:
                return {'id': pr,
                        'title': lineas[0],
                        'body': lineas[1],
                        'funcion': lineas[2],
                        'aumentar': [int(_) - 1 for _ in lineas[3].split(', ') if _ != '0'],
                        'tipo_param': lineas[4:]}
    return {}


# Devuelve una entrada aleatoria del tipo indicado y de tamaño n.
def entrada_aleatoria(tipo, n):
    if tipo == 'str':  # string de letras minúsculas
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))
    elif tipo.startswith('int'):
        if tipo.endswith('digits'):
            return random.randint(10 ** (n - 1), (10 ** n) - 1)
        elif tipo.removeprefix('int ').startswith('list'):
            if tipo.endswith('out'):
                return 2 * n + 1
            return random.randint(0, 2 * n)
        return n
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
            resultado.sort(reverse=True)
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
    return None


# Añade el contador de líneas a la función introducida como parámetro (en cadena de texto).
def contador_lineas(cad_funcion):
    tab = '    '
    cont = 'contador_de_lineas_para_calcular_oe_complejidad'
    lista = cad_funcion.split('\n')
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
        # No se cuenta la línea si está vacía, es un else ni si es un comentario
        # Tampoco se cuentan los elif por comodidad (aunque se pierda precisión)
        if linea == '' or linea.startswith('else:') or linea.startswith('elif ') or linea.startswith('#'):
            i += 1
        # Si es un while o for se cuenta una vez antes (para la vez que ya no entre, pero compruebe la condición)
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


contador_de_lineas_para_calcular_oe_complejidad = 0


# Evalúa la función introducida como parámetro para entradas con tallas cada vez mayores
# y devuelve dos listas con los datos de tamaños y tiempos u operaciones.
def evalua_complejidad(dic_problema, cad_funcion, tams_entrada, complejidad):
    global contador_de_lineas_para_calcular_oe_complejidad, aumento_tam
    # Lee la función con o sin contador de OE
    if complejidad == 'T':
        exec(cad_funcion)
    elif complejidad == 'OE':
        cad_funcion_cont = contador_lineas(cad_funcion)
        if not comprueba_pruebas(dic_problema, cad_funcion_cont)[0]:
            exit('Ha surgido un problema al contar las líneas.')
        exec(cad_funcion_cont)

    funcion = eval(dic_problema['funcion'])
    aumentar = dic_problema['aumentar']
    tipo_entrada = dic_problema['tipo_param']

    # Inicializa tamaños y mediciones (tiempos u operaciones)
    tams = [1]
    for i in aumentar:
        tams_entrada[i] = tams[-1]
    tiempos = []
    aum = 1
    veces_cte = 0  # se cuentan las que son seguidas
    tiempo_inicial = time.perf_counter()  # inicializa el contador de tiempo total

    # Evalúa la función con tamaños cada vez mayores y guarda las mediciones
    while tiempos == [] or (complejidad == 'T' and tiempos[-1] < tiempo_max and veces_cte < max_veces_cte) or \
            (complejidad == 'OE' and tiempos[-1] < ops_max and veces_cte < max_veces_cte):

        # Comprueba si está avanzando muy poco, casi constante
        if len(tiempos) >= 2 and ((complejidad == 'T' and abs(tiempos[-1] - tiempos[-2]) < t_min_entre_ejec) or
                                  (complejidad == 'OE' and abs(tiempos[-1] - tiempos[-2]) < ops_min_entre_ejec)):
            aum *= factor_aum
            print('aumento', aum)
            veces_cte += 1
        else:
            veces_cte = 0

        # Aumenta el tamaño de los parámetros que tocan
        if tiempos and aumentar:
            nuevo_tam = tams[-1] + aumento_tam * aum
            tams.append(nuevo_tam)
            for i in aumentar:
                tams_entrada[i] = nuevo_tam

        # Evalúa pruebas_por_tam veces con ese tamaño
        tiempo_pruebas = []
        for _ in range(pruebas_por_tam):
            # Crea otra prueba aleatoria
            entrada = [entrada_aleatoria(tipo_entrada[i], tams_entrada[i]) for i in range(len(tipo_entrada))]
            # Evalúa y cuenta mediciones
            if complejidad == 'T':
                tiempoini = time.perf_counter()
                funcion(*entrada)
                tiempo_pruebas.append(time.perf_counter() - tiempoini)
            elif complejidad == 'OE':
                contador_de_lineas_para_calcular_oe_complejidad = 0
                funcion(*entrada)
                tiempo_pruebas.append(contador_de_lineas_para_calcular_oe_complejidad)
            # Si la medición de una ya supera el máximo, sale del bucle y descarta el tamaño
            if (complejidad == 'T' and tiempo_pruebas[-1] > tiempo_max) or \
                    (complejidad == 'OE' and tiempo_pruebas[-1] > ops_max):
                tams.pop()
                # Si solo tiene un tamaño guardado, vuelve a empezar pero aumentando la tercera parte
                if len(tams) == 1:
                    aumento_tam = aumento_tam // 3
                    return evalua_complejidad(dic_problema, cad_funcion, tams_entrada, complejidad)
                break
        # Guarda la media si ha hecho las pruebas_por_tam ejecuciones
        if len(tiempo_pruebas) == pruebas_por_tam:
            tiempos.append(sum(tiempo_pruebas) / pruebas_por_tam)
        else:
            break
        # Comprueba que no sobrepase el tiempo límite total
        # Si lo supera y ya tiene las mínimas ejecuciones requeridas, devuelve el resultado
        # Si lo supera y no tiene las mínimas ejecuciones requeridas, evalúa con tamaños intermedios
        if time.perf_counter() - tiempo_inicial >= tiempo_total_max:
            if len(tams) >= ejec_min:
                return tams, tiempos
            break

        print('sigo', tams[-1], tiempos[-1])

    while len(tiempos) < ejec_min:

        print('añadiendo puntos intermedios...')

        for j in range(1, len(tams) * 2 - 1, 2):
            tams.insert(j, (tams[j - 1] + tams[j]) // 2)

            for i in aumentar:
                tams_entrada[i] = tams[j]

            tiempo_pruebas = []
            for _ in range(pruebas_por_tam):
                entrada = [entrada_aleatoria(tipo_entrada[i], tams_entrada[i]) for i in range(len(tipo_entrada))]
                if complejidad == 'T':
                    tiempoini = time.perf_counter()
                    funcion(*entrada)
                    tiempo_pruebas.append(time.perf_counter() - tiempoini)
                elif complejidad == 'OE':
                    contador_de_lineas_para_calcular_oe_complejidad = 0
                    funcion(*entrada)
                    tiempo_pruebas.append(contador_de_lineas_para_calcular_oe_complejidad)
                if (complejidad == 'T' and tiempo_pruebas[-1] > tiempo_max) or \
                        (complejidad == 'OE' and tiempo_pruebas[-1] > ops_max):
                    tams.pop(j)
                    break
            if len(tiempo_pruebas) == pruebas_por_tam:
                tiempos.insert(j, sum(tiempo_pruebas) / pruebas_por_tam)
            else:
                break

            print('sigo', tams[j], tiempos[j])

            if len(tiempos) >= ejec_min:
                break

    return tams, tiempos


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
    return a + b * pow(2, x)


funciones = (constante, lineal, cuadratica, polinomial, logaritmica, cuasilineal, exponencial)


# Comprueba qué función de las familias de funciones es más próxima a los datos tamaño-tiempo introducidos como x, y.
# Devuelve la función más cercana, junto con el residuo y la imagen, de cada una de las familias.
def funciones_complejidad(x, y, funcs=funciones):
    x, y = np.array(x), np.array(y)
    lfuncs = list(funcs)
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
            lfuncs.remove(f)
    print('funciones: ', lfuncs)
    print('residuos: ', residuos)
    return lfuncs, valores_opt, residuos, fx


# Dibuja la gráfica de tamaño-tiempo junto con la función más próxima y junto con todas las aproximaciones calculadas.
def pinta_graficas(x, y, prefijo_graficas, complejidad):
    if complejidad == 'T':
        label_comp = 'Tiempo'
    else:
        label_comp = 'Operaciones'

    retorno = []

    funcs, val_opt, residuos, fx = funciones_complejidad(x, y)
    res_min = np.min(np.array(residuos))
    pos_min = residuos.index(res_min)
    f_min = funcs[pos_min]
    val_min = val_opt[pos_min]
    # Si es una polinomial, pero con exponente casi 0, 1 o 2, quita polinomial
    # y busca la siguiente mejor que será constante, lineal o cuadrática
    if f_min == polinomial and round(val_min[-1], 1) in [0, 1, 2]:
        [_.pop(pos_min) for _ in [funcs, val_opt, residuos, fx]]
        res_min = np.min(np.array(residuos))
        pos_min = residuos.index(res_min)
        f_min = funcs[pos_min]
        val_min = val_opt[pos_min]

    plt.plot(x, y, '.-', label=label_comp)

    x_symbol = sympy.Symbol('x')
    f_str = f_min(x_symbol, *val_min)
    plt.plot(x, fx[pos_min], '--', label=f_str)
    plt.legend(loc='lower right')
    titulo = 'La complejidad es de orden ' + f_min.__name__
    if f_min.__name__ == 'polinomial':
        titulo += ' con exp ' + str(round(val_min[-1], 4))
    plt.title(titulo)
    plt.tight_layout()

    fichero = prefijo_graficas + '_' + 'grafica_mejor.png'
    plt.savefig(fichero)
    retorno.append(os.path.basename(fichero))
    # plt.show()
    plt.figure()
    plt.plot(x, y, '.-', label=label_comp)
    for i in range(len(funcs)):
        if (complejidad == 'T' and residuos[i] <= residuo_max_t) or \
                (complejidad == 'OE' and residuos[i] <= residuo_max_oe):
            # f_str = funcs[i](x_symbol, *val_opt[i])
            nombre = funcs[i].__name__
            if nombre == 'polinomial':
                nombre += '\nexp=' + str(round(val_opt[i][-1], 3))
            res = f"{residuos[i]:.1e}" if residuos[i] < 0.001 else str(round(residuos[i], 3))
            plt.plot(x, fx[i], '--', label='\n'.join([nombre, 'res=' + res]))
    plt.legend(bbox_to_anchor=(1.05, 1.05), loc='upper left')
    plt.tight_layout()
    plt.title('Gráfica con todas las aproximaciones.')

    fichero = prefijo_graficas + '_' + 'grafica_todas.png'
    plt.savefig(fichero)
    retorno.append(os.path.basename(fichero))
    # plt.show()

    return retorno


# Ejecuta la función con cada uno de los ficheros de prueba que hay en el directorio del problema, comprueba si
# la salida coincide con la esperada y devuelve una lista que contenga cadenas con el resultado de cada prueba.
# - Si la prueba es correcta, el contenido será: 'Bien' y su tiempo de ejecución.
# - Si la prueba es incorrecta, el contenido será: 'Fallo', entrada, salida esperada y salida obtenida.
# - Si surge un error al ejecutar la prueba, el contenido será: 'Error', entrada, salida esperada y error obtenido.
#
# Los ficheros xxxxxxx.entrada.txt contienen un parámetro de entrada en cada línea.
# Los ficheros xxxxxxx.salida.txt contienen la salida esperada en la primera línea.
def comprueba_pruebas(dic_problema, cad_funcion, calcula_tams=False):
    exec(cad_funcion, globals())
    funcion = eval(dic_problema['funcion'])
    # Almacena todos los ficheros con las pruebas (entrada, salida esperada)
    pruebas, resultados = [], []
    with scandir(os.path.join(carpeta_problemas, dic_problema['id'])) as carpeta:
        for file in carpeta:
            if file.is_file() and file.name.endswith(sufijo_entrada):
                pruebas.append((file.path, file.path[:-len(sufijo_entrada)] + sufijo_salida))
    # Comprueba el resultado de todas las pruebas
    todo_correcto = True
    for prueba in pruebas:
        # Lee los ficheros de las pruebas
        with open(prueba[0], 'r') as e:
            entrada = e.read().split('\n')
            # Quita el argumento vacío que surge si hay una línea vacía al final
            if entrada[-1] == '' and len(entrada) > len(dic_problema['tipo_param']):
                entrada = entrada[:-1]
            entrada_eval = [eval(_) for _ in entrada]
        with open(prueba[1], 'r') as s:
            salidaesperada = eval(s.read())
        # Ejecuta la función con la entrada y comprueba si coincide con la salida esperada
        try:
            tiempoini = time.perf_counter()
            salidareal = funcion(*entrada_eval)
            tiempototal = time.perf_counter() - tiempoini
            if salidareal == salidaesperada:
                resultados.append('Bien. Tiempo de ejecución:' + str(tiempototal))
            else:
                todo_correcto = False
                resultados.append('Fallo. Entrada: (' + ', '.join(entrada) + '). Salida esperada: ' +
                                  str(salidaesperada) + '. Salida obtenida: ' + str(salidareal))
        except Exception as e:
            todo_correcto = False
            resultados.append('Error. Entrada: (' + ', '.join(entrada) + '). Salida esperada: ' + str(salidaesperada) +
                              '. Tipo de error: ' + str(type(e)))

    if calcula_tams and todo_correcto and len(pruebas) > 0:
        # Calcula los tamaños de entrada necesarios
        tams_entrada = []
        for i in range(len(entrada)):
            if i in dic_problema['aumentar']:
                tams_entrada.append(0)
            else:
                tipo = dic_problema['tipo_param'][i]
                if tipo == 'str':
                    tams_entrada.append(len(str(entrada[i])))
                elif tipo.startswith('int'):
                    tams_entrada.append(int(entrada[i]))
                elif tipo == 'float':
                    parte_entera, parte_decimal = str(entrada[i]).split('.')
                    tams_entrada.append([int(parte_entera), int(parte_decimal)])
                elif tipo.startswith('list') or tipo.startswith('tuple'):
                    tams_entrada.append(len(entrada[i]))
    else:
        tams_entrada = [0] * len(dic_problema['tipo_param'])

    return todo_correcto, resultados, tams_entrada


# Lee el fichero cuya ruta es "fichero", que contiene la definición de una función en Python,
# cuyo nombre viene definido por la clave 'funcion' del diccionario lee_problema(id).
# Llama a comprueba_pruebas para verificar si la solución es correcta.
# Si lo es, llama a pinta_gráficas para que dibuje las gráficas correspondientes.
# Devuelve los resultados de ejecutar las pruebas y las gráficas creadas.
def evalua_problema(id, fichero, prefijo_graficas='', complejidad=''):
    dic_problema = lee_problema(id)
    with open(fichero, 'r') as fich:
        cad_funcion = fich.read()

    graficas = []

    aumenta = dic_problema['aumentar']
    # Solo calcula los tamaños si alguno se queda fijo
    calcula_tams = True if (aumenta != [] and len(aumenta) < len(dic_problema['tipo_param'])) else False
    todo_correcto, resultados, tams_entrada = comprueba_pruebas(dic_problema, cad_funcion, calcula_tams)

    if todo_correcto and (complejidad == 'T' or complejidad == 'OE') and aumenta != []:
        tams, tiempos = evalua_complejidad(dic_problema, cad_funcion, tams_entrada, complejidad)
        graficas = pinta_graficas(tams, tiempos, prefijo_graficas, complejidad)

    return todo_correcto, resultados, graficas


# base = 'soluciones'

# EJEMPLOS PALÍNDROMO
# evalua_problema('palindromo', os.path.join(base, 'solucion-palindromo-efi.py'), complejidad='OE')
# evalua_problema('palindromo', os.path.join(base, 'solucion-palindromo-inefi.py'), complejidad='OE')

# EJEMPLOS ORDENAR
# evalua_problema('ordenar', os.path.join(base, 'solucion-ordenar-burbuja.py'), complejidad='T')
# evalua_problema('ordenar', os.path.join(base, 'solucion-ordenar-insercion.py'), complejidad='T')
# evalua_problema('ordenar', os.path.join(base, 'solucion-ordenar-seleccion.py'), complejidad='T')
# evalua_problema('ordenar', os.path.join(base, 'solucion-ordenar-sort.py'), complejidad='T')

# EJEMPLOS BUSCAR
# evalua_problema('buscar', os.path.join(base, 'solucion-buscar-binaria.py'), complejidad='OE')
# evalua_problema('buscar', os.path.join(base, 'solucion-buscar-unoauno.py'), complejidad='OE')
# evalua_problema('buscar', os.path.join(base, 'solucion-buscar-unoauno-inefi.py'), complejidad='T')
# evalua_problema('buscar', os.path.join(base, 'solucion-buscar-in.py'), complejidad='T')

# EJEMPLOS POTENCIAS DE 2
# evalua_problema('potencias2', os.path.join(base, 'solucion-potencias2-efi.py'), complejidad='T')
# evalua_problema('potencias2', os.path.join(base, 'solucion-potencias2-inefi.py'), complejidad='OE')
# evalua_problema('potencias2', os.path.join(base, 'solucion-potencias2-pow.py'), complejidad='OE')

# EJEMPLOS MENOR QUE
# evalua_problema('menorque', os.path.join(base, 'solucion-menorque.py'), complejidad='T')
