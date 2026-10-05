import tkinter as tk
from tkinter import messagebox
from datetime import date


class RegistrarPrestamo(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #! Datos de ejemplo para busqueda
        self.socios_datos = [
            {"nombre": "Juan Perez", "dni": "2011111111"},
            {"nombre": "Lucia Diaz", "dni": "2022222222"},
        ]
        self.libros_datos = [
            {"titulo": "1984", "autor": "George Owell"},
            {"titulo": "Rayuela", "autor": "Julio Cortazar"},
        ]

        self.socio_seleccionado = None
        self.libro_seleccionado = None

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        tk.Label(
            self, text="Registrar Prestamo", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, sticky="new", pady=12)

        #? --- Frame Central
        self.frame_central = tk.Frame(self, padx=20, pady=5)
        self.frame_central.grid(row=1, sticky="nsew")
        self.frame_central.columnconfigure(0, weight=1)

        #? --- Buscar Socio
        tk.Label(self.frame_central, text="buscar socio").grid(
            row=0, column=0, sticky="w", pady=(5, 0)
        )
        self.busqueda_socio = tk.Entry(self.frame_central, justify="center")
        self.busqueda_socio.insert(0, "Escribir nombre o DNI")
        self.busqueda_socio.grid(row=1, column=0, sticky="ew", ipady=5, pady=(0, 5))
        self.busqueda_socio.bind(
            "<FocusIn>",
            lambda e: self.busqueda_socio.delete(0, tk.END)
            if self.busqueda_socio.get() == "Escribir nombre o DNI" else None,
        )
        self.busqueda_socio.bind("<Return>", lambda e: self.buscar_socio())

        self.lbl_socio_seleccionado = tk.Label(
            self.frame_central,
            text="Ningun socio seleccionado",
            bg="#f0f0f0",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_socio_seleccionado.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        #? --- Buscar Libro
        tk.Label(self.frame_central, text="buscar libro (solo disponibles)").grid(
            row=3, column=0, sticky="w", pady=(5, 0)
        )
        self.busqueda_libro = tk.Entry(self.frame_central, justify="center")
        self.busqueda_libro.insert(0, "Escribir titulo...")
        self.busqueda_libro.grid(row=4, column=0, sticky="ew", ipady=5, pady=(0, 5))
        self.busqueda_libro.bind(
            "<FocusIn>",
            lambda e: self.busqueda_libro.delete(0, tk.END)
            if self.busqueda_libro.get() == "Escribir titulo..." else None,
        )
        self.busqueda_libro.bind("<Return>", lambda e: self.buscar_libro())

        self.lbl_libro_seleccionado = tk.Label(
            self.frame_central,
            text="Ningun libro seleccionado",
            bg="#f0f0f0",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_libro_seleccionado.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        #? --- Fecha de prestamo (automatica)
        tk.Label(self.frame_central, text="Fecha de prestamo (Automatica)").grid(
            row=6, column=0, sticky="w", pady=(5, 0)
        )
        self.lbl_fecha_prestamo = tk.Label(
            self.frame_central,
            text=date.today().strftime("%d/%m/%Y"),
            bg="#d9d9d9",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_fecha_prestamo.grid(row=7, column=0, sticky="ew", pady=(0, 10))

        #? --- Fecha de devolucion estimada
        tk.Label(self.frame_central, text="Fecha de devolucion estimada").grid(
            row=8, column=0, sticky="w", pady=(5, 0)
        )
        self.entry_fecha_devolucion = tk.Entry(self.frame_central, justify="center")
        self.entry_fecha_devolucion.insert(0, "dd/mm/aaaa")
        self.entry_fecha_devolucion.grid(row=9, column=0, sticky="ew", ipady=5, pady=(0, 15))
        self.entry_fecha_devolucion.bind(
            "<FocusIn>",
            lambda e: self.entry_fecha_devolucion.delete(0, tk.END)
            if self.entry_fecha_devolucion.get() == "dd/mm/aaaa" else None,
        )

        #? --- Botones Confirmar / Cancelar
        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=10, column=0, sticky="ew")
        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.columnconfigure(1, weight=1)

        self.btn_confirmar = tk.Button(
            self.frame_botones,
            text="Confirmar Prestamo",
            command=self.confirmar_prestamo,
        )
        self.btn_confirmar.grid(row=0, column=0, sticky="ew", padx=(0, 5), ipady=6)

        self.btn_cancelar = tk.Button(
            self.frame_botones, text="Cancelar", command=self.cancelar
        )
        self.btn_cancelar.grid(row=0, column=1, sticky="ew", padx=(5, 0), ipady=6)

    def buscar_socio(self):
        texto = self.busqueda_socio.get().strip().lower()
        for socio in self.socios_datos:
            if texto == socio["nombre"].lower() or texto == socio["dni"]:
                self.socio_seleccionado = socio
                self.lbl_socio_seleccionado.config(
                    text=f"Seleccionado: {socio['nombre']}  (DNI: {socio['dni']})",
                    bg="#d9f2d9",
                )
                return
        messagebox.showwarning("Atención", "Socio no encontrado.")

    def buscar_libro(self):
        texto = self.busqueda_libro.get().strip().lower()
        for libro in self.libros_datos:
            if texto == libro["titulo"].lower():
                self.libro_seleccionado = libro
                self.lbl_libro_seleccionado.config(
                    text=f"Seleccionado: {libro['titulo']} - {libro['autor']}",
                    bg="#d9f2d9",
                )
                return
        messagebox.showwarning("Atención", "Libro no encontrado o no disponible.")

    def confirmar_prestamo(self):
        if not self.socio_seleccionado or not self.libro_seleccionado:
            messagebox.showwarning(
                "Atención", "Debes seleccionar un socio y un libro."
            )
            return
        fecha_devolucion = self.entry_fecha_devolucion.get().strip()
        if not fecha_devolucion or fecha_devolucion == "dd/mm/aaaa":
            messagebox.showwarning(
                "Atención", "Ingresa la fecha de devolución estimada."
            )
            return

        print(
            f"Prestamo confirmado: {self.socio_seleccionado['nombre']} "
            f"- {self.libro_seleccionado['titulo']} - Devuelve: {fecha_devolucion}"
        )
        self.cancelar()

    def cancelar(self):
        from views.gestion_prestamos_view import GestionPrestamos
        self.controller.show_frame(GestionPrestamos)