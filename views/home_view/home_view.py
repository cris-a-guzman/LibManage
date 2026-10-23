import tkinter as tk
from tkinter import ttk
from views.libros_views.gestion_libros_view import GestionLibros
from views.prestamos_views.gestion_prestamos_view import GestionPrestamos
from views.socio_views.gestion_socios_view import GestionSocios
from views.components.base_frame import BaseFrame


class HomeView(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        
        datos_libro = [
            ("Cantidad de Libros:", self.ApiLibros.cantidad_total_ejemplares()),
            ("Libros Prestados:", (self.ApiLibros.cantidad_ejemplares_prestados())),
            ("Libros Disponibles:", (self.ApiLibros.cantidad_total_ejemplares() - self.ApiLibros.cantidad_ejemplares_prestados())),
        ]
        
        
        datos_prestamos = [
            ("Prestamos Activos:", self.ApiPrestamos.cantidad_prestamos_activos()),
            ("Prestamos Finalizados:", self.ApiPrestamos.cantidad_prestamos_finalizados()),
            ("Prestamos Con Atraso:", self.ApiPrestamos.cantidad_prestamos_atraso()),
        ]
        
        datos_socios = [ 
            ("Cantidad de Socios:", self.ApiSocios.cantidad_socios()),
            ("Socios Con Prestamos:", self.ApiSocios.cantidad_socios_prestamos())
            ]
        
        self.crear_titulo("Inicio")
        
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
        
        self.subtitulo = tk.Label(
            self.frame_central,
            text="Resumen",
            font=("Arial", 14, "bold"),
            pady=8,
            padx=8
        )
        self.subtitulo.grid(row=1, column=1, sticky="nsew", padx=10, pady=(10,5)) 
        
        self.tree_libros = self.crear_tree(self.frame_central,0)
        self.renderizar_datos(datos_libro, self.tree_libros)
        
        self.tree_prestamos = self.crear_tree(self.frame_central, 1)
        self.renderizar_datos(datos_prestamos, self.tree_prestamos)
        
        self.tree_socios = self.crear_tree(self.frame_central, 2)
        self.renderizar_datos(datos_socios, self.tree_socios)        
        
    def crear_tree(self, frame_parent, col):
        columnas = {
            "atributo":150,
            "valor":50
        }
        tree = ttk.Treeview(frame_parent,
                                 columns=tuple(columnas.keys()),
                                 show="tree",
                                 height=4)
        tree.grid(row=2, column=col, padx=15, pady=10, sticky="nsew")
        
        tree.column("#0", width=0, stretch=False)
        for clave, valor in columnas.items():
            tree.column(clave, width=valor, stretch=False)
            
        return tree

    def renderizar_datos(self, datos, tree):
        for clave, valor in datos:
            tree.insert("", "end", values=(clave, valor))