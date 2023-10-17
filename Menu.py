import tkinter as tk
from tkinter import filedialog, messagebox
import re

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
        self.editor = tk.Text(self.root, width=65, height=30)
        self.editor.place(x=20, y=100)
        
        # creat un text area para la impresion
        self.impresion = tk.Text(self.root, width=35, height=30)
        self.impresion.config(state='disabled')
        self.impresion.place(x=580, y=100)
        
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
        global contenido
        list_claves = []
        list_registros = []
        # guardar el texto de self.editor en la variable contenido
        contenido = self.editor.get("1.0", tk.END)
        
        # Patrones de expresiones regulares
        patron_claves = re.compile(r'Claves\s*=\s*\[(.*?)\]', re.DOTALL)
        patron_signos = re.compile(r'[\'\"\s\n]+')
        patron_registros = re.compile(r'Registros\s*=\s*\[(.*?)\]', re.DOTALL)
        
        # buscar el patron en contenido y extraer el texto
        claves = patron_claves.search(contenido).group(1)
        # buscar con el patron_signos y extraer el texto
        claves = patron_signos.sub("", claves)
        # buscar hasta donde se encuentre una coma y guardar cada palabra en list_claves
        for clave in claves.split(","):
            list_claves.append(clave)
        
        registros = patron_registros.search(contenido).group(1)
        registros = patron_signos.sub("", registros)
        # a travez de un for buscar desde "{" hasta "}" y guardar cada palabra en list_registros
        for registro in registros.split("}"):
            list_registros.append(registro)
        print(list_registros)
        
            
        
        
        
            
                
        
        

        
        
    
    #Metodo para generar reporte de errores
    def reporte_errores(self):
        pass
    
    #Metodo para generar reporte de tokens
    def reporte_tokens(self):
        pass
    
    #Metodo para generar el arbol
    def generar_arbol(self):
        pass
        
        
if __name__ == '__main__':
    root = tk.Tk()
    app = Menu(root)
    root.mainloop()