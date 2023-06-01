def palindromo(cadena):
    for i in range(len(cadena) // 2):
        if cadena[i] != cadena[-i-1]:
            return False
    return True
