import tkinter as tk
from tkinter import ttk,messagebox
from datetime import date, datetime
from views.components.lista_desplegable import AutocompleteCombobox
from views.components.base_frame import BaseFrame
from views.components.formulario_desplazable import FormularioDesplazable

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

        tk.Label(
            self, text="Registrar Préstamo", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, sticky="new", pady=12)

        # --- Frame Central
        self.scroll_formulario = FormularioDesplazable(
        self.frame_central
        )
        self.scroll_formulario.pack(fill="both", expand=True)

        self.frame_central = tk.Frame(self.scroll_formulario.contenido, padx=20, pady=5)
        self.frame_central.pack(fill="both", expand=True)
        self.frame_central.columnconfigure(0, weight=1)

        # --- Buscar Socio (DNI)
        tk.Label(
            self.frame_central, text="Ingrese DNI del SOCIO:"
        ).grid(row=0, column=0, sticky="w", pady=(5, 0))

        self.combo_dni_socio = AutocompleteCombobox(
            self.frame_central, width=30, font=("Arial", 10)
        )
        self.combo_dni_socio.set_completion_list(self.dni_socios)
        self._configurar_placeholder(self.combo_dni_socio, "Escribir DNI...")
        self.combo_dni_socio.grid(row=1, column=0, sticky="ew", ipady=5, pady=(0, 5))
        self.combo_dni_socio.bind("<<ComboboxSelected>>", self.al_seleccionar_socio)

        self.lbl_socio_seleccionado = tk.Label(
            self.frame_central,
            text="Ningún socio seleccionado",
            bg="#f0f0f0",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_socio_seleccionado.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # --- Buscar Libro (Título)
        tk.Label(
            self.frame_central, text="Buscar libro por TÍTULO:"
        ).grid(row=3, column=0, sticky="w", pady=(5, 0))

        self.combo_libro = AutocompleteCombobox(
            self.frame_central, width=30, font=("Arial", 10)
        )
        self.combo_libro.set_completion_list(
            list(self.opciones_libros.keys())
        )        
        self._configurar_placeholder(self.combo_libro, "Escribir título...")
        self.combo_libro.grid(row=4, column=0, sticky="ew", ipady=5, pady=(0, 5))
        self.combo_libro.bind("<<ComboboxSelected>>", self.al_seleccionar_libro)

        self.lbl_libro_seleccionado = tk.Label(
            self.frame_central,
            text="Ningún libro seleccionado",
            bg="#f0f0f0",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_libro_seleccionado.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        # --- Libros incluidos en el préstamo
        self.frame_libros = tk.LabelFrame(
            self.frame_central,
            text="Libros del préstamo",
            padx=10,
            pady=10
        )
        self.frame_libros.grid(
            row=6, column=0, sticky="ew", pady=10
        )
        self.frame_libros.columnconfigure(0, weight=1)

        # Controles para agregar ejemplares
        self.controles_libros = tk.Frame(self.frame_libros)
        self.controles_libros.grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        tk.Label(
            self.controles_libros,
            text="Cantidad:"
        ).pack(side="left", padx=5)

        self.cantidad_libro = tk.Spinbox(
            self.controles_libros,
            from_=1,
            to=999,
            width=5
        )
        self.cantidad_libro.pack(side="left", padx=5)

        self.btn_agregar_libro = tk.Button(
            self.controles_libros,
            text="Agregar libro",
            command=self.agregar_libro
        )
        self.btn_agregar_libro.pack(side="left", padx=5)

        # Tabla de libros seleccionados
        self.tabla_libros = ttk.Treeview(
            self.frame_libros,
            columns=("titulo", "cantidad"),
            show="headings",
            height=4,
            selectmode="browse"
        )

        self.tabla_libros.heading("titulo", text="Libro")
        self.tabla_libros.heading("cantidad", text="Cantidad")

        self.tabla_libros.column("titulo", width=260)
        self.tabla_libros.column("cantidad", width=80)

        self.tabla_libros.grid(
            row=1, column=0, sticky="ew", pady=10
        )

        barra_libros = ttk.Scrollbar(
            self.frame_libros,
            orient="vertical",
            command=self.tabla_libros.yview
        )
        barra_libros.grid(row=1, column=1, sticky="ns")

        self.tabla_libros.configure(
            yscrollcommand=barra_libros.set
        )

        self.btn_quitar_libro = tk.Button(
            self.frame_libros,
            text="Quitar seleccionado",
            command=self.quitar_libro
        )
        self.btn_quitar_libro.grid(
            row=2, column=0, sticky="e"
        )

        # --- Fecha de préstamo (automática)
        tk.Label(
            self.frame_central, text="Fecha de préstamo (Automática)"
        ).grid(row=7, column=0, sticky="w", pady=(5, 0))

        self.lbl_fecha_prestamo = tk.Label(
            self.frame_central,
            text=date.today().strftime("%d/%m/%Y"),
            bg="#d9d9d9",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_fecha_prestamo.grid(row=8, column=0, sticky="ew", pady=(0, 10))

        # --- Fecha de devolución estimada
        tk.Label(
            self.frame_central, text="Fecha de devolución estimada"
        ).grid(row=9, column=0, sticky="w", pady=(5, 0))

        self.entry_fecha_devolucion = tk.Entry(self.frame_central, justify="center")
        self._configurar_placeholder(self.entry_fecha_devolucion, "dd/mm/aaaa")
        self.entry_fecha_devolucion.grid(
            row=10, column=0, sticky="ew", ipady=5, pady=(0, 15)
        )

        # --- Botones Confirmar / Cancelar
        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=11, column=0, sticky="ew")
        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.columnconfigure(1, weight=1)

        self.btn_confirmar = tk.Button(
            self.frame_botones,
            text="Confirmar Préstamo",
            command=self.confirmar_prestamo,
        )
        self.btn_confirmar.grid(row=0, column=0, sticky="ew", padx=(0, 5), ipady=6)

        self.btn_cancelar = tk.Button(
            self.frame_botones, text="Cancelar", command=self.cancelar
        )
        self.btn_cancelar.grid(row=0, column=1, sticky="ew", padx=(5, 0), ipady=6)

    def _configurar_placeholder(self, widget, placeholder):
        """Helper para reutilizar la lógica de placeholders en campos de texto/combos."""
        widget.insert(0, placeholder)
        widget.bind(
            "<FocusIn>",
            lambda e: widget.delete(0, tk.END) if widget.get() == placeholder else None,
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
                text=f"Socio Seleccionado (DNI): {dni_ingresado}", bg="#d9f2d9"
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
            bg="#d9f2d9"
        )

    def agregar_libro(self):
        libro = self.libro_seleccionado

        if not libro:
            messagebox.showwarning(
                "Atención",
                "Primero seleccioná un libro."
            )
            return

        # Evitar agregar un título distinto del seleccionado
        if self.opciones_libros.get(
            self.combo_libro.get().strip()
        ) is not libro:
            messagebox.showwarning(
                "Atención",
                "Seleccioná nuevamente el libro."
            )
            return

        try:
            cantidad = int(self.cantidad_libro.get())

            if cantidad <= 0:
                raise ValueError
            
            if cantidad > libro["disponibles"]:
                messagebox.showwarning(
                    "Sin disponibilidad suficiente",
                    f"Solo hay {int(libro['disponibles'])} "
                    "ejemplares disponibles de este libro."
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Cantidad inválida",
                "Ingresá una cantidad entera mayor que cero."
            )
            return

        id_libro = libro["id_libro"]

        if id_libro in self.libros_seleccionados:
            messagebox.showwarning(
                "Libro repetido",
                "Este libro ya está agregado. "
                "Quitalo si querés cambiar su cantidad."
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
        self.cantidad_libro.delete(0, tk.END)
        self.cantidad_libro.insert(0, "1")

        self.lbl_libro_seleccionado.config(
            text="Ningún libro seleccionado",
            bg="#f0f0f0"
        )

    def quitar_libro(self):
        seleccion = self.tabla_libros.selection()

        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un libro para quitarlo."
            )
            return

        id_libro = int(seleccion[0])

        self.libros_seleccionados.pop(id_libro, None)
        self.tabla_libros.delete(seleccion[0])
    
    def confirmar_prestamo(self):
        if not self.socio_seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un socio."
            )
            return

        if self.combo_dni_socio.get().strip() != self.socio_seleccionado:
            messagebox.showwarning(
                "Atención",
                "Volvé a seleccionar un socio válido."
            )
            return

        if not self.libros_seleccionados:
            messagebox.showwarning(
                "Atención",
                "Agregá al menos un libro al préstamo."
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
            messagebox.showwarning(
                "Fecha inválida",
                "Ingresá una fecha válida igual o posterior a hoy."
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
            messagebox.showerror(
                "Error",
                f"No se pudo registrar el préstamo: {error}"
            )
            return

        messagebox.showinfo(
            "Préstamo registrado",
            f"El préstamo {id_prestamo} se registró correctamente."
        )

        self.cancelar()

    def cancelar(self):
        from views.prestamos_views.gestion_prestamos_view import GestionPrestamos
        self.controller.show_frame(GestionPrestamos)