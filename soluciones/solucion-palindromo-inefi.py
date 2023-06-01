def palindromo(cadena):
    result = True
    for i in range(len(cadena) // 2):
        if cadena[i] != cadena[-i-1]:
            result = False
    return result
