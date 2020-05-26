# DS_A2-MutualExclusion
 Algoritmo en Python que proporciona la exclusión mutua a un fichero almacenado en IBM COS
## Configuración del entorno de ejecución
 Este programa construído en Python necesita de la versión 3.7 del mismo. Además, previamente a la ejecución del código, hay que tener el paquete pywren-ibm-cloud instalado (link *[aquí][1]*)
 Además, hace falta incluir la configuración necesaria de COS y CF, en el fichero ~/.pywren_config (situado en el directorio HOME del usuario)
## Explicación de ejecución del algoritmo
 Varias funciones ejecutadas en el cloud y coordinadas por una función master son las encargadas de agregar al final del fichero result.json su identificador de función (núm. correlativo). Sólo una función puede acceder a la vez al fichero (principio de ex. mutua).

 El algoritmo se invoca desde la línea de comandos del siguiente modo:

 `$ ./main.py N`

 , donde N es el número de funciones remotas que añadirán su id al fichero result.json


 [1]: https://github.com/pywren/pywren-ibm-cloud