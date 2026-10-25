
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from views.components.base_frame import BaseFrame
from views.components.estilo import SUBTITULO, CUERPO, FUENTE


class VistaPrestamosSocio(BaseFrame):

    def __init__(self, parent, controller, conexion, id_socio):
        super().__init__(parent, controller, conexion)
        self.controller = controller

        # ? Traer datos del socio y sus préstamos de la base de datos mysql
        self.socio = self.ApiSocios.obtener_socio_por_id(id_socio)
        self.prestamos_socio = self.ApiSocios.listar_prestamos_socio(id_socio)

        if not self.socio:
            Messagebox.show_error("No se encontró el socio.", title="Error")
            self.volver_atras()
            return

        if self.prestamos_socio is None:
            self.prestamos_socio = []

        # Estilos
        style = tb.Style()
        style.configure(
            "Prestamos.Treeview",
            rowheight=34,
            font=CUERPO
        )
        style.configure(
            "Prestamos.Treeview.Heading",
            font=(FUENTE, 10, "bold")
        )

        # Distribución del contenido
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.rowconfigure(2, weight=1)

        self.crear_titulo(
            f"Préstamos de {self.socio['nombre']} "
            f"{self.socio['apellido']}"
        )

        # Ficha del socio
        self.frame_datos = tb.Labelframe(
            self.frame_central,
            text="Información del socio",
            padding=16,
            bootstyle=PRIMARY
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

        tb.Label(
            self.frame_datos,
            text=f"ID: {self.socio['id_socio']}",
            font=CUERPO
        ).grid(row=0, column=0, sticky="w", padx=8)

        tb.Label(
            self.frame_datos,
            text=f"Socio: {self.socio['nombre']} "
                 f"{self.socio['apellido']}",
            font=SUBTITULO
        ).grid(row=0, column=1, sticky="w", padx=8)

        tb.Label(
            self.frame_datos,
            text=f"DNI: {self.socio['dni']}",
            font=CUERPO
        ).grid(row=0, column=2, sticky="w", padx=8)
        
        tb.Label(
            self.frame_datos,
            text=f"Fecha de Asociacion: {self.socio['fecha_asociacion']}",
            font=CUERPO
        ).grid(row=0, column=3, sticky="w", padx=8)
        
        tb.Label(
            self.frame_datos,
            text=f"Telefono: {self.socio['telefono']}",
            font=CUERPO
        ).grid(row=0, column=4, sticky="w", padx=8)

        # Encabezado del historial
        self.lbl_historial = tb.Label(
            self.frame_central,
            text="Historial de préstamos",
            font=SUBTITULO,
            anchor="w",
            bootstyle=PRIMARY
        )
        self.lbl_historial.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 8)
        )

        # Tabla
        self.frame_tabla = tb.Frame(self.frame_central)
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

        self.tabla = tb.Treeview(
            self.frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
            style="Prestamos.Treeview",
            bootstyle=INFO
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

        scrollbar_y = tb.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla.yview,
            bootstyle="round"
        )

        scrollbar_x = tb.Scrollbar(
            self.frame_tabla,
            orient="horizontal",
            command=self.tabla.xview,
            bootstyle="round"
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # Filas alternadas
        colores = tb.Style().colors
        self.tabla.tag_configure("par", background=colores.bg)
        self.tabla.tag_configure("impar", background=colores.inputbg)

        # Botones inferiores de BaseFrame
        self.crear_boton_volver(self.volver_atras)

        # Cargar información
        self.actualizar_tabla(self.prestamos_socio)

    def actualizar_tabla(self, prestamos_socio):
        self.tabla.delete(*self.tabla.get_children())

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
        from views.socio_views.gestion_socios_view import GestionSocios
        self.controller.show_frame(GestionSocios)
