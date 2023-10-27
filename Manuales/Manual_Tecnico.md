# Manual Técnico
# Proyecto No.2: BizData
## Herramientas Utilizadas
### Python
Python es un lenguaje de programación de alto nivel, interpretado y orientado a objetos. Fue creado por Guido van Rossum en 1991 y se ha convertido en uno de los lenguajes de programación más populares y versátiles en todo el mundo. Python es conocido por su facilidad de uso, legibilidad de código y su amplia compatibilidad con una amplia variedad de aplicaciones y plataformas. Se utiliza en una amplia variedad de campos, incluyendo la web, la ciencia de datos, la ingeniería, la finanzas, la medicina, la tecnología y más. Python también es compatible con otros lenguajes de programación, como C, C++ y Java, lo que lo hace una buena opción para desarrolladores que deseen trabajar en proyectos que involucren varios lenguajes de programación.

### Graphviz
Graphviz es una herramienta de visualización de grafos que se utiliza para representar datos estructurados en forma de grafo. Es una herramienta de código abierto que se puede utilizar en una amplia variedad de contextos, incluyendo la programación, la inteligencia artificial, la ciencia de datos y la visualización de datos.

Graphviz utiliza un lenguaje de descripción de grafos basado en texto para definir los grafos y sus propiedades. El lenguaje de descripción de grafos de Graphviz se basa en una sintaxis similar a la utilizada en la mayoría de los diagramas de flujo y los diagramas UML.

### Tkinter
Tkinter es una biblioteca de Python que proporciona una interfaz gráfica de usuario (GUI) para aplicaciones de escritorio. Fue creado originalmente por Guido van Rossum en 1991 y se ha convertido en una de las bibliotecas de GUI de Python más populares y ampliamente utilizadas.

Tkinter también proporciona una amplia variedad de herramientas para trabajar con eventos de teclado, mouse y pantalla, lo que permite a los desarrolladores crear aplicaciones de escritorio más interactivas y dinámicas. Además, Tkinter es compatible con una amplia variedad de sistemas operativos, incluyendo Windows, macOS y Linux, lo que lo hace una herramienta ideal para desarrolladores de aplicaciones de escritorio que deseen crear aplicaciones que se ejecuten en una amplia variedad de plataformas.

## Contenido
### Menu.py
* Constructor: En este metodo esta la parte grafica de nuestro analizador, en el definimos que nuestra ventana se muestre al centro de la pantalla, asi como los colores de fondo de la ventana, el color de los botones, tambien creamos el area de texto de nuestro analizador lexico y el area de texto del analizador sintactico. Por ultimo le damos el funcionamiento a cada boton para que ejecute la accion correspondiente.

* Metodo abrir_archivo: En este metodo creamos una variable que se encargara de guardar la ruta de nuestro archivo .bizdata, luego se extrae la informacion del archivo para luego enviarla al area de texto de nuestro analizador lexico para seguidamente mostrarnos la informacion.

* Metodo analizar_archivo: En este metodo practicamente esta toda la logica de nuestro analizador, a travez de expresiones regulares creadas especificamente para extraer los datos que necesitamos para nuestro analizador extraemos las claves y los registros de nuestro archivo para guardarlos en diccionarios que luego se agregaran a listas para llevar un control mas practico. Luego de la misma forma con expresiones regulares extraemos las funciones de que realizara nuestro analizador para luego mostrar los resultados en el area de texto del analizador sintactico.

* Metodo reporte_errores: Este metodo se encarga de recopilar los errores de nuestro archivo .bizdata, a travez de expresiones regulares, palabras reservadas y caracteres reservados. Estos errores son tanto lexicos como sintacticos que contiene el archivo donde los crea en diccionarios para luego agregarlos a una lista, estos errores se exportan en una tabla creada en un archivo HTML para que al usuario le sea mas facil verlos, donde tambien se detalla el error, la fila y la columna.

* Metodo verificacion_token: Este metodo recibe a travez de parametros una palabra, una fila y una columna para determinar que tipo de token es, puede ser una palabra, un numero o un signo, este metodo crea el token en un diccionario para luego retornarlo y asi se pueda manipular en otro metodo.

* Metodo reporte_tokens: Este metodo se encarga de crear todos los tokens de nuestro analizador lexico, utiliza expresiones regulares para extraer datos del analizador, para luego analizar cada palabra o caracter dependiendo si es un signo, aqui se utiliza el metodo anterior para que verifique los tokens, luego de crearlos se agregan a una lista para luego exportarlos en una tabla creada en un archivo HTML.

* Metodo generar_arbol: Este metodo crea nuestro arbol de derivacion en relacion de nuestro analizador sintactico, para crearlo se utiliza la herramienta de Graphviz donde recopila la informacion del analizador y asi crear los nodos de nuestro arbol, este crea una imagen en PNG que luego la envia a un archivo HTML donde se muestra como queda el arbol de derivacion.

## Expresiones Regulares
* Expresion regular utilizada para las claves:<br>
`r'Claves\s*=\s*\[(.*?)\]'`

* Expresion regular utilizada para los registros:<br>
`r'Registros\s*=\s*\[(.*?)\]'`

* Expresion regular utilizada para `imprimir`:<br>
`r'imprimir\("?(.*?)"?\)'`

* Expresion regular utilizada para `imprimirln`:<br>
`r'imprimirln\("?(.*?)"?\)'`

* Expresion regular utilizada para `conteo`:<br>
`r'conteo\(\)'`

* Expresion regular utilizada para `promedio`:<br>
`r'promedio\("?(.*?)"?\)'`

* Expresion regular utilizada para `contarsi`:<br>
`r'contarsi\("(.+?)",\s*(\d+)\)'`

* Expresion regular utilizada para `datos`:<br>
`r'datos\(\)'`

* Expresion regular utilizada para `sumar`:<br>
`r'sumar\("?(.*?)"?\)'`

* Expresion regular utilizada para `max`:<br>
`r'max\("?(.*?)"?\)'`

* Expresion regular utilizada para `min`:<br>
`r'min\("?(.*?)"?\)'`

* Expresion regular utilizada para `exportarReporte`:<br>
`r'exportarReporte\("?(.*?)"?\)'`

## Método del Árbol
![arbol](/Manuales/Imagenes/arbol.dot.png)

## Autómata Finito Determinista del analizador léxico
**Tokens:** ver archivo HTML con tokens<br>
**Estados:** Q = {q0, q1, q2, q3}<br>
**Estado inicial:** q0<br>
**Alfabeto:** Σ = {texto, numero, signo}<br>
**Transiciones:**
* (q0,texto) = q1
* (q0,numero) = q2
* (q0,signo) = q3
* (q1,texto) = q1
* (q1,numero) = q2
* (q1,signo) = q3
* (q2,texto) = q1
* (q2,numero) = q2
* (q2,signo) = q3
* (q3,texto) = q1
* (q3,numero) = q2
* (q3,signo) = q3<br><br>
![AFD](/Manuales/Imagenes/AFD.JPG)

## Gramatica independiente del contexto del analizador sintactico
**Definiendo reglas de produccion:**<br>
Claves -> Registros<br>
imprimir -> cadena<br>
imprimirln -> cadena<br>
conteo -> Numero<br>
promedio -> Claves<br>
contarsi -> Claves<br>
datos -> Numero<br>
sumar -> Claves<br>
max -> Claves<br>
min -> Claves<br>
exportarReporte -> cadena<br>

**Simbolo Inicial**<br>
S -> Claves<br>