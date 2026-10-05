import tkinter as tk
from tkinter import ttk
from views.gestion_libros_view import GestionLibros
from views.gestion_prestamos_view import GestionPrestamos
from views.gestion_socios_view import GestionSocios
from views.components.base_frame import BaseFrame


class HomeView(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        #? Datos de ejemplo, esto deberia traer la db
        datos_libro = [
            ("Cantidad de Libros:", "120"),
            ("Libros Prestados:", "15"),
            ("Libros Disponibles:", "105"),
        ]
        
        datos_prestamos = [
            ("Prestamos Activos:", "32"),
            ("Prestamos Finalizados:", "23"),
            ("Prestamos Con Atraso:", "6"),
        ]
        
        datos_socios = [
            ("Cantidad de Socios:", "54"),
                ("Socios Con Prestamos:", "23")
            ]
        
        self.crear_titulo("Dashboard")
        
        self.frame_central.columnconfigure((0,1,2), weight=1)
        
        #?-- Botones centrales
        ttk.Button(
            self.frame_central,
            text="📚 Gestión de Libros",
            style="Dashboard.TButton",
            padding=(20,20),
            command=lambda: controller.show_frame(GestionLibros)
        ).grid(row=0, column=0, padx=15, pady=10, sticky="ew")
        
        ttk.Button(
            self.frame_central,
            text="🔄 Gestión de Préstamos",
            style="Dashboard.TButton",
            padding=(20,20),
            command=lambda: controller.show_frame(GestionPrestamos)
        ).grid(row=0, column=1, padx=15, pady=10, sticky="ew")
        
        ttk.Button(
            self.frame_central,
            text="👥 Gestión de Socios",
            style="Dashboard.TButton",
            padding=(20,20),
            command=lambda: controller.show_frame(GestionSocios)
        ).grid(row=0, column=2, padx=15, pady=10, sticky="ew")
        
        
        #? 
        self.subtitulo = tk.Label(
            self.frame_central,
            text="Resumen",
            font=("Arial", 14, "bold"),
            pady=8,
            padx=8
        )
        self.subtitulo.grid(row=1, column=1, sticky="nsew", padx=10, pady=(10,5))
        
        self.crear_tree_libros()
        self.renderizar_datos(datos_libro, self.tree_libros)
        
        self.crear_tree_socios()
        self.renderizar_datos(datos_socios, self.tree_socios)
        self.crear_tree_prestamos()
        self.renderizar_datos(datos_prestamos, self.tree_prestamos)
        
    
    def crear_tree_libros(self):
        self.tree_libros = ttk.Treeview(self.frame_central,
                                        columns=("atributo", "valor"),
                                        show="tree",
                                        height=4
                                        )
        self.tree_libros.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")
        self.tree_libros.column("#0", width=0, stretch=False)
        self.tree_libros.column("atributo", width=150, anchor="w")
        self.tree_libros.column("valor", width=50, anchor="center")
        
    def crear_tree_prestamos(self):
        self.tree_prestamos = ttk.Treeview(self.frame_central,
                                           columns=("atributo", "valor"),
                                           show="tree",
                                           height=4
                                           )
        self.tree_prestamos.grid(row=2, column=1, padx=15, pady=10, sticky="nsew")
        self.tree_prestamos.column("#0", width=0, stretch=False)
        self.tree_prestamos.column("atributo", width=150, anchor="w")
        self.tree_prestamos.column("valor", width=50, anchor="center")
        
    def crear_tree_socios(self):
        self.tree_socios = ttk.Treeview(self.frame_central,
                                        columns=("atributo", "valor"),
                                        show="tree",
                                        height=4
                                        )
        self.tree_socios.grid(row=2, column=2, padx=15, pady=10, sticky="nsew")
        self.tree_socios.column("#0", width=0, stretch=False)
        self.tree_socios.column("atributo", width=150, anchor="w")
        self.tree_socios.column("valor", width=50, anchor="center")
        


    def renderizar_datos(self, datos, tree):
        for clave, valor in datos:
            tree.insert("", "end", values=(clave, valor))