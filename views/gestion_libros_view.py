import tkinter as tk
from tkinter import messagebox, ttk


class GestionLibros(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        tk.Label(
            self, text="Pantalla Gestión Libros", font=("Arial", 14, "bold")
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

        #? --- Buscar
        self.busqueda = tk.Entry(self.frame_central)
        self.busqueda.grid(
            row=0, column=0, sticky="ew", padx=(0, 10), pady=3
        )

        self.boton = tk.Button(
            self.frame_central, text="Buscar", command=self.buscar
        )
        self.boton.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        self.busqueda.bind("<Return>", lambda event: self.buscar())

        #? --- Filtros y Ordnar
        self.botones_filtros_frame = tk.Frame(self.frame_central)
        self.botones_filtros_frame.grid(
            row=1, column=0, columnspan=2, sticky="nsew", pady=5
        )
        self.botones_filtros_frame.columnconfigure(0, weight=1)
        self.botones_filtros_frame.columnconfigure(1, weight=1)

        self.boton_ordenar = tk.Button(
            self.botones_filtros_frame, text="Ordenar A-Z", command=self.ordenar
        )
        self.boton_ordenar.grid(row=0, column=0, sticky="w")

        self.boton_filtrar = tk.Button(
            self.botones_filtros_frame,
            text="Limpiar Filtro",
            command=self.limpiar_busqueda,
        )
        self.boton_filtrar.grid(row=0, column=1, sticky="e")

        #? --- Tabla de Libros 
        self.frame_tabla = tk.Frame(self.frame_central)
        self.frame_tabla.grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=10
        )
        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        columnas = ("id", "titulo", "autor", "genero")
        self.tabla = ttk.Treeview(
            self.frame_tabla, columns=columnas, show="headings"
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("titulo", text="Título")
        self.tabla.heading("autor", text="Autor")
        self.tabla.heading("genero", text="Género")

        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("titulo", width=180)
        self.tabla.column("autor", width=140)
        self.tabla.column("genero", width=100)

        scrollbar = ttk.Scrollbar(
            self.frame_tabla, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Botones de Acción (Inferiores)
        self.frame_acciones = tk.Frame(self.frame_central)
        self.frame_acciones.grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=5
        )

        self.btn_eliminar = tk.Button(
            self.frame_acciones,
            text="Eliminar Seleccionado",
            command=self.eliminar_libro,
        )
        self.btn_eliminar.pack(side="right", padx=5)

        #! Ejemplo de datos
        self.libros_datos = [
            (1, "Don Quijote de la Mancha", "Miguel de Cervantes", "Novela"),
            (2, "Cien años de soledad", "Gabriel García Márquez", "Realismo Mágico"),
            (3, "El Principito", "Antoine de Saint-Exupéry", "Fábula"),
        ]
        self.actualizar_tabla(self.libros_datos)

    def actualizar_tabla(self, lista_libros):
        """Limpia y vuelve a cargar los datos en la tabla."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for libro in lista_libros:
            self.tabla.insert("", "end", values=libro)

    def buscar(self, event=None):
        """Filtra la lista de libros según lo ingresado."""
        texto = self.busqueda.get().strip().lower()
        if not texto:
            self.actualizar_tabla(self.libros_datos)
            return

        resultados = [
            libro
            for libro in self.libros_datos
            if texto in libro[1].lower() or texto in libro[2].lower()
        ]
        self.actualizar_tabla(resultados)

    def limpiar_busqueda(self):
        """Restablece la búsqueda y muestra todos los datos."""
        self.busqueda.delete(0, tk.END)
        self.actualizar_tabla(self.libros_datos)

    def ordenar(self):
        """Ordena los libros alfabéticamente por título."""
        libros_ordenados = sorted(self.libros_datos, key=lambda x: x[1])
        self.actualizar_tabla(libros_ordenados)

    def eliminar_libro(self):
        """Elimina la fila seleccionada en la tabla."""
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Atención", "Por favor, selecciona un libro de la lista."
            )
            return

        item = self.tabla.item(seleccion)
        libro_id = item["values"][0]

        self.libros_datos = [
            libro for libro in self.libros_datos if libro[0] != libro_id
        ]
        self.actualizar_tabla(self.libros_datos)