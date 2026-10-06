import tkinter as tk
from tkinter import ttk
from views.components.base_frame import BaseFrame

class VistaPrestamosSocio(BaseFrame):

    def __init__(self, parent, controller, id_socio):
        super().__init__(parent, controller)
        self.controller = controller
        self.socio = self.API.traer_socio_por_id(id_socio)
        self.prestamos_socio = self.API.traer_prestamos_socio(id_socio)
        
        if self.prestamos_socio == None:
            print("Algo salio mal, volviendo atras")
        else:
            print(self.socio)
            print(self.prestamos_socio)

        #? Frame Central
        self.frame_central.columnconfigure(0, weight=1) #? Esto tambien se podria refactorizar
        self.frame_central.columnconfigure(1, weight=1)
        self.frame_central.rowconfigure(0, weight=0)
        self.frame_central.rowconfigure(1, weight=0)
        self.frame_central.rowconfigure(2, weight=1)
        self.frame_central.rowconfigure(3, weight=0)
        self.frame_central.rowconfigure(4, weight=0)
        
        #? Titulo
        self.crear_titulo(f"Prestamos de {self.socio["nombre"]} {self.socio["apellido"]} ")

        #? Tabla de datos del socio
       
        self.frame_datos = tk.Frame(self.frame_central)
        self.frame_datos.grid(row=2, column=0, rowspan=4, sticky="nsew", pady=10)
        self.frame_datos.rowconfigure(0, weight=1)
        self.frame_datos.rowconfigure(1, weight=1)
        self.frame_datos.rowconfigure(2, weight=1)
        self.frame_datos.columnconfigure(0, weight=1)
        
        lbl_id = tk.Label(
            self.frame_central,
            text=f"ID: {self.socio["id_socio"]}"
        )
        
        lbl_nombre = tk.Label(
            self.frame_datos,
            text=f"Nombre: {self.socio['nombre']} {self.socio['apellido']}"
        )

        lbl_dni = tk.Label(
            self.frame_datos,
            text=f"DNI: {self.socio["dni"]}"
        )

        lbl_id.grid(row=0, column=0)
        lbl_nombre.grid(row=1, column=0)
        lbl_dni.grid(row=2, column=0)



        #? --- Tabla de Prestamos
        self.frame_tabla = tk.Frame(self.frame_central)
        self.frame_tabla.grid(
            row=2, column=1, rowspan=3, sticky="nsew", pady=10
        )
        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        columnas = (
                "id",
                "libro",
                "fecha_prestamo",
                "fecha_devolucion_estimada",
                "fecha_devolucion_real",
                "estado"
                )
        
        self.tabla = ttk.Treeview(
            self.frame_tabla, columns=columnas, show="headings"
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("libro", text="Libro")
        self.tabla.heading("fecha_prestamo", text="Fecha prés")
        self.tabla.heading("fecha_devolucion_estimada", text="Fecha devo")
        self.tabla.heading("fecha_devolucion_real", text="Devo real")
        self.tabla.heading("estado", text="Estado")


        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("libro", width=100, anchor="center")
        self.tabla.column("fecha_prestamo", width=60, anchor="center")
        self.tabla.column("fecha_devolucion_estimada", width=60, anchor="center")
        self.tabla.column("fecha_devolucion_real", width=60, anchor="center")
        self.tabla.column("estado", width=60, anchor="center")


        scrollbar = ttk.Scrollbar(
            self.frame_tabla, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Botones 
        self.frame_acciones = tk.Frame(self.frame_central)
        self.frame_acciones.grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=5
        )
        self.frame_acciones.columnconfigure(0, weight=1)

        self.crear_boton_volver(self.volver_atras)
        self.actualizar_tabla(self.prestamos_socio)

    def actualizar_tabla(self, prestamos_socio):
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for prestamo in prestamos_socio:
            self.tabla.insert(
                "",
                "end",
                values=(
                    prestamo["id"],
                    prestamo["libro"],
                    prestamo["fecha_prestamo"],
                    prestamo["fecha_devolucion_estimada"],
                    prestamo["fecha_devolucion_real"],
                    prestamo["estado"]
                )
            )

    def buscar(self, event=None):
        """Filtra la lista de prestamos según lo ingresado."""
        texto = self.busqueda.get().strip().lower()
        if not texto:
            self.actualizar_tabla(self.prestamos_datos)
            return

        resultados = [
            p for p in self.prestamos_datos
            if texto in p[1].lower() or texto in p[2].lower()
        ]
        self.actualizar_tabla(resultados)

    def limpiar_busqueda(self):
        """Restablece la búsqueda y muestra todos los datos."""
        self.busqueda.delete(0, tk.END)
        self.actualizar_tabla(self.prestamos_datos)

    def ordenar(self):
        """Ordena los prestamos por fecha de vencimiento."""
        prestamos_ordenados = sorted(self.prestamos_datos, key=lambda x: x[3])
        self.actualizar_tabla(prestamos_ordenados)

    def marcar_devuelto(self):
        """Elimina de la lista el prestamo seleccionado (ya devuelto)."""
        seleccion = self.tabla.selection()
        if not seleccion:
            tk.messagebox.showwarning(
                "Atención", "Por favor, selecciona un préstamo de la lista."
            )
            return

        item = self.tabla.item(seleccion)
        prestamo_id = item["values"][0]

        self.prestamos_datos = [
            p for p in self.prestamos_datos if p[0] != prestamo_id
        ]
        self.actualizar_tabla(self.prestamos_datos)
        
    def volver_atras(self): #! Esto lo podriamos pasar a controller me parece
        from views.home_view import HomeView
        self.controller.show_frame(HomeView)