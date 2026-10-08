import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame

class GestionLibros(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        #? Datos de prueba con los mismos campos que la tabla libro de la BD
        self.libros_datos = self.API.traer_libros()
        #? Frame principal
        self.frame_central = self.crear_frame_central()

        #? Titulo
        self.crear_titulo("Gestion de Libro")

        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.columnconfigure(1, weight=1) #? Esto tambien se podria refactorizar
        self.frame_central.rowconfigure(2, weight=1)

        #? Barra de busqueda
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

        columnas = ("id_libro", "isbn", "titulo", "autor", "anio", "cantidad_total")
        ancho = (50,120,200,150,60,80)
        modo = "browse"
        self.crear_treeview(columnas,ancho, modo)

        #? Doble clic sobre una fila = modificar ese libro
        self.tabla.bind("<Double-1>", lambda e: self.modificar_seleccionado())

        #? Boton Modificar (actua sobre la fila seleccionada)
        btn_modificar = tk.Button(
            self.frame_libros,
            text="Modificar",
            command=self.modificar_seleccionado
        )
        btn_modificar.grid(row=1, column=0, columnspan=2, sticky="e", pady=(5, 0))

        self.actualizar_tabla(self.libros_datos)

        #? Boton Crear Libro
        self.crear_boton_crear("Crear Libro", self.modificar_libro)

        #? Boton Volver Atras
        self.crear_boton_volver(self.volver_atras)

    def actualizar_tabla(self, lista_libros):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

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
        texto = self.busqueda.get().strip().lower()
        if not texto or texto == "barra de busqueda":
            self.actualizar_tabla(self.libros_datos)
            return

        resultados = [
            l for l in self.libros_datos
            if texto in l["titulo"].lower()
            or texto in l["autor"].lower()
            or texto in str(l["isbn"] or "").lower()
        ]
        self.actualizar_tabla(resultados)

    def ordenar(self):
        libros_ordenados = sorted(self.libros_datos, key=lambda x: x["titulo"])
        self.actualizar_tabla(libros_ordenados)

    def filtrar(self):
        self.busqueda.delete(0, tk.END)
        self.actualizar_tabla(self.libros_datos)

    def modificar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atención", "Por favor, seleccioná un libro de la lista."
            )
            return

        id_libro = self.tabla.item(seleccion[0])["values"][0]
        libro = next((l for l in self.libros_datos if l["id_libro"] == id_libro), None)
        self.modificar_libro(libro)

    def modificar_libro(self, libro=None):
        from views.modificar_libro_view import ModificarLibro
        self.controller.show_frame(ModificarLibro)

    def volver_atras(self):
        from views.home_view import HomeView
        self.controller.show_frame(HomeView)