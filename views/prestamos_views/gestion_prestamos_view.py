import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame

class GestionPrestamos(BaseFrame):

    def __init__(self, parent, controller, conexion):
        super().__init__(parent, controller, conexion)
        self.controller = controller
        self.solo_vencidos = False   


        # ?--- Frame Central
        self.frame_central = self.crear_frame_central()
        self.frame_central.columnconfigure(0, weight=4)
        self.frame_central.columnconfigure(1, weight=1)
        
        self.frame_central.rowconfigure((0,1,3), weight=0)
        self.frame_central.rowconfigure(2, weight=1)

        #? -- TItulo
        self.crear_titulo("Gestion de Prestamos")

        #? --- Barra de busqueda
        self.crear_barra_busqueda("Buscar préstamo", self.buscar)

        self.busqueda.grid_configure(columnspan=1, padx=(0, 5))

        self.boton = tk.Button( #! se puede refactorizar
            self.frame_central, text="Buscar", command=self.buscar
        )
        self.boton.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #? Boton Solo Vencidos
        self.btn_filtros.config(text="Solo vencidos")

        #? --- Tabla de Prestamos
        columnas = {
            "id":40,
            "socio":140,
            "libro":180,
            "vence":90,
            "estado":100
        }

        self.crear_treeview(self.frame_central, columnas)

        # --- Botones de Acción (Inferiores)
        self.frame_acciones = tk.Frame(self.frame_central)
        self.frame_acciones.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        self.frame_acciones.columnconfigure(0, weight=1)

        self.btn_devolver = tk.Button(self.frame_acciones, text="devolver", command=self.marcar_devuelto, )
        self.btn_devolver.pack(side="right", padx=5)
        self.btn_devolver.config(state="disabled")

        self.tabla.bind("<<TreeviewSelect>>", self.actualizar_boton_devolver)

        #? Boton Crear (Registrar prestamo)
        self.crear_boton_crear("Registrar Prestamo", self.registrar_prestamo)
        
        #? Boton Volver Atras
        self.crear_boton_volver(self.volver_atras)

        #? Traer prestamos de la base de datos
        self.prestamos_datos = self.ApiPrestamos.listar_prestamos()
        self.actualizar_tabla(self.prestamos_datos)

    
    def filtrar(self):
        nuevo_estado = not self.solo_vencidos

        try:
            datos = self.ApiPrestamos.listar_prestamos(
                solo_vencidos=nuevo_estado
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron filtrar los préstamos: {error}"
            )
            return

        self.solo_vencidos = nuevo_estado
        self.prestamos_datos = datos

        self.limpiar_busqueda(self.prestamos_datos)

        if self.solo_vencidos:
            self.btn_filtros.config(text="Mostrar todos")
        else:
            self.btn_filtros.config(text="Solo vencidos")

    def actualizar_tabla(self, lista_prestamos):
        super().actualizar_tabla(lista_prestamos)
        self.actualizar_boton_devolver()

    def buscar(self, event=None):
        self.buscar_por_columnas(self.prestamos_datos, (1, 2))

    def ordenar(self):
        self.ordenar_por(self.prestamos_datos, 3)

    def actualizar_boton_devolver(self, event=None):
        seleccion = self.tabla.selection()

        if not seleccion:
            self.btn_devolver.config(state="disabled")
            return

        valores = self.tabla.item(seleccion[0], "values")
        estado = str(valores[4]).strip().lower()

        if estado == "activo":
            self.btn_devolver.config(state="normal")
        else:
            self.btn_devolver.config(state="disabled")


    def marcar_devuelto(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            self.mensaje_advertencia("Atención", "Seleccioná un préstamo.")
            return

        item = self.tabla.item(seleccion[0])
        id_prestamo = int(item["values"][0])

        confirmar = self.mensaje_confirmacion("Confirmar devolución", f"¿Confirmás la devolución del préstamo {id_prestamo}?")

        if not confirmar:
            return

        try:
            resultado = self.ApiPrestamos.devolver_prestamo(id_prestamo)

            if not resultado:
                self.mensaje_advertencia("Atención", "El préstamo no está activo o no puede devolverse.")
                return

            # Volver a consultar MySQL para actualizar la tabla
            self.prestamos_datos = self.ApiPrestamos.listar_prestamos(
                solo_vencidos=self.solo_vencidos
            ) 
            self.actualizar_tabla(self.prestamos_datos)

            self.mensaje_info("Devolución registrada","El préstamo fue devuelto correctamente.")

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo registrar la devolución: {error}"
            )


    def registrar_prestamo(self):
        from views.prestamos_views.registrar_prestamo_view import RegistrarPrestamo
        self.controller.show_frame(RegistrarPrestamo)
        
    def volver_atras(self): #! Esto lo podriamos pasar a controller me parece
        from views.home_view.home_view import HomeView
        self.controller.show_frame(HomeView)