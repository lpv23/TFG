def buscar(lista, elem):
    inicio = 0
    fin = len(lista) - 1
    while inicio <= fin:
        medio = (inicio + fin) // 2
        if lista[medio] == elem:
            return True
        if lista[medio] < elem:
            inicio = medio + 1
        else:
            fin = medio - 1
    return False
