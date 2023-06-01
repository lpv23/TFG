# Trabajo de Fin de Grado: Implementación de sistema de juez en línea para desafíos algorítmicos.

Este directorio contiene el código de implementación de un pequeño sistema de juez en línea. 
Forma parte del Trabajo de Fin de Grado realizado por Laura Pina Valencia para obtener el Grado en Matemáticas impartido en la Universidad de Alicante.

## Resumen

Los sistemas de juez en línea son aplicaciones web que se utilizan para la evaluación automática de algoritmos. 
Permiten a los usuarios enviar sus soluciones a distintos desafíos algorítmicos y se encargan de comprobar su validez, 
exigiendo a su vez que el tiempo de ejecución no supere un límite establecido. Estos sistemas desempeñan un papel
fundamental en el ámbito de la educación y los concursos de programación.

Este trabajo se centra en el desarrollo de un sistema de juez en línea, con el lenguaje
de programación Python, que sea capaz de verificar la solución introducida y estimar
su complejidad algorítmica asintótica en el caso promedio. Esta se obtendrá de forma
empírica, evaluando la función del usuario con tamaños de entrada cada vez mayores. Al
no contar con un límite de tiempo tan estricto y mostrar la complejidad, el sistema se
convertirá en un recurso más didáctico que competitivo.

## Instrucciones de uso

Para iniciar la aplicación web del juez en línea, se debe escribir en la terminal del directorio el comando ``flask --app juez run`` y pulsar en el enlace generado.

<!-- Para añadir un nuevo desafío al sistema, se debe crear en la carpeta problemas un nuevo directorio con los ficheros de texto correspondientes. 
- El documento ``problema.txt`` con la información del desafío separada en líneas. 
  - Línea 1. Título del desafío algorítmico.
  - Línea 2. Descripción del mismo. Aquí se especifica al usuario el nombre de la función y los argumentos de entrada y de salida.
  - Línea 3. Nombre que debe tener la función. El sistema utilizará este nombre para ejecutar la función con las distintas entradas.
  - Línea 4. Enumera los argumentos de los que depende la complejidad. Para poder estudiar el orden de complejidad, el sistema aumentará automáticamente el tamaño de estas entradas. La enumeración de los argumentos empieza en 1 y se separan por comas. Si es 0 o no hay ningún número, el juez entenderá que no debe estudiar su complejidad.
  - Línea 5 y siguientes. En cada línea, a partir de la 5, se define el tipo de un parámetro de entrada y si cumple alguna característica. Por ejemplo, si una lista
debe estar ordenada. Veremos los tipos disponibles con más detalle en la sección 2.4,
en la tabla 1. Esta información la necesitará el juez a la hora de generar entradas
aleatorias de distintas tallas para estudiar la complejidad.
- Las pruebas de entrada y salida para verificar la solución. Cada prueba consta de dos documentos que comienzan por el mismo nombre. Sin embargo, tendrán distintas terminaciones: 
  - ``.entrada.txt`` para el que contenga la entrada de la función (cada argumento en una línea) 
  - ``.salida.txt`` para el que incluya la salida esperada.  -->

Se puede encontrar más información acerca de su funcionamiento en el documento ''MemoriaTFG.pdf''.


