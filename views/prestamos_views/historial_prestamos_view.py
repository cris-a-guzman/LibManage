# Vista histórica en estado incompleto dentro de la versión principal.
# Se conserva exactamente como fue implementada: los nombres self.socio y
# self.prestamos no se inicializan aquí. La guía registra esa discrepancia sin
# corregirla: docs/estudio/README.md#limitaciones-y-observaciones
import tkinter as tk
from tkinter import messagebox
from views.components.base_frame import BaseFrame

class HistorialPrestamosSocio(BaseFrame):
    # Maqueta una ficha de socio junto con el texto de sus préstamos.

    def __init__(self, parent, controller, datos):
        super().__init__(parent, controller)
        self.controller = controller
        self.datos_socio = datos
        self.datos_prestamos = {}

        self.frame_central = self.crear_frame_central()
        
        self.crear_titulo("Historial de prestamos del socio")

        #? --- Frame Central
        self.frame_central = tk.Frame(self, bd=1, relief="solid", padx=15, pady=15)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        self.frame_central.columnconfigure((0,1), weight=1)
        self.frame_central.rowconfigure(4, weight=1)

        #? --- Columna izquierda: Datos del socio
        self.lbl_nombre = tk.Label(
            self.frame_central,
            text=f"Nombre y Apellido: {self.socio['nombre']}",
            bd=1,
            relief="solid",
            pady=10,
        )
        self.lbl_nombre.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=(0, 10), ipady=5)

        self.lbl_dni = tk.Label(
            self.frame_central,
            text=f"DNI: {self.socio['dni']}",
            bd=1,
            relief="solid",
            pady=10,
        )
        self.lbl_dni.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 10), ipady=5)

        self.lbl_telefono = tk.Label(
            self.frame_central,
            text=f"Telefono: {self.socio['telefono']}",
            bd=1,
            relief="solid",
            pady=10,
        )
        self.lbl_telefono.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 10), ipady=5)

        self.lbl_fecha_asociacion = tk.Label(
            self.frame_central,
            text=f"Fecha de Asociacion: {self.socio['fecha_asociacion']}",
            bd=1,
            relief="solid",
            pady=10,
        )
        self.lbl_fecha_asociacion.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 10), ipady=5)

        self.btn_ver_prestamos = tk.Button(
            self.frame_central,
            text="Ver prestamos del socio",
            command=self.ver_prestamos,
        )
        self.btn_ver_prestamos.grid(row=4, column=0, sticky="new", padx=(0, 10), ipady=8)

        #? --- Columna derecha: Listado de prestamos
        self.lbl_listado_titulo = tk.Label(
            self.frame_central,
            text="Listado De Prestamos",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_listado_titulo.grid(row=0, column=1, sticky="ew", pady=(0, 10), ipady=3)

        self.frame_listado = tk.Frame(self.frame_central, bd=1, relief="solid")
        self.frame_listado.grid(row=1, column=1, rowspan=4, sticky="nsew")

        self.lbl_listado = tk.Label(
            self.frame_listado,
            text="",
            justify="left",
            anchor="nw",
            padx=10,
            pady=10,
        )
        self.lbl_listado.pack(fill="both", expand=True)

        self.renderizar_listado()

        #? --- Volver Atras
        self.crear_boton_volver(self.volver_atras)

    def renderizar_listado(self):
        # Acumula una representación legible de cada préstamo. En el estado
        # actual, self.prestamos no fue asignado por el constructor.
        """Arma el texto del listado de prestamos del socio."""
        texto = ""
        for prestamo in self.prestamos:
            texto += (
                f"Prestamo {prestamo['numero']}:\n"
                f"Estado: {prestamo['estado']}\n"
                f"Dia de prestamo: {prestamo['fecha_prestamo']}\n"
                f"Dia de Devolucion: {prestamo['fecha_devolucion']}\n"
                f"Dias de retraso: {prestamo['dias_retraso']}\n\n"
            )
        self.lbl_listado.config(text=texto.strip())

    def ver_prestamos(self):
        # Acción provisoria: informa por consola, sin consultar datos.
        print(f"Mostrando prestamos completos de {self.socio['nombre']}...")

    def volver_atras(self):
        # Regresa a la gestión de socios.
        from views.socio_views.gestion_socios_view import GestionSocios
        self.controller.show_frame(GestionSocios)