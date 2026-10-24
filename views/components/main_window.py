import tkinter as tk
from tkinter import ttk
from views.home_view.home_view import HomeView

class MainWindow(tk.Tk):
    """Ventana principal del programa"""
    def __init__(self):
        super().__init__()
        
        # Configuracion de la ventana
        self.title("LibManage") #* Titulo
        self.centrar_pantalla() #* Llama a la funcion para centrar la pantalla
        self.resizable(True, True) #* No permite el usuario modifique el tamaño de la ventana
        
        self._crear_header()
        
        self.container = ttk.Frame(self) #* Crea el frame el cual vamos a ir llenando de elementos
        self.container.pack(fill="both", expand=True) #* lo ubica en la ventana principal
        
        self.show_frame(HomeView) #* Esto manda a mostrar la pantalla de home_view
        
    def show_frame(self, frame_class, datos=None):
        """Esta funcion refresca la ventana principal y ubica los elementos de la pantalla que 
        Queremos mostrar realmente
        Seria lo que se hace por detras de cuando hacemos INICIO -> GESTION_PRESTAMO"""
        
        for widget in self.container.winfo_children(): #? Recorre todos los elementos dentro
                                                        #? De la ventana y elimina los elementos
                                                        #? Para dejarla limpia y poder meter los nuevos elementos de la pantalla elegida
            widget.destroy() #* Esto los borra, uno por uno
        
        if datos is not None: #* Si tenemos datos entonces se lo pasamos a la respectiva pantalla para que lo muestre
            frame = frame_class(self.container, self, datos)
            frame.pack(fill="both", expand=True)
        else: #* Si no pasamos datos entonces simplemente mostramos la pantalla
            frame = frame_class(self.container, self)
            frame.pack(fill="both", expand=True)
        
    def _crear_header(self):
        """Se crea el Header de la pantalla que vamos a mostrar"""
        header = ttk.Frame(self, style="Header.TFrame")
        header.pack(fill="x")

        inner = ttk.Frame(header, style="Header.TFrame")
        inner.pack(fill="x", ipadx=24, ipady=28)
        
        #* Titulo 
        ttk.Label(
            inner,
            text="LibManage",style="HeaderTitle.TLabel"
        ).pack()
        
        #* subtitulo
        ttk.Label(inner,
                  text="Gestor de libros y prestamos",
                  style="HeaderSubTitle.TLabel").pack(pady=(2,0))
        
    def centrar_pantalla(self):
        """Funcion para sentrar la aplicacion en el medio de la pantalla"""
        ancho = 800
        alto = 600
        ancho_pantalla = self.winfo_screenwidth() #? Calcula el tamañno de la pantalla
        alto_pantalla = self.winfo_screenheight() 

        x = (ancho_pantalla - ancho) // 2 #? Se la divide en 2 para sacar la cordenada
        y = (alto_pantalla - alto) // 2 #? Del "Punto MEdio"
        self.geometry(f"{ancho}x{alto}+{x}+{y}") #? Se establece el tamaño de la app y se le pasa la cordenada a la que debe ir