"""Pantalla de inicio (Home) de LibManage.

Muestra tres botones para ir a las pantallas de gestion (libros, prestamos y
socios) y, debajo, un resumen con estadisticas generales en tres tablas.
"""

import tkinter as tk
from tkinter import ttk
from views.libros_views.gestion_libros_view import GestionLibros
from views.prestamos_views.gestion_prestamos_view import GestionPrestamos
from views.socio_views.gestion_socios_view import GestionSocios
from views.components.base_frame import BaseFrame


class HomeView(BaseFrame):
    """Pantalla de inicio: botones de navegacion + resumen de estadisticas.

    Hereda de BaseFrame, que (se define en views/components/base_frame.py)
    nos da cosas ya armadas como self.frame_central, self.crear_titulo() y
    los accesos a los datos: self.ApiLibros, self.ApiPrestamos, self.ApiSocios.
    """

    def __init__(self, parent, controller):
        """Arma toda la pantalla: calcula los datos, crea los botones y las tablas.

        Args:
            parent: Frame contenedor donde se va a dibujar esta pantalla
                (es el self.container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar
                de pantalla con controller.show_frame(...).
        """
        super().__init__(parent, controller) #* Esta linea lo que hace es traer todos los atributos de la clase padre
                                            #* O sea BASEFRAME

        #*-- Datos del resumen
        #? Cada lista tiene tuplas (texto que se ve, valor numerico).
        #? Los valores se piden a la capa de datos (Api...) cada vez que se abre la pantalla,
        #? por eso siempre se ven actualizados.
        datos_libro = [
            ("Cantidad de Libros:", self.ApiLibros.cantidad_total_ejemplares()), #* Self explanatory
            ("Libros Prestados:", (self.ApiLibros.cantidad_ejemplares_prestados())),
            #? Disponibles = total de ejemplares - los que estan prestados en este momento
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

        self.crear_titulo("Inicio") #* Pone el titulo de la pantalla (metodo heredado de BaseFrame)

        #? Le decimos al frame central que tiene 3 columnas (0, 1 y 2) y que las 3
        #? se reparten el ancho por igual (weight=1). Asi los botones y las tablas quedan alineados.
        self.frame_central.columnconfigure((0,1,2), weight=1)

        #*-- Creamos los botones principales
        #? Usamos lambda para que show_frame se ejecute RECIEN cuando se hace click.
        #? Si pusieramos command=controller.show_frame(GestionLibros) se ejecutaria al crear el boton.
        ttk.Button(
            self.frame_central,
            text="Gestión de Libros",
            style="Dashboard.TButton", #* Estilo definido aparte (colores, fuente, etc.)
            padding=(20,20), #* Espacio interno del boton (lo hace mas grande)
            command=lambda: controller.show_frame(GestionLibros) #* Le decimos que si hace click en este boton nos lleve a la pantalla de Gestion de Libros
        ).grid(row=0, column=0, padx=15, pady=10, sticky="ew") #* sticky="ew" estira el boton a lo ancho de su columna

        ttk.Button(
            self.frame_central,
            text="Gestión de Préstamos",
            style="Dashboard.TButton",
            padding=(20,20),
            command=lambda: controller.show_frame(GestionPrestamos) #* Le decimos que si hace click en este boton nos lleve a la pantalla de Gestion de prestamos
        ).grid(row=0, column=1, padx=15, pady=10, sticky="ew")

        ttk.Button(
            self.frame_central,
            text="Gestión de Socios",
            style="Dashboard.TButton",
            padding=(20,20),
            command=lambda: controller.show_frame(GestionSocios) #* Le decimos que si hace click en este boton nos lleve a la pantalla de Gestion de socios
        ).grid(row=0, column=2, padx=15, pady=10, sticky="ew")

        #*-- Subtitulo "Resumen" (queda en la columna del medio, entre los botones y las tablas)
        self.subtitulo = tk.Label(
            self.frame_central,
            text="Resumen",
            font=("Arial", 14, "bold"),
            pady=8,
            padx=8
        )
        self.subtitulo.grid(row=1, column=1, sticky="nsew", padx=10, pady=(10,5))

        #*-- Tablas del resumen: una por columna (0 = libros, 1 = prestamos, 2 = socios)
        #? Siempre son 2 pasos: primero se crea la tabla vacia y despues se la llena con los datos.
        self.tree_libros = self.crear_tree(self.frame_central,0)
        self.renderizar_datos(datos_libro, self.tree_libros)

        self.tree_prestamos = self.crear_tree(self.frame_central, 1)
        self.renderizar_datos(datos_prestamos, self.tree_prestamos)

        self.tree_socios = self.crear_tree(self.frame_central, 2)
        self.renderizar_datos(datos_socios, self.tree_socios)

    def crear_tree(self, frame_parent, col):
        """Crea un Treeview vacio de 2 columnas (atributo y valor) y lo ubica en la grilla.

        Args:
            frame_parent: Frame donde se va a dibujar la tabla.
            col (int): Numero de columna de la grilla donde se coloca (0, 1 o 2).

        Returns:
            ttk.Treeview: La tabla ya creada y ubicada, lista para llenarla
            con renderizar_datos().
        """
        columnas = { #* Aca establecemos los nombres de las columnas ("atributo") y el tamaño (150)
            "atributo":150,
            "valor":50
        }
        tree = ttk.Treeview(frame_parent,
                                 columns=tuple(columnas.keys()), #* Pasa solo los nombres: ("atributo", "valor")
                                 show="tree", #? "tree" oculta la fila de encabezados, solo se ven los datos
                                 height=4) #* Cantidad de filas visibles a la vez
        tree.grid(row=2, column=col, padx=15, pady=10, sticky="nsew")

        #? Todo Treeview trae una columna extra "#0" (la del arbol con las flechitas).
        #? Como no la usamos, la dejamos con ancho 0 y sin poder estirarse para que no se vea.
        tree.column("#0", width=0, stretch=False)
        for clave, valor in columnas.items(): #* Crea las columnas
            tree.column(clave, width=valor, stretch=False) #* stretch=False: mantiene el ancho fijo aunque se agrande la ventana

        return tree

    def renderizar_datos(self, datos, tree):
        """Inserta las filas en un Treeview, una por cada par (atributo, valor).

        Args:
            datos (list[tuple]): Lista de tuplas (texto, valor). Ej: ("Libros Prestados:", 12).
            tree (ttk.Treeview): Tabla donde se van a insertar las filas.
        """
        for clave, valor in datos: #* Recorre los datos dentro de Datos
            #? "" = sin padre (fila de primer nivel) y "end" = la agrega al final de la tabla
            tree.insert("", "end", values=(clave, valor)) #* Los inserta en el treeView