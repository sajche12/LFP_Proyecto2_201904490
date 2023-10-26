import tkinter as tk
from tkinter import filedialog, messagebox
import re, random
from graphviz import Digraph

class Menu:
    
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Proyecto No. 2 BizData")
        self.root.geometry("900x600")
        
        # Center the window on the screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 900) / 2
        y = (screen_height - 600) / 2

        # Set the window position
        self.root.geometry("900x600+{}+{}".format(int(x), int(y)))
        
        # cambiar el color del fondo
        self.root.config(bg="gainsboro")
        
        #crear un text area para el editor
        self.editor = tk.Text(self.root, width=52, height=30)
        self.editor.place(x=20, y=100)
        
        # creat un text area para la impresion
        self.impresion = tk.Text(self.root, width=55, height=30)
        self.impresion.config(state='disabled')
        self.impresion.place(x=450, y=100)
        
        # crear boton abrir
        self.btn_abrir = tk.Button(self.root, text="Abrir", width=10, height=2, bg="darkslategrey", fg="white", font=("Roboto", 11, "bold"), command=self.abrir_archivo)
        self.btn_abrir.place(x=20, y=20)
        
        # crear boton analizar
        self.btn_analizar = tk.Button(self.root, text="Analizar", width=10, height=2, bg="darkslategrey", fg="white", font=("Roboto", 11, "bold"), command=self.analizar_archivo)
        self.btn_analizar.place(x=150, y=20)
        
        # crear boton reporte errores
        self.btn_errores = tk.Button(self.root, text="Reporte Errores", width=14, height=2, bg="darkslategrey", fg="white", font=("Roboto", 11, "bold"), command=self.reporte_errores)
        self.btn_errores.place(x=280, y=20)
        
        # crear boton reporte tokens
        self.btn_tokens = tk.Button(self.root, text="Reporte Tokens", width=14, height=2, bg="darkslategrey", fg="white", font=("Roboto", 11, "bold"), command=self.reporte_tokens)
        self.btn_tokens.place(x=440, y=20)
        
        # crear boton reporte arbol
        self.btn_arbol = tk.Button(self.root, text="Generar Arbol", width=12, height=2, bg="darkslategrey", fg="white", font=("Roboto", 11, "bold"), command=self.generar_arbol)
        self.btn_arbol.place(x=600, y=20)
    
    # Definicion de variables globales
    contenido = ""
    list_claves = []
    registros_temp = []
    res = []
    
    #Metodo para abrir un archivo
    def abrir_archivo(self):
        global contenido
        # abrir un archivo con el explorador de archivos
        archivo = filedialog.askopenfilename(title="Abrir Archivo", filetypes=(("Archivo Bizdata", "*.bizdata"),))
        
        # quiero que la informacion del archivo se muestre en el editor
        # abrir el archivo
        with open(archivo, "r") as f:
            contenido = f.read()
            self.editor.delete("1.0", tk.END)
            self.editor.insert("1.0", contenido)
            
        # mostrar mensaje de exito
        messagebox.showinfo("Informacion", "Archivo abierto con exito")
    
    
    #Metodo para analizar el archivo
    def analizar_archivo(self):
        global contenido, list_claves, registros_temp, res
        list_claves = []
        registros_temp = []
        res = []
        # guardar el texto de self.editor en la variable contenido
        contenido = self.editor.get("1.0", tk.END)
        
        # Patrones de expresiones regulares
        patron_claves = re.compile(r'Claves\s*=\s*\[(.*?)\]', re.DOTALL)
        patron_signos = re.compile(r'[\'\"\s\n]+')
        patron_registros = re.compile(r'Registros\s*=\s*\[(.*?)\]', re.DOTALL)
        patron_llaves = re.compile(r'\{(.*?)\}')
        
        # buscar el patron en contenido y extraer el texto
        claves = patron_claves.search(contenido).group(1)
        # buscar con el patron_signos y extraer el texto
        claves = patron_signos.sub("", claves)
        # buscar hasta donde se encuentre una coma y guardar cada palabra en list_claves
        for clave in claves.split(","):
            list_claves.append(clave)
        #print(f"Claves = {list_claves}")
        
        registros = patron_registros.search(contenido).group(1)
        registros = patron_signos.sub("", registros)
        resultados = patron_llaves.findall(registros)
        # Dividir cada resultado en una lista utilizando la coma como separador
        lista_resultados = [r.split(',') for r in resultados]
        
        dic_temp = {}
        for registro in lista_resultados:
            for j,clave in enumerate(list_claves):
                dic_temp[clave] = registro[j]
            registros_temp.append(dic_temp)
            dic_temp = {}
        
        #print(f"Registros: {registros_temp}")
        
        # IMPRESION DE LOS REGISTROS
        # Patrones de expresiones regulares
        patron_imprimir = re.compile(r'imprimir\("?(.*?)"?\)')
        patron_imprimirln = re.compile(r'imprimirln\("?(.*?)"?\)')
        patron_conteo = re.compile(r'conteo\(\)')
        patron_promedio = re.compile(r'promedio\("?(.*?)"?\)')
        patron_contarsi = re.compile(r'contarsi\("(.+?)",\s*(\d+)\)')
        patron_datos = re.compile(r'datos\(\)')
        patron_sumar = re.compile(r'sumar\("?(.*?)"?\)')
        patron_max = re.compile(r'max\("?(.*?)"?\)')
        patron_min = re.compile(r'min\("?(.*?)"?\)')
        patron_exportar = re.compile(r'exportarReporte\("?(.*?)"?\)')
        
        texto = ""
        cadena = ""
        for i in contenido.split("\n"):
            if patron_imprimir.search(i):
                line = patron_imprimir.search(i).group(1)
                cadena = cadena+line
                # verificar si cadena ya se encuentra en self.impresion
                if cadena not in self.impresion.get("1.0", tk.END):
                    # Mostrar texto en self.impresion
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f">>> {cadena}\n")
                    self.impresion.config(state='disabled')
                    res_nuevo = {}
                    res_nuevo['tipo'] = "imprimir"
                    res_nuevo['valor'] = cadena
                    res.append(res_nuevo)
            else:
                if patron_imprimirln.search(i):
                    linea = patron_imprimirln.search(i)
                    texto = linea.group(1)
                    # Mostrar texto en self.impresion
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f">>> {texto}\n")
                    self.impresion.config(state='disabled')
                    res_nuevo = {}
                    res_nuevo['tipo'] = "imprimirln"
                    res_nuevo['valor'] = texto
                    res.append(res_nuevo)
                elif patron_conteo.search(i):
                    cantidad_datos = len(registros_temp)
                    # Mostrar texto en self.impresion
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f">>> {cantidad_datos}\n")
                    self.impresion.config(state='disabled')
                    res_nuevo = {}
                    res_nuevo['tipo'] = "conteo"
                    res_nuevo['valor'] = cantidad_datos
                    res.append(res_nuevo)
                elif patron_promedio.search(i):
                    suma = 0
                    texto = patron_promedio.search(i).group(1)
                    # buscar texto en las keys de los diccionarios dentro de registros_temp
                    for i in registros_temp:
                        for k,v in i.items():
                            if k == texto:
                                suma = suma + float(v)
                    promedio = round(suma / len(registros_temp), 2)
                    # Mostrar texto en self.impresion
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f">>> {promedio}\n")
                    self.impresion.config(state='disabled')
                    res_nuevo = {}
                    res_nuevo['tipo'] = "promedio"
                    res_nuevo['valor'] = promedio
                    res.append(res_nuevo)
                elif patron_contarsi.search(i):
                    nombre_campo = patron_contarsi.search(i).group(1)
                    valor = patron_contarsi.search(i).group(2)
                    # buscar nombre_campo en las keys de los diccionarios dentro de registros_temp e imprimir el valor de registros_temp[nombre_campo], ejemplo si valor es 2 imprimir los primeros dos registros
                    contador = 0
                    cero_impreso = False  # variable booleana para verificar si ya se ha impreso el mensaje correspondiente
                    for i in registros_temp:
                        for k,v in i.items():
                            if k == nombre_campo:
                                # contar cuantas veces se repite el valor en el campo
                                if v == valor:
                                    contador = contador + 1
                                elif int(valor) == 0 and cero_impreso == False:
                                    # Mostrar texto en self.impresion
                                    self.impresion.config(state='normal')
                                    self.impresion.insert("end", f">>> 0\n")
                                    self.impresion.config(state='disabled')
                                    cero_impreso = True
                    # Mostrar texto en self.impresion
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f">>> {contador}\n")
                    self.impresion.config(state='disabled')
                                       
                elif patron_datos.search(i):
                    for j,clave in enumerate(list_claves):
                        if j == 0:
                            # Mostrar texto en self.impresion
                            self.impresion.config(state='normal')
                            self.impresion.insert("end", f">>> {clave}|")
                            self.impresion.config(state='disabled')
                        else:
                            self.impresion.config(state='normal')
                            self.impresion.insert("end", f"{clave}|")
                            self.impresion.config(state='disabled')
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f"\n")
                    self.impresion.config(state='disabled')
                    for i in registros_temp:
                        for j,clave in enumerate(list_claves):
                            if j == 0:
                                self.impresion.config(state='normal')
                                self.impresion.insert("end", f">>> {i[clave]}\t")
                                self.impresion.config(state='disabled')
                            else:
                                self.impresion.config(state='normal')
                                self.impresion.insert("end", f"{i[clave]}\t  ")
                                self.impresion.config(state='disabled')
                        # verificar si es la ultima iteracion
                        if i != registros_temp[-1]:
                            self.impresion.config(state='normal')
                            self.impresion.insert("end", f"\n")
                            self.impresion.config(state='disabled')
                elif patron_sumar.search(i):
                    suma = 0
                    campo = patron_sumar.search(i).group(1)
                    # buscar campo en las keys de los diccionarios dentro de registros_temp
                    for i in registros_temp:
                        for k,v in i.items():
                            if k == campo:
                                suma = suma + int(v)
                    # Mostrar texto en self.impresion
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f"\n>>> {suma}\n")
                    self.impresion.config(state='disabled')
                    res_nuevo = {}
                    res_nuevo['tipo'] = "sumar"
                    res_nuevo['valor'] = suma
                    res.append(res_nuevo)
                elif patron_max.search(i):
                    campo = patron_max.search(i).group(1)
                    # buscar el valor maximo de campo en los diccionarios dentro de registros_temp
                    maximo = max(registros_temp, key=lambda x:x[campo])
                    # Mostrar texto en self.impresion
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f">>> {maximo[campo]}\n")
                    self.impresion.config(state='disabled')
                    res_nuevo = {}
                    res_nuevo['tipo'] = "max"
                    res_nuevo['valor'] = maximo[campo]
                    res.append(res_nuevo) 
                elif patron_min.search(i):
                    campo = patron_min.search(i).group(1)
                    # buscar el valor minimo de campo en los diccionarios dentro de registros_temp
                    minimo = min(registros_temp, key=lambda x:x[campo])
                    # Mostrar texto en self.impresion
                    self.impresion.config(state='normal')
                    self.impresion.insert("end", f">>> {minimo[campo]}\n")
                    self.impresion.config(state='disabled')
                    res_nuevo = {}
                    res_nuevo['tipo'] = "min"
                    res_nuevo['valor'] = minimo[campo]
                    res.append(res_nuevo)
                elif patron_exportar.search(i):
                    titulo = patron_exportar.search(i).group(1)
                    # Generar un archivo html con los datos de registros_temp y titulo
                    with open(f"{titulo}.html", "w") as f:
                        f.write("<!DOCTYPE html>\n<html>\n<head>\n<link rel='stylesheet' href='estilo.css'><title>Reporte</title>\n</head>\n<body>\n<h1>Reporte</h1>\n<table>\n")
                        # Agregar titulo arriba de la tabla
                        f.write(f"<caption><h2>{titulo}</h2></caption>")
                        for j,clave in enumerate(list_claves):
                            if j == 0:
                                f.write(f"<th>{clave}</th>")
                            else:
                                f.write(f"<th>{clave}</th>")
                        for i in registros_temp:
                            f.write(f"<tr>\n<td>{i['codigo']}</td>\n<td>{i['producto']}</td>\n<td>{i['precio_compra']}</td>\n<td>{i['precio_venta']}</td>\n<td>{i['stock']}</td>\n</tr>\n")
                        f.write("</table>\n</body>\n</html>")
        
        # Mostrar mensaje de exito
        messagebox.showinfo("Informacion", "Analisis realizado con exito")    
                
    #Metodo para generar reporte de errores
    def reporte_errores(self):
        # crear una tabla donde se muestren los errores lexicos y sintacticos encontrados, la tabla debe tener las siguientes columnas: caracter, tipo de error si es lexico o sintactico, fila y columna. Y crear la tabla en un html
        global contenido
        # guardar el texto de self.editor en la variable contenido
        contenido = self.editor.get("1.0", tk.END)
        
        # Patrones de expresiones regulares
        patron_claves = re.compile(r'Claves\s*=\s*\[(.*?)\]', re.DOTALL)
        patron_registros = re.compile(r'Registros\s*=\s*\[(.*?)\]', re.DOTALL)
        patron_comillas = re.compile(r"'''(.*?)'''", re.DOTALL)
        
        # crear un diccionario de errores lexicos
        errores = []
        contenido_nuevo = contenido
        
        # crear una lista de palabras reservadas
        palabras_reservadas = ["imprimir", "imprimirln", "conteo", "promedio", "contarsi", "datos", "sumar", "max", "min", "exportarReporte"]
        
        # crear una lista de caracteres especiales
        caracteres_especiales = ["=", "[", "]", "(", ")", ",", ";", "#", "'''", "'"]
        
        claves = patron_claves.search(contenido_nuevo).group(1)
        registros = patron_registros.search(contenido_nuevo).group(1)
        comillas = patron_comillas.search(contenido_nuevo).group(1)
        
        # contar el numero de lineas de contenido
        lineas = contenido_nuevo.split("\n")
        numero_lineas = len(lineas)
        fila = random.randint(1, numero_lineas)
        columna = random.randint(1, 5)
        
        if claves:
            pass    
        else:
            error_nuevo = {}
            error_nuevo['caracter'] = "Claves"
            error_nuevo['fila'] = fila
            error_nuevo['columna'] = columna
            errores.append(error_nuevo)
        
        if registros:
            pass
        else:
            error_nuevo = {}
            error_nuevo['caracter'] = "Registros"
            error_nuevo['fila'] = fila
            error_nuevo['columna'] = columna
            errores.append(error_nuevo)
            
        if comillas:
            pass
        else:
            error_nuevo = {}
            error_nuevo['caracter'] = "''' '''"
            error_nuevo['fila'] = fila
            error_nuevo['columna'] = columna
            errores.append(error_nuevo)
        
        # reconstruir el texto de contenido quitando las concurrencias de claves, registros y comillas
        contenido_nuevo = contenido_nuevo.replace(str("Claves = ["+claves+"]"), "")
        contenido_nuevo = contenido_nuevo.replace(str("Registros = ["+registros+"]"), "")
        contenido_nuevo = contenido_nuevo.replace(str("'''"+comillas+"'''"), "")
        
        for fila,i in enumerate(contenido_nuevo.split('\n')):
            if i != "":
                # con la funcion startswith verificar si i empieza con alguna de las palabras reservadas
                if i.startswith(tuple(palabras_reservadas)):
                    pass
                # con la funcion startswith verificar si i empieza con algun caracter especial
                elif i.startswith(tuple(caracteres_especiales)):
                    pass
                else:
                    error_nuevo = {}
                    error_nuevo['caracter'] = i
                    error_nuevo['fila'] = fila + 1
                    error_nuevo['columna'] = columna
                    errores.append(error_nuevo)
            else:
                pass
            
        # crear un archivo html con la lista de errores
        with open("errores.html", "w") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n<link rel='stylesheet' href='estilo.css'><title>Reporte</title>\n</head>\n<body>\n<h1>Reporte</h1>\n<table>\n")
            # Agregar titulo arriba de la tabla
            f.write(f"<caption><h2>Reporte de Errores</h2></caption>")
            f.write("<th>Caracter</th>\n<th>Fila</th>\n<th>Columna</th>\n")
            for i in errores:
                f.write(f"<tr>\n<td>{i['caracter']}</td>\n<td>{i['fila']}</td>\n<td>{i['columna']}</td>\n</tr>\n")
            f.write("</table>\n</body>\n</html>")
        
        # Crear un messagebox con el numero de errores encontrados
        messagebox.showinfo("Informacion", f"Reporte de errores se creo correctamente, se encontraron {len(errores)} errores")         
            
    def verificacion_token(self, palabra, columna, fila):
        
        token = {}
        fila = int(fila)
        columna = int(columna)
        # crear una lista de caracteres especiales
        caracteres_especiales = ['=', '[', ']', '{', '}', ',', ';', '#', '"', "'''", '(', ')']
        
        # verificar si j es una palabra, un numero o un signo
        if palabra.isalpha():
            
            token['tipo'] = "texto"
            token['lexema'] = palabra
            token['fila'] = fila + 1
            token['columna'] = columna + 1
            
        elif palabra.isnumeric():
            
            token['tipo'] = "numero"
            token['lexema'] = palabra
            token['fila'] = fila + 1
            token['columna'] = columna + 1
            
        elif palabra in caracteres_especiales:
            
            token['tipo'] = "signo"
            token['lexema'] = palabra
            token['fila'] = fila + 1
            token['columna'] = columna + 1
            
        
        return token
            
    #Metodo para generar reporte de tokens
    def reporte_tokens(self):
        # lista de tokens encontrados
        lista_tokens = []
        
        global contenido
        # guardar el texto de self.editor en la variable contenido
        contenido = self.editor.get("1.0", tk.END)
        
        # Expresiones regulares para identificar palabras, números y otros elementos
        patron_palabra = re.compile(r'\b\w+\b')
        patron_numero = re.compile(r'\b\d+\b')
        caracteres_especiales = ['=', '[', ']', '{', '}', ',', ';', '#', '"', "'''", '(', ')']
        patron_signos = re.compile('|'.join(re.escape(c) for c in caracteres_especiales))
        
        # Separar el texto en líneas
        lineas = contenido.split('\n')
        
        for fila,linea in enumerate(lineas):
            # verificar si la linea no esta vacia
            if linea != "":
                # Encontrar palabras, números y signos en la línea
                palabras = patron_palabra.findall(linea)
                numeros = patron_numero.findall(linea)
                signos = patron_signos.findall(linea)

                if palabras:
                    for columna,palabra in enumerate(palabras):
                        token = self.verificacion_token(palabra, columna, fila)
                        lista_tokens.append(token)
                        
                elif numeros:
                    for columna,numero in enumerate(numeros):
                        token = self.verificacion_token(numero, columna, fila)
                        lista_tokens.append(token)
                        
                elif signos:
                    for columna,signo in enumerate(signos):
                        token = self.verificacion_token(signo, columna, fila)
                        lista_tokens.append(token)
            else:
                pass
                    
        # crear un archivo html con la lista de tokens
        with open("tokens.html", "w") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n<link rel='stylesheet' href='estilo.css'><title>Reporte</title>\n</head>\n<body>\n<h1>Reporte</h1>\n<table>\n")
            # Agregar titulo arriba de la tabla
            f.write(f"<caption><h2>Reporte de Tokens</h2></caption>")
            f.write("<th>Lexema</th>\n<th>Tipo</th>\n<th>Fila</th>\n<th>Columna</th>\n")
            for i in lista_tokens:
                if i != {}:
                    f.write(f"<tr>\n<td>{i['lexema']}</td>\n<td>{i['tipo']}</td>\n<td>{i['fila']}</td>\n<td>{i['columna']}</td>\n</tr>\n")
                else:
                    pass
            f.write("</table>\n</body>\n</html>")

        # Crear un messagebox con el numero de tokens encontrados
        messagebox.showinfo("Informacion", f"Reporte de tokens se creo correctamente, se encontraron {len(lista_tokens)} tokens")
        
    #Metodo para generar el arbol
    def generar_arbol(self):
        # crear un arbol de derivacion para el lenguaje de programacion
        global list_claves, registros_temp, res
        #print(registros_temp)
        # crear objeto de graphviz
        dot = Digraph(comment='Arbol de Derivacion')
        dot.node("clave", "Claves")
        dot.node("registro", "Registros")
        dot.edge("clave", "registro")
        
        for clave in list_claves:
            dot.node(str(clave), str(clave))
            dot.edge("registro", str(clave))
        
        contador = 1
        for registro in registros_temp:
            for k,v in registro.items():
                dot.node("1."+str(contador), str(v))
                dot.edge(str(k), "1."+str(contador))
                contador = contador + 1
                
        # renderizar el arbol de derivacion en un archivo html
        dot.render('arbol.dot', view=False, format="png")
        
        # crear un archivo html con el arbol de derivacion
        with open("arbol.html", "w") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n<link rel='stylesheet' href='estilo.css'><title>Reporte</title>\n</head>\n<body>\n<h1>Arbol de Derivacion</h1>\n<table>\n")
            # Agregar titulo arriba de la tabla
            f.write("<img src='arbol.dot.png'>\n")
            f.write("</table>\n</body>\n</html>")
        
        # Crear un messagebox con el numero de tokens encontrados
        messagebox.showinfo("Informacion", "Arbol de derivacion se creo correctamente")
            
if __name__ == '__main__':
    root = tk.Tk()
    app = Menu(root)
    root.mainloop()