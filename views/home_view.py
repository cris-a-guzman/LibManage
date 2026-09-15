import tkinter as tk
from tkinter import ttk
from views.gestion_libros_view import GestionLibros

class HomeView(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        
        tk.Label(
            self,
            text="Pantalla Dashboard"
        ).grid(row=0, column=0, sticky="ew")
        
        self.rowconfigure(1, weight=1)
        
        
        #?--- Frame central
        self.inicio = tk.Frame(self)
        
        self.inicio.columnconfigure(0, weight=1)
        self.inicio.columnconfigure(1, weight=1)
        self.inicio.columnconfigure(2, weight=1)
        
        self.inicio.grid(row=1)
        
        #?-- Botones centrales
        ttk.Button(
            self.inicio,
            text="📚 Gestión de Libros",
            style="Dashboard.TButton",
            padding=(20,15),
            command=lambda: controller.show_frame(GestionLibros)
        ).grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        
        ttk.Button(
            self.inicio,
            text="🔄 Gestión de Préstamos",
            style="Dashboard.TButton",
            padding=(20,15)
        ).grid(row=0, column=1, padx=15, pady=10, sticky="ew")
        
        ttk.Button(
            self.inicio,
            text="👥 Gestión de Socios",
            style="Dashboard.TButton",
            padding=(20,15)
        ).grid(row=0, column=2, padx=15, pady=10, sticky="ew")
        
        self.rowconfigure(2, weight=1)
        
        #?--- Frame inferior/footer
        self.listas = ttk.Frame(self)
        self.listas.grid(row=2, column=0, padx=20, pady=(0, 30), sticky="nsew")
        self.listas.columnconfigure((0, 1, 2), weight=1)
        self.listas.rowconfigure(0, weight=1)
        
        
        #?--- Secciones del footer
        self.lista_libros = ttk.Frame(self.listas)
        self.lista_libros.grid(row=0, column=0, padx=15, sticky="nsew")
        self.lista_libros.columnconfigure(0, weight=1)
        self.lista_prestamos = ttk.Frame(self.listas)
        self.lista_prestamos.grid(row=0,column=1, sticky="nsew")
        self.lista_socios = ttk.Frame(self.listas)
        self.lista_socios.grid(row=0,column=2, sticky="nsew")
        
        #?--- Label de la seccion izq del footer
        
        ttk.Label(self.lista_libros, text="Cantidad de Libros en biblioteca:").grid(sticky="ew")
        
        
        #?--- Labels de la seccion centro del footer
        
        ttk.Label(self.lista_prestamos, text="Cantidad de Prestamos").grid(row=0,column=0,padx=15,pady=3,sticky="w")
        ttk.Label(self.lista_prestamos, text="4").grid(row=0,column=1,padx=15,pady=3,sticky="w")
        
        ttk.Label(self.lista_prestamos, text="Prestamos completos:").grid(row=1,column=0,padx=15,pady=3,sticky="w")
        ttk.Label(self.lista_prestamos, text="4").grid(row=1,column=1,padx=15,pady=3,sticky="w")
        
        ttk.Label(self.lista_prestamos, text="Prestamos pendientes:").grid(row=2,column=0,padx=15,pady=3,sticky="w")
        ttk.Label(self.lista_prestamos, text="4").grid(row=2,column=1,padx=15,pady=3,sticky="w")
        # probando = [1,2,3]
        # for i in probando:
        #     ttk.Label(self.lista_prestamos, text=str(i)).grid()
        
        
        #?--- Labels de la seccion der del footer
        ttk.Label(self.lista_socios, text="Cantidad de socios:").grid()
        ttk.Label(self.lista_socios, text="Socios con prestamos:").grid()