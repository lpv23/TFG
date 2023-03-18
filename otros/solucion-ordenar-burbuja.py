def ordenar(lista):
    for i in range(1, len(lista)):
        for j in range(len(lista) - 1, i - 1, -1):
            if lista[j] < lista[j - 1]:
                aux = lista[j]
                lista[j] = lista[j - 1]
                lista[j - 1] = aux
    return lista
