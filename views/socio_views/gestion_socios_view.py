import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame


class GestionSocios(BaseFrame):
    def __init__(self, parent, controller, conexion):
        super().__init__(parent, controller, conexion)
        self.controller = controller

        #? Traer socios de la base de datos
        self.socios = self.ApiSocios.listar_socios()

        #? Frame Central
        self.frame_central.columnconfigure(0, weight=1) #? Esto tambien se podria refactorizar
        self.frame_central.columnconfigure(1, weight=1)
        
        #? Titulo
        self.crear_titulo("Gestion de Socios")

        #? Barra de busqueda
        self.crear_barra_busqueda("Buscar Socio", self.buscar)
        
        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)
        
        #? Creando el treeview
        columnas = {
            "id_socio":40,
            "dni":80,
            "nombre":140,
            "apellido":140
        }

        self.crear_treeview(self.frame_central, columnas)
        

        #? Boton Crear (Agregar socio)
        self.crear_boton_ver("Registrar Socio", self.registrar_socio, 0)
        
        #? Boton Modificar Socio
        self.crear_boton_ver("Modificar Socio", self.modificar_socio, 1)
        
        #? Ver prestamos
        self.crear_boton_ver("Préstamos / Historial", self.ver_prestamos, 2)
        
        #? Boton Volver
        self.crear_boton_ver("Volver atras",self.volver_atras, 3) #! Hay que cambiar esto para que use la funcion de baseframe
        
        #! Renderizamos los datos de los socios
        self.actualizar_tabla(self.socios)
        
    def crear_boton_ver(self, texto, funcion_ver, col):
        self.frame_inferior.columnconfigure(2, weight=1)
        self.btn_ver = tk.Button(
            self.frame_inferior,
            text=texto,
            fg="black",
            command=funcion_ver,
        )
        self.btn_ver.grid(row=0, column=col, sticky="ew", padx=(10,10), pady=(10, 0), ipady=6)

    def buscar(self, event=None):
        self.buscar_por_columnas(self.socios, ("dni", "nombre", "apellido"))

    def ordenar(self):
        self.ordenar_por(self.socios, "apellido")

    def registrar_socio(self, socio=None):
        from views.socio_views.registrar_socio_view import RegistrarSocio
        self.controller.show_frame(RegistrarSocio, socio)
        
    def volver_atras(self):
        from views.home_view.home_view import HomeView
        self.controller.show_frame(HomeView)
    
    def modificar_socio(self, datos=None):
        seleccionado = self.tabla.selection()
        
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un socio")
            return
        item = self.tabla.item(seleccionado[0])
        id_socio = item["values"][0]

        from views.socio_views.modificar_socio_view import ModificarSocio
        self.controller.show_frame(
            ModificarSocio,
            id_socio
        )
    def ver_prestamos(self, datos=None):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un socio")
            return

        item = self.tabla.item(seleccionado[0])
        id_socio = item["values"][0]

        from views.socio_views.prestamos_socio_view import VistaPrestamosSocio
        self.controller.show_frame(
            VistaPrestamosSocio,
            id_socio
        )