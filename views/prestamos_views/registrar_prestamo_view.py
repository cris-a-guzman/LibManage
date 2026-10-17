import tkinter as tk
from tkinter import messagebox
from datetime import date, datetime
from views.components.lista_desplegable import AutocompleteCombobox
from views.components.base_frame import BaseFrame
from views.components.formulario_desplazable import FormularioDesplazable


class RegistrarPrestamo(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        # Carga de datos desde la API/Repositories
        self.dni_socios = self.ApiSocios.obtener_socios_dni()
        self.titulos_ids_libros = self.ApiLibros.obtener_titulos_ids()

        self.socio_seleccionado = None
        self.libro_seleccionado = None

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

        titulos = [x["titulo"] for x in self.titulos_ids_libros]

        self.combo_libro = AutocompleteCombobox(
            self.frame_central, width=30, font=("Arial", 10)
        )
        self.combo_libro.set_completion_list(titulos)
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

        # --- Fecha de préstamo (automática)
        tk.Label(
            self.frame_central, text="Fecha de préstamo (Automática)"
        ).grid(row=6, column=0, sticky="w", pady=(5, 0))

        self.lbl_fecha_prestamo = tk.Label(
            self.frame_central,
            text=date.today().strftime("%d/%m/%Y"),
            bg="#d9d9d9",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_fecha_prestamo.grid(row=7, column=0, sticky="ew", pady=(0, 10))

        # --- Fecha de devolución estimada
        tk.Label(
            self.frame_central, text="Fecha de devolución estimada"
        ).grid(row=8, column=0, sticky="w", pady=(5, 0))

        self.entry_fecha_devolucion = tk.Entry(self.frame_central, justify="center")
        self._configurar_placeholder(self.entry_fecha_devolucion, "dd/mm/aaaa")
        self.entry_fecha_devolucion.grid(
            row=9, column=0, sticky="ew", ipady=5, pady=(0, 15)
        )

        # --- Botones Confirmar / Cancelar
        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=10, column=0, sticky="ew")
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
        titulo_ingresado = self.combo_libro.get().strip()
        if titulo_ingresado and titulo_ingresado != "Escribir título...":
            # Buscamos el objeto/ID correspondiente en la lista traída del repo
            libro_encontrado = next(
                (item for item in self.titulos_ids_libros if item["titulo"] == titulo_ingresado),
                None,
            )
            if libro_encontrado:
                self.libro_seleccionado = libro_encontrado
                self.lbl_libro_seleccionado.config(
                    text=f"Libro Seleccionado: {libro_encontrado['titulo']}", bg="#d9f2d9"
                )

    
    def confirmar_prestamo(self):
        if not self.socio_seleccionado or not self.libro_seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un socio y un libro."
            )
            return

        # Comprobar que no se modificaron los campos tras seleccionar
        if (
            self.combo_dni_socio.get().strip() != self.socio_seleccionado
            or self.combo_libro.get().strip()
            != self.libro_seleccionado["titulo"]
        ):
            messagebox.showwarning(
                "Atención",
                "Volvé a seleccionar un socio y un libro válidos."
            )
            return

        # Validar la fecha ingresada
        fecha_texto = self.entry_fecha_devolucion.get().strip()

        try:
            fecha_devolucion = datetime.strptime(
                fecha_texto, "%d/%m/%Y"
            ).date()

            if fecha_devolucion < date.today():
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Fecha inválida",
                "Ingresá una fecha válida, igual o posterior a hoy, "
                "con formato dd/mm/aaaa."
            )
            return

        # Registrar el préstamo en MySQL
        try:
            id_prestamo = self.ApiPrestamos.crear_prestamo(
                dni_socio=self.socio_seleccionado,
                id_libro=self.libro_seleccionado["id_libro"],
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