def ordenar(lista):
    for i in range(1, len(lista)):
        x = lista[i]
        j = i - 1
        while (j >= 0) and (lista[j] > x):
            lista[j + 1] = lista[j]
            j = j - 1
        lista[j + 1] = x
    return lista
