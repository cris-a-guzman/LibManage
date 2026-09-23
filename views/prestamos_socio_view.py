import tkinter as tk
from tkinter import ttk

class VistaPrestamosSocio(tk.Frame):

    def __init__(self, parent, controller, datos):
        super().__init__(parent)
        self.controller = controller
        self.datos = datos
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        tk.Label(
            self, text="Historial de Prestamos del Socio", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, sticky="new", pady=12)

        # ?--- Frame Central
        self.frame_central = tk.Frame(self, padx=20, pady=5)
        self.frame_central.grid(row=1, sticky="nsew")

        self.frame_central.columnconfigure(0, weight=4)
        self.frame_central.columnconfigure(1, weight=1)
        self.frame_central.rowconfigure(0, weight=0)
        self.frame_central.rowconfigure(1, weight=0)
        self.frame_central.rowconfigure(2, weight=1)
        self.frame_central.rowconfigure(3, weight=0)
        self.frame_central.rowconfigure(4, weight=0)

        #? Tabla de datos del socio
       
        self.frame_datos = tk.Frame(self.frame_central)
        self.frame_datos.grid(row=2, column=0, rowspan=4, sticky="nsew", pady=10)
        self.frame_datos.rowconfigure(0, weight=1)
        self.frame_datos.rowconfigure(1, weight=1)
        self.frame_datos.rowconfigure(2, weight=1)
        self.frame_datos.rowconfigure(3, weight=1)
        self.frame_datos.columnconfigure(0, weight=1)

        
        datos_socio = {
            "nombre_apellido":"Javier Pastore",
            "DNI":"21362518",
            "telefono":"3515517689",
            "fecha_asociacion": "19/07/1998"
            
        }
        
        lbl_nombre = tk.Label(self.frame_datos, text=datos_socio["nombre_apellido"])
        lbl_dni = tk.Label(self.frame_datos, text=datos_socio["DNI"])
        lbl_telefono = tk.Label(self.frame_datos, text=datos_socio["telefono"])
        lbl_fecha_asociacion = tk.Label(self.frame_datos, text=datos_socio["fecha_asociacion"])
        lbl_nombre.grid(row=0, column=0)
        lbl_dni.grid(row=1, column=0)
        lbl_telefono.grid(row=2, column=0)
        lbl_fecha_asociacion.grid(row=3, column=0)


        #? --- Tabla de Prestamos
        self.frame_tabla = tk.Frame(self.frame_central)
        self.frame_tabla.grid(
            row=2, column=1, rowspan=3, sticky="nsew", pady=10
        )
        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        columnas = ("id", "socio", "Dia de Prestamo", "Dia de devolucion", "Dias de retraso")
        self.tabla = ttk.Treeview(
            self.frame_tabla, columns=columnas, show="headings"
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("socio", text="Socio")
        self.tabla.heading("Dia de Prestamo", text="Dia de Prestamo")
        self.tabla.heading("Dia de devolucion", text="Dia de devolucion")
        self.tabla.heading("Dias de retraso", text="Dias de retraso")

        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("socio", width=80, anchor="center")
        self.tabla.column("Dia de Prestamo", width=100, anchor="center")
        self.tabla.column("Dia de devolucion", width=100, anchor="center")
        self.tabla.column("Dias de retraso", width=80, anchor="center")

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

        self.btn_atras = tk.Button(
            self.frame_central, 
            text="Volver atras", 
            command=self.volver_atras
        )
        self.btn_atras.grid(row=4, column=1, columnspan=1, sticky="ew", pady=(15, 0), ipady=5)
        #! Ejemplo de datos
        self.prestamos_datos = [
            (1, "Javier Pastore", "19/09/2026", "25/09/2026", "0"),
            (2, "Javier Pastore", "20/08/2026", "05/09/2026", "10")
        ]
        self.actualizar_tabla(self.prestamos_datos)

    def actualizar_tabla(self, lista_prestamos):
        """Limpia y vuelve a cargar los datos en la tabla."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for prestamo in lista_prestamos:
            self.tabla.insert("", "end", values=prestamo)

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