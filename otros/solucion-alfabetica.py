def alfabetica(cadena):
	retorno=True
	for i in range(len(cadena)-1):
		if cadena[i] > cadena[i+1]:
			retorno=False
			break
	return retorno
