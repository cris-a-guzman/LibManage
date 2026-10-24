"""Pantalla de gestion de libros de LibManage.

Muestra el listado de libros en una tabla y permite:
    - Buscar por titulo, autor o ISBN.
    - Ordenar alfabeticamente por titulo.
    - Crear un libro nuevo.
    - Modificar el libro seleccionado (boton o doble click).
    - Volver al inicio.

Gran parte de la pantalla (barra de busqueda, botones, tabla) se arma con
metodos heredados de BaseFrame; aca solo se eligen y se configuran.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame

class GestionLibros(BaseFrame):
    """Pantalla con el listado de libros y las acciones para gestionarlos."""

    def __init__(self, parent, controller):
        """Arma la pantalla: pide los libros a la base, crea los controles y llena la tabla.

        Args:
            parent: Frame contenedor donde se dibuja esta pantalla (el container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar de pantalla.
        """
        super().__init__(parent, controller)
        self.controller = controller #* Guardamos la ventana principal para poder navegar a otras pantallas
            #? Frame principal

        # ? Traer libros de la base de datos
        #? Se piden UNA sola vez al abrir la pantalla y se guardan en self.libros_datos.
        #? Buscar y ordenar trabajan sobre esta lista, sin volver a consultar la base.
        #? Como show_frame recrea la pantalla cada vez que se entra, la lista siempre llega actualizada.
        self.libros_datos = self.ApiLibros.listar_libros()
        self.frame_central = self.crear_frame_central() #* Frame donde va todo el contenido (metodo de BaseFrame)

        #? Titulo
        self.crear_titulo("Gestion de Libro")
        self.frame_central.columnconfigure((0,1), weight=1) #* Dos columnas que se reparten el ancho por igual
        self.frame_central.rowconfigure(2, weight=1) #? La fila 2 (la de la tabla) es la que se estira al agrandar la ventana

        #? Barra de busqueda
        #? Se le pasa self.buscar SIN parentesis: es la funcion que se va a ejecutar al buscar (no se ejecuta ahora)
        self.crear_barra_busqueda("Buscar Libro", self.buscar)

        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #? --- Tabla de Libros
        self.frame_libros = tk.Frame(self.frame_central)
        self.frame_libros.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        self.frame_libros.rowconfigure(0, weight=1)
        self.frame_libros.columnconfigure(0, weight=1)

        #? Nombres de las columnas y el ancho de cada una (en pixeles). Van en el mismo orden:
        #? id_libro=50, isbn=120, titulo=200, autor=150, anio=60, cantidad_total=80
        columnas = ("id_libro", "isbn", "titulo", "autor", "anio", "cantidad_total")
        ancho = (50,120,200,150,60,80)
        modo = "browse" #? "browse" = se puede seleccionar una sola fila a la vez
        #? crear_treeview (de BaseFrame) arma la tabla y la deja guardada en self.tabla
        self.crear_treeview(self.frame_libros, columnas,ancho, modo)

        #? Doble clic sobre una fila = modificar ese libro
        #! A esto lo podriamos pasar al general creo
        #? "<Double-1>" = doble click izquierdo. El lambda recibe el evento (e) pero no lo usa.
        self.tabla.bind("<Double-1>", lambda e: self.modificar_seleccionado())

        self.frame_inferior.columnconfigure(2, weight=1) #* La columna 2 de la barra de botones de abajo se estira (ahi va "Modificar")

        #? Boton Crear Libro
        self.crear_boton_crear("Crear Libro", self.crear_libro)

        #? Boton Volver Atras
        self.crear_boton_volver(self.volver_atras)

        #? Boton Modificar (actua sobre la fila seleccionada)
        #? Este boton se crea a mano (no con un metodo de BaseFrame) y se ubica en la columna 2
        btn_modificar = tk.Button(
            self.frame_inferior,
            text="Modificar",
            command=self.modificar_seleccionado
        )
        btn_modificar.grid(row=0, column=2, sticky="ew", padx=(10,10), pady=(10, 0), ipady=6)

        #* Por ultimo se llena la tabla con todos los libros
        self.actualizar_tabla(self.libros_datos)

    def actualizar_tabla(self, lista_libros):
        """Borra las filas de la tabla y la vuelve a llenar con la lista recibida.

        Args:
            lista_libros (list[dict]): Libros a mostrar. Cada dict necesita las claves
                "id_libro", "isbn", "titulo", "autor", "anio" y "cantidad_total".
        """
        #*-- Primero se borran todas las filas actuales
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        #*-- Despues se agrega una fila por cada libro
        #? "" = sin padre (fila de primer nivel), "end" = la agrega al final.
        #? El orden de values tiene que coincidir con el orden de las columnas de la tabla.
        for libro in lista_libros:
            self.tabla.insert(
                "",
                "end",
                values=(
                    libro["id_libro"],
                    libro["isbn"],
                    libro["titulo"],
                    libro["autor"],
                    libro["anio"],
                    libro["cantidad_total"],
                )
            )

    def buscar(self):
        """Filtra la tabla por el texto de la barra de busqueda (titulo, autor o ISBN).

        Si la barra esta vacia (o tiene el texto de ejemplo), muestra todos los libros.
        La busqueda no distingue mayusculas de minusculas.
        """
        texto = self.busqueda.get().strip().lower() #? Pasamos todo a minusculas para comparar sin importar mayusculas
        #? Si no escribio nada (o quedo el texto de ejemplo) mostramos todo y cortamos
        if not texto or texto == "barra de busqueda":
            self.actualizar_tabla(self.libros_datos)
            return

        #? List comprehension: arma una lista nueva solo con los libros donde el texto
        #? aparece en el titulo, en el autor o en el ISBN ("in" = "esta contenido en").
        #? El ISBN puede ser NULL en la base (llega como None): "l['isbn'] or ''" lo cambia por ""
        #? asi str() y lower() no fallan.
        resultados = [
            l for l in self.libros_datos
            if texto in l["titulo"].lower()
            or texto in l["autor"].lower()
            or texto in str(l["isbn"] or "").lower()
        ]
        self.actualizar_tabla(resultados)

    def ordenar(self):
        """Muestra los libros ordenados alfabeticamente por titulo (de la A a la Z)."""
        #? sorted() devuelve una lista nueva ordenada (no modifica self.libros_datos).
        #? key=lambda x: x["titulo"] le dice por que campo ordenar.
        libros_ordenados = sorted(self.libros_datos, key=lambda x: x["titulo"])
        self.actualizar_tabla(libros_ordenados)

    def filtrar(self):
        """Limpia la barra de busqueda y vuelve a mostrar todos los libros."""
        self.busqueda.delete(0, tk.END) #* Borra el texto de la barra (de la posicion 0 hasta el final)
        self.actualizar_tabla(self.libros_datos)

    def crear_libro(self):
        """Va a la pantalla para crear un libro nuevo (boton "Crear Libro")."""
        #? El import esta aca adentro y no arriba del archivo, seguramente para evitar un
        #? "import circular" (CrearLibro tambien importa a esta pantalla).
        from views.libros_views.crear_libro_view import CrearLibro
        self.controller.show_frame(CrearLibro)

    def modificar_seleccionado(self):
        """Busca el libro elegido en la tabla y abre la pantalla para modificarlo.

        Se ejecuta con el boton "Modificar" o con doble click sobre una fila.
        Si no hay ninguna fila seleccionada, muestra un aviso.
        """
        seleccion = self.tabla.selection() #* Devuelve las filas seleccionadas
        if not seleccion: #* Si no hay ninguna, avisamos y cortamos
            messagebox.showwarning(
                "Atención", "Por favor, seleccioná un libro de la lista."
            )
            return

        #? .item(...)["values"] devuelve los valores de la fila; el [0] es la primera columna (el id_libro)
        id_libro = self.tabla.item(seleccion[0])["values"][0]
        #? next(generador, None) devuelve el primer libro cuyo id coincide, o None si no hay ninguno.
        #? Asi recuperamos el diccionario completo del libro a partir del ID de la fila.
        libro = next((l for l in self.libros_datos if l["id_libro"] == id_libro), None)
        self.modificar_libro(libro)

    def modificar_libro(self, libro=None):
        """Abre la pantalla de modificacion, pasandole los datos del libro.

        Args:
            libro (dict | None): Datos del libro a modificar.
        """
        #? Import dentro de la funcion por el mismo motivo que en crear_libro (evitar import circular)
        from views.libros_views.modificar_libro_view import ModificarLibro
        #? El tercer valor (libro) es el parametro "datos" de show_frame: llega a la pantalla nueva
        self.controller.show_frame(ModificarLibro, libro)

    def volver_atras(self):
        """Vuelve a la pantalla de inicio (boton "Volver")."""
        #? Import dentro de la funcion por el mismo motivo que en crear_libro (evitar import circular)
        from views.home_view.home_view import HomeView
        self.controller.show_frame(HomeView)