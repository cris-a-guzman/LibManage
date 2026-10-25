import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from datetime import date, datetime
from views.components.lista_desplegable import AutocompleteCombobox
from views.components.base_frame import BaseFrame
from views.components.formulario_desplazable import FormularioDesplazable
from views.components.estilo import TITULO

class RegistrarPrestamo(BaseFrame):

    def __init__(self, parent, controller, conexion):
        super().__init__(parent, controller, conexion)
        self.controller = controller

        # Carga de datos desde la API/Repositories
        self.dni_socios = self.ApiSocios.obtener_socios_dni()
        self.libros_catalogo = self.ApiLibros.obtener_disponibilidad_libros()

        self.opciones_libros = {
            f"[{int(libro['disponibles'])} disponibles] "
            f"{libro['titulo']} (ID {libro['id_libro']})": libro
            for libro in self.libros_catalogo
            if libro["disponibles"] > 0
        }
        self.socio_seleccionado = None
        self.libro_seleccionado = None
        self.libros_seleccionados = {}

        # Configuración del grid del contenedor principal
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        tb.Label(
            self, text="Registrar Préstamo", font=TITULO, bootstyle=PRIMARY
        ).grid(row=0, column=0, sticky="new", pady=12)

        # --- Frame Central
        self.scroll_formulario = FormularioDesplazable(
        self.frame_central
        )
        self.scroll_formulario.pack(fill="both", expand=True)

        self.frame_central = tb.Labelframe(self.scroll_formulario.contenido, text="Nuevo préstamo", padding=22, bootstyle=PRIMARY)
        self.frame_central.pack(fill="both", expand=True)
        self.frame_central.columnconfigure(0, weight=1)

        tb.Label(
            self.frame_central, text="Ingrese DNI del SOCIO:", bootstyle=PRIMARY
        ).grid(row=0, column=0, sticky="w", pady=(5, 0))

        self.combo_dni_socio = AutocompleteCombobox(
            self.frame_central, width=30, bootstyle=PRIMARY
        )
        self.combo_dni_socio.set_completion_list(self.dni_socios)
        self._configurar_placeholder(self.combo_dni_socio, "Escribir DNI...")
        self.combo_dni_socio.grid(row=1, column=0, sticky="ew", ipady=5, pady=(0, 5))
        self.combo_dni_socio.bind("<<ComboboxSelected>>", self.al_seleccionar_socio)

        self.lbl_socio_seleccionado = tb.Label(
            self.frame_central,
            text="Ningún socio seleccionado",
            bootstyle="secondary",
            padding=8,
        )
        self.lbl_socio_seleccionado.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # --- Buscar Libro (Título)
        tb.Label(
            self.frame_central, text="Buscar libro por TÍTULO:", bootstyle=PRIMARY
        ).grid(row=3, column=0, sticky="w", pady=(5, 0))

        self.combo_libro = AutocompleteCombobox(
            self.frame_central, width=30, bootstyle=PRIMARY
        )
        self.combo_libro.set_completion_list(
            list(self.opciones_libros.keys())
        )        
        self._configurar_placeholder(self.combo_libro, "Escribir título...")
        self.combo_libro.grid(row=4, column=0, sticky="ew", ipady=5, pady=(0, 5))
        self.combo_libro.bind("<<ComboboxSelected>>", self.al_seleccionar_libro)

        self.lbl_libro_seleccionado = tb.Label(
            self.frame_central,
            text="Ningún libro seleccionado",
            bootstyle="secondary",
            padding=8,
        )
        self.lbl_libro_seleccionado.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        # --- Libros incluidos en el préstamo
        self.frame_libros = tb.Labelframe(
            self.frame_central,
            text="Libros del préstamo",
            padding=10,
            bootstyle=INFO
        )
        self.frame_libros.grid(
            row=6, column=0, sticky="ew", pady=10
        )
        self.frame_libros.columnconfigure(0, weight=1)

        # Controles para agregar ejemplares
        self.controles_libros = tb.Frame(self.frame_libros)
        self.controles_libros.grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        tb.Label(
            self.controles_libros,
            text="Cantidad:"
        ).pack(side="left", padx=5)

        self.cantidad_libro = tb.Spinbox(
            self.controles_libros,
            from_=1,
            to=999,
            width=5,
            bootstyle=PRIMARY
        )
        self.cantidad_libro.set(1)
        self.cantidad_libro.pack(side="left", padx=5)

        self.btn_agregar_libro = tb.Button(
            self.controles_libros,
            text="Agregar libro",
            command=self.agregar_libro,
            bootstyle=SUCCESS
        )
        self.btn_agregar_libro.pack(side="left", padx=5)

        # Tabla de libros seleccionados
        self.tabla_libros = tb.Treeview(
            self.frame_libros,
            columns=("titulo", "cantidad"),
            show="headings",
            height=4,
            selectmode="browse",
            bootstyle=INFO
        )

        self.tabla_libros.heading("titulo", text="Libro")
        self.tabla_libros.heading("cantidad", text="Cantidad")

        self.tabla_libros.column("titulo", width=260)
        self.tabla_libros.column("cantidad", width=80)

        self.tabla_libros.grid(
            row=1, column=0, sticky="ew", pady=10
        )

        barra_libros = tb.Scrollbar(
            self.frame_libros,
            orient="vertical",
            command=self.tabla_libros.yview,
            bootstyle="round"
        )
        barra_libros.grid(row=1, column=1, sticky="ns")

        self.tabla_libros.configure(
            yscrollcommand=barra_libros.set
        )

        self.btn_quitar_libro = tb.Button(
            self.frame_libros,
            text="Quitar seleccionado",
            command=self.quitar_libro,
            bootstyle="danger-outline"
        )
        self.btn_quitar_libro.grid(
            row=2, column=0, sticky="e"
        )

        # --- Fecha de préstamo (automática)
        tb.Label(
            self.frame_central, text="Fecha de préstamo (Automática)"
        ).grid(row=7, column=0, sticky="w", pady=(5, 0))

        self.lbl_fecha_prestamo = tb.Label(
            self.frame_central,
            text=date.today().strftime("%d/%m/%Y"),
            bootstyle="secondary",
            padding=8,
        )
        self.lbl_fecha_prestamo.grid(row=8, column=0, sticky="ew", pady=(0, 10))

        # --- Fecha de devolución estimada
        tb.Label(
            self.frame_central, text="Fecha de devolución estimada"
        ).grid(row=9, column=0, sticky="w", pady=(5, 0))

        self.entry_fecha_devolucion = tb.Entry(self.frame_central, justify="center", bootstyle=PRIMARY)
        self._configurar_placeholder(self.entry_fecha_devolucion, "dd/mm/aaaa")
        self.entry_fecha_devolucion.grid(
            row=10, column=0, sticky="ew", ipady=5, pady=(0, 15)
        )

        # --- Botones Confirmar / Cancelar
        self.frame_botones = tb.Frame(self.frame_central)
        self.frame_botones.grid(row=11, column=0, sticky="ew")
        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.columnconfigure(1, weight=1)

        self.btn_confirmar = tb.Button(
            self.frame_botones,
            text="Confirmar Préstamo",
            command=self.confirmar_prestamo,
            bootstyle=SUCCESS
        )
        self.btn_confirmar.grid(row=0, column=0, sticky="ew", padx=(0, 5), ipady=8)

        self.btn_cancelar = tb.Button(
            self.frame_botones, text="Cancelar", command=self.cancelar, bootstyle="secondary-outline"
        )
        self.btn_cancelar.grid(row=0, column=1, sticky="ew", padx=(5, 0), ipady=8)

    def _configurar_placeholder(self, widget, placeholder):
        """Helper para reutilizar la lógica de placeholders en campos de texto/combos."""
        widget.insert(0, placeholder)
        widget.bind(
            "<FocusIn>",
            lambda e: widget.delete(0, "end") if widget.get() == placeholder else None,
        )
        widget.bind(
            "<FocusOut>",
            lambda e: widget.insert(0, placeholder) if widget.get().strip() == "" else None,
        )

    def al_seleccionar_socio(self, event):
        dni_ingresado = self.combo_dni_socio.get().strip()
        if dni_ingresado and dni_ingresado != "Escribir DNI...":
            # Guardamos la referencia al socio seleccionado
            self.socio_seleccionado = dni_ingresado
            self.lbl_socio_seleccionado.config(
                text=f"Socio Seleccionado (DNI): {dni_ingresado}", bootstyle=SUCCESS
            )

    def al_seleccionar_libro(self, event):
        opcion = self.combo_libro.get().strip()

        libro = self.opciones_libros.get(opcion)

        if libro is None:
            self.libro_seleccionado = None
            return

        self.libro_seleccionado = libro

        self.lbl_libro_seleccionado.config(
            text=(
                f"Libro: {libro['titulo']} - "
                f"{int(libro['disponibles'])} disponibles"
            ),
            bootstyle=SUCCESS
        )

    def agregar_libro(self):
        libro = self.libro_seleccionado

        if not libro:
            Messagebox.show_warning(
                "Primero seleccioná un libro.",
                title="Atención"
            )
            return

        # Evitar agregar un título distinto del seleccionado
        if self.opciones_libros.get(
            self.combo_libro.get().strip()
        ) is not libro:
            Messagebox.show_warning(
                "Seleccioná nuevamente el libro.",
                title="Atención"
            )
            return

        try:
            cantidad = int(self.cantidad_libro.get())

            if cantidad <= 0:
                raise ValueError
            
            if cantidad > libro["disponibles"]:
                Messagebox.show_warning(
                    f"Solo hay {int(libro['disponibles'])} "
                    "ejemplares disponibles de este libro.",
                    title="Sin disponibilidad suficiente"
                )
                return

        except ValueError:
            Messagebox.show_warning(
                "Ingresá una cantidad entera mayor que cero.",
                title="Cantidad inválida"
            )
            return

        id_libro = libro["id_libro"]

        if id_libro in self.libros_seleccionados:
            Messagebox.show_warning(
                "Este libro ya está agregado. "
                "Quitalo si querés cambiar su cantidad.",
                title="Libro repetido"
            )
            return

        # Guardar la selección en memoria
        self.libros_seleccionados[id_libro] = {
            "titulo": libro["titulo"],
            "cantidad": cantidad
        }

        # Mostrarla en el Treeview
        self.tabla_libros.insert(
            "",
            "end",
            iid=str(id_libro),
            values=(libro["titulo"], cantidad)
        )

        # Preparar el formulario para otro libro
        self.combo_libro.set("")
        self.libro_seleccionado = None
        self.cantidad_libro.delete(0, "end")
        self.cantidad_libro.insert(0, "1")

        self.lbl_libro_seleccionado.config(
            text="Ningún libro seleccionado",
            bootstyle="secondary"
        )

    def quitar_libro(self):
        seleccion = self.tabla_libros.selection()

        if not seleccion:
            Messagebox.show_warning(
                "Seleccioná un libro para quitarlo.",
                title="Atención"
            )
            return

        id_libro = int(seleccion[0])

        self.libros_seleccionados.pop(id_libro, None)
        self.tabla_libros.delete(seleccion[0])
    
    def confirmar_prestamo(self):
        if not self.socio_seleccionado:
            Messagebox.show_warning(
                "Seleccioná un socio.",
                title="Atención"
            )
            return

        if self.combo_dni_socio.get().strip() != self.socio_seleccionado:
            Messagebox.show_warning(
                "Volvé a seleccionar un socio válido.",
                title="Atención"
            )
            return

        if not self.libros_seleccionados:
            Messagebox.show_warning(
                "Agregá al menos un libro al préstamo.",
                title="Atención"
            )
            return

        # Validar la fecha
        try:
            fecha_devolucion = datetime.strptime(
                self.entry_fecha_devolucion.get().strip(),
                "%d/%m/%Y"
            ).date()

            if fecha_devolucion < date.today():
                raise ValueError

        except ValueError:
            Messagebox.show_warning(
                "Ingresá una fecha válida igual o posterior a hoy.",
                title="Fecha inválida"
            )
            return

        # Preparar los datos para el repositorio
        libros = [
            (id_libro, datos["cantidad"])
            for id_libro, datos in self.libros_seleccionados.items()
        ]

        try:
            id_prestamo = self.ApiPrestamos.crear_prestamo_multiple(
                dni_socio=self.socio_seleccionado,
                libros=libros,
                fecha_devolucion=fecha_devolucion
            )

        except Exception as error:
            Messagebox.show_error(
                f"No se pudo registrar el préstamo: {error}",
                title="Error"
            )
            return

        Messagebox.show_info(
            f"El préstamo {id_prestamo} se registró correctamente.",
            title="Préstamo registrado"
        )

        self.cancelar()

    def cancelar(self):
        from views.prestamos_views.gestion_prestamos_view import GestionPrestamos
        self.controller.show_frame(GestionPrestamos)
