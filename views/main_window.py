import tkinter as tk
from tkinter import ttk
from views.login_view import login_view

class MainWindow(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        # Configuracion de la ventana
        self.title("LibManage")
        self.geometry("800x600")
        self.resizable(False, False)
        
        self._crear_header()
        
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        self.show_frame(login_view)
        
    def show_frame(self, frame_class, datos=None):
        
        for widget in self.container.winfo_children():
            print(widget)
            widget.destroy()
        
        if datos is not None:
            frame = frame_class(self.container, self, datos)
            frame.pack(fill="both", expand=True)
        else:
            frame = frame_class(self.container, self)
            frame.pack(fill="both", expand=True)
        
    def _crear_header(self):
        
        header = ttk.Frame(self, style="Header.TFrame")
        header.pack(fill="x")

        inner = ttk.Frame(header, style="Header.TFrame")
        inner.pack(fill="x", ipadx=24, ipady=28)
        
        #Titulo
        ttk.Label(
            inner,
            text="LibManage",style="HeaderTitle.TLabel"
        ).pack()
        
        #subtitulo
        ttk.Label(inner,
                  text="Gestor de libros y prestamos",
                  style="HeaderSubTitle.TLabel").pack(pady=(2,0))
        
    
        
