import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from views.components.base_frame import BaseFrame

class GestionLibros(BaseFrame):
    def __init__(self, parent, controller, conexion):
        super().__init__(parent, controller, conexion)
        self.controller = controller
            #? Frame principal
        
        # ? Traer libros de la base de datos
        self.libros_datos = self.ApiLibros.listar_libros()
        self.frame_central = self.crear_frame_central()

        #? Titulo
        self.crear_titulo("Gestion de Libro")
        self.frame_central.columnconfigure((0,1), weight=1)
        self.frame_central.rowconfigure(2, weight=1)

        #? Barra de busqueda
        self.crear_barra_busqueda("Buscar Libro", self.buscar)

        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #? --- Tabla de Libros
        self.frame_libros = tb.Frame(self.frame_central)
        self.frame_libros.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        self.frame_libros.rowconfigure(0, weight=1)
        self.frame_libros.columnconfigure(0, weight=1)

        columnas = {
            "id_libro":50,
            "isbn":120,
            "titulo":200,
            "autor":150,
            "anio":60,
            "cantidad_total":60
        }

        modo = "browse"
        self.crear_treeview(self.frame_libros, columnas, modo)

        #? Doble clic sobre una fila = modificar ese libro
        #! A esto lo podriamos pasar al general creo
        self.tabla.bind("<Double-1>", lambda e: self.modificar_seleccionado())
        
        self.frame_inferior.columnconfigure(2, weight=1)

        #? Boton Crear Libro
        self.crear_boton_crear("Crear Libro", self.crear_libro)

        #? Boton Volver Atras
        self.crear_boton_volver(self.volver_atras)

        #? Boton Modificar (actua sobre la fila seleccionada)
        btn_modificar = tb.Button(
            self.frame_inferior,
            text="Modificar",
            command=self.modificar_seleccionado,
            bootstyle="warning-outline"
        )
        btn_modificar.grid(row=0, column=2, sticky="ew", padx=8, pady=(8, 0), ipady=8)

        self.actualizar_tabla(self.libros_datos)
        
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
        self.busqueda.delete(0, "end")
        self.actualizar_tabla(self.libros_datos)
        
    def crear_libro(self):
        from views.libros_views.crear_libro_view import CrearLibro
        self.controller.show_frame(CrearLibro)

    def modificar_seleccionado(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            Messagebox.show_warning(
                "Por favor, seleccioná un libro de la lista.",
                title="Atención"
            )
            return

        id_libro = self.tabla.item(seleccion[0])["values"][0]
        libro = next((l for l in self.libros_datos if l["id_libro"] == id_libro), None)
        self.modificar_libro(libro)

    def modificar_libro(self, libro=None):
        from views.libros_views.modificar_libro_view import ModificarLibro
        self.controller.show_frame(ModificarLibro, libro)

    def volver_atras(self):
        from views.home_view.home_view import HomeView
        self.controller.show_frame(HomeView)
