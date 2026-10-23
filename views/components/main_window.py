# Ventana raíz y controlador de navegación de la interfaz.
# Conserva un contenedor común y reemplaza su pantalla hija cuando cambia la vista.
# Referencia: docs/estudio/README.md#tkinter-y-programación-dirigida-por-eventos
import tkinter as tk
from tkinter import ttk
from views.login_view.login_view import login_view

# Hereda de `tk.Tk`: cada instancia representa la ventana principal de LibManage.
class MainWindow(tk.Tk):
    
    # Configura la ventana, crea el contenedor e inicia mostrando el login.
    def __init__(self):
        super().__init__()
        
        # Configuracion de la ventana
        self.title("LibManage")
        self.centrar_pantalla()
        self.resizable(True, True)
        
        self._crear_header()
        
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.show_frame(login_view)
        
    # Recibe una clase de vista y datos opcionales; destruye la vista anterior
    # y crea una nueva dentro del mismo contenedor.
    def show_frame(self, frame_class, datos=None):
        
        for widget in self.container.winfo_children():
            widget.destroy()
        
        if datos is not None:
            frame = frame_class(self.container, self, datos)
            frame.pack(fill="both", expand=True)
        else:
            frame = frame_class(self.container, self)
            frame.pack(fill="both", expand=True)
        
    # Construye el encabezado visual compartido por todas las pantallas.
    def _crear_header(self):
        header = ttk.Frame(self, style="Header.TFrame")
        header.pack(fill="x")

        inner = ttk.Frame(header, style="Header.TFrame")
        inner.pack(fill="x", ipadx=24, ipady=28)
        
        #Titulo - Esto tambien se podria factorizar?
        ttk.Label(
            inner,
            text="LibManage",style="HeaderTitle.TLabel"
        ).pack()
        
        #subtitulo
        ttk.Label(inner,
                  text="Gestor de libros y prestamos",
                  style="HeaderSubTitle.TLabel").pack(pady=(2,0))
        
    # Calcula coordenadas a partir del tamaño de pantalla y fija la geometría inicial.
    def centrar_pantalla(self):
        """Funcion para sentrar la aplicacion en el medio de la pantalla"""
        ancho = 800
        alto = 600
        ancho_pantalla = self.winfo_screenwidth() #? Calcula el tamañno de la pantalla
        alto_pantalla = self.winfo_screenheight() 

        x = (ancho_pantalla - ancho) // 2 #? Se la divide en 2 para sacar la cordenada
        y = (alto_pantalla - alto) // 2 #? Del "Punto MEdio"
        self.geometry(f"{ancho}x{alto}+{x}+{y}") #? Se establece el tamaño de la app y se le pasa la cordenada a la que debe ir