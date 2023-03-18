# def buscar(lista, elem):
#     while len(lista) > 0:
#         elem_mitad = lista[len(lista) // 2]
#         if elem_mitad == elem:
#             return True
#         if elem_mitad < elem:
#             lista = lista[(len(lista) // 2 + 1):]
#         else:
#             lista = lista[:len(lista) // 2]
#     return False

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
