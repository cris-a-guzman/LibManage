# Vista de detalle que combina datos del socio y su historial de préstamos.
# Guía: docs/estudio/README.md#modelo-relacional-y-sql
import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame


class VistaPrestamosSocio(BaseFrame):
    # Consulta un socio por id y representa sus préstamos en una tabla.

    def __init__(self, parent, controller, id_socio):
        super().__init__(parent, controller)
        self.controller = controller

        # ? Traer datos del socio y sus préstamos de la base de datos mysql
        self.socio = self.ApiSocios.obtener_socio_por_id(id_socio)
        self.prestamos_socio = self.ApiSocios.listar_prestamos_socio(id_socio)

        # Si la consulta principal no encuentra al socio, no hay ficha válida
        # para construir y se regresa a la pantalla anterior.
        if not self.socio:
            messagebox.showerror("Error", "No se encontró el socio.")
            self.volver_atras()
            return

        if self.prestamos_socio is None:
            self.prestamos_socio = []

        # Estilos
        style = ttk.Style(self)
        style.configure(
            "Prestamos.Treeview",
            rowheight=30,
            font=("Arial", 10)
        )
        style.configure(
            "Prestamos.Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        # Distribución del contenido
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.rowconfigure(2, weight=1)

        self.crear_titulo(
            f"Préstamos de {self.socio['nombre']} "
            f"{self.socio['apellido']}"
        )

        # Ficha del socio
        self.frame_datos = tk.LabelFrame(
            self.frame_central,
            text="Información del socio",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=10
        )
        self.frame_datos.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10, 15)
        )

        self.frame_datos.columnconfigure((0,2), weight=1)
        self.frame_datos.columnconfigure(1, weight=2)

        tk.Label(
            self.frame_datos,
            text=f"ID: {self.socio['id_socio']}",
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="w", padx=8)

        tk.Label(
            self.frame_datos,
            text=f"Socio: {self.socio['nombre']} "
                 f"{self.socio['apellido']}",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, sticky="w", padx=8)

        tk.Label(
            self.frame_datos,
            text=f"DNI: {self.socio['dni']}",
            font=("Arial", 10)
        ).grid(row=0, column=2, sticky="w", padx=8)

        # Encabezado del historial
        self.lbl_historial = tk.Label(
            self.frame_central,
            text="Historial de préstamos",
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        self.lbl_historial.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 8)
        )

        # Tabla
        self.frame_tabla = tk.Frame(self.frame_central)
        self.frame_tabla.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
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
            self.frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
            style="Prestamos.Treeview"
        )

        encabezados = {
            "id": "ID",
            "libro": "Libro",
            "fecha_prestamo": "Fecha de préstamo",
            "fecha_devolucion_estimada": "Vencimiento",
            "fecha_devolucion_real": "Devolución real",
            "estado": "Estado"
        }

        anchos = {
            "id": 55,
            "libro": 220,
            "fecha_prestamo": 135,
            "fecha_devolucion_estimada": 135,
            "fecha_devolucion_real": 135,
            "estado": 100
        }

        for columna in columnas:
            self.tabla.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla.column(
                columna,
                width=anchos[columna],
                minwidth=60,
                anchor="center"
            )

        self.tabla.column("libro", anchor="w")

        scrollbar_y = ttk.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        scrollbar_x = ttk.Scrollbar(
            self.frame_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Filas alternadas
        self.tabla.tag_configure("par", background="#F2F5F9")
        self.tabla.tag_configure("impar", background="#FFFFFF")

        # Botones inferiores de BaseFrame
        self.crear_boton_volver(self.volver_atras)

        # Cargar información
        self.actualizar_tabla(self.prestamos_socio)

    def actualizar_tabla(self, prestamos_socio):
        # Reemplaza filas, alterna estilos y actualiza el total mostrado.
        self.tabla.delete(*self.tabla.get_children())

        # enumerate aporta el índice usado para alternar colores par/impar.
        for indice, prestamo in enumerate(prestamos_socio):
            self.tabla.insert(
                "",
                "end",
                values=(
                    prestamo["id"],
                    prestamo["libro"],
                    prestamo["fecha_prestamo"],
                    prestamo["fecha_devolucion_estimada"],
                    prestamo["fecha_devolucion_real"] or "-",
                    prestamo["estado"]
                ),
                tags=("par" if indice % 2 == 0 else "impar",)
            )

        cantidad = len(prestamos_socio)
        self.lbl_historial.config(
            text=f"Historial de préstamos  ·  {cantidad} registro(s)"
        )

    def volver_atras(self):
        # Regresa a la gestión de socios.
        from views.socio_views.gestion_socios_view import GestionSocios
        self.controller.show_frame(GestionSocios)
