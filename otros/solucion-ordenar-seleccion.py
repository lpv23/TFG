def ordenar(lista):
    for i in range(0, len(lista) - 1):
        min = lista[i]
        posmin = i
        for j in range(i + 1, len(lista)):
            if lista[j] < min:
                min = lista[j]
                posmin = j
        lista[posmin] = lista[i]
        lista[i] = min
    return lista
