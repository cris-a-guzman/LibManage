import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame
from views.components.formulario_desplazable import FormularioDesplazable
from api_libros.open_library import LibraryApi

class CrearLibro(BaseFrame):
    def __init__(self, parent, controller, conexion, libro_datos=None):
        super().__init__(parent, controller, conexion)
        self.controller = controller
        self.libro_datos = libro_datos or {}
        self.api_busqueda = LibraryApi()
        self.docs = []

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.crear_titulo("Crear Libro")

        self.scroll_formulario = FormularioDesplazable(self)
        self.scroll_formulario.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        self.frame_central = tk.Frame(self.scroll_formulario.contenido, bd=1, relief="solid", padx=20, pady=20)
        self.frame_central.pack(fill="both", expand=True)
        self.frame_central.columnconfigure((0, 1), weight=1, uniform="columnas")
        self.frame_central.rowconfigure(0, weight=1)
        
        self.frame_formulario = tk.Frame(self.frame_central)
        self.frame_formulario.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        #? campos (clave, etiqueta, placeholder, fila)
        campos = [
            ("titulo", "Título", "Título del Libro", 0),
            ("autor", "Autor", "Autor", 2),
            ("anio", "Año", "Año", 4),
            ("cantidad", "Cantidad Total", "Cantidad total", 6),
            ("isbn", "ISBN", "ISBN", 8),
        ]

        self.entradas = {}
        for clave, texto_label, placeholder, fila in campos:
            self.crear_etiqueta(texto_label, fila)
            entrada = self.crear_campo(placeholder, fila + 1)
            self.entradas[clave] = entrada

        # Alias para mantener compatibilidad con métodos existentes
        self.txt_titulo = self.entradas["titulo"]
        self.txt_autor = self.entradas["autor"]
        self.txt_anio = self.entradas["anio"]
        self.txt_cantidad = self.entradas["cantidad"]
        self.txt_isbn = self.entradas["isbn"]

        # Botón de búsqueda de libro integrado junto al campo de título
        self.btn_buscar = tk.Button(self.frame_formulario, text="Buscar Libro", command=self.buscar_libro)
        self.btn_buscar.grid(row=1, column=1, padx=5, pady=4, ipady=4)
        
        self.frame_api = tk.Frame(self.frame_central, bd=1, relief="solid")
        self.frame_api.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_api.rowconfigure(1, weight=1)
        self.frame_api.columnconfigure(0, weight=1)

        self.lbl_busqueda = tk.Label(self.frame_api, text="Los Resultados se listarón debajo", justify="center")
        self.lbl_busqueda.grid(row=0, column=0, columnspan=2, pady=6)

        # Configuración del Treeview
        columnas = {
            "id": ("ID", 60, "center"),
            "titulo": ("Título", 250, "w"),
            "autor": ("Autor", 200, "w"),
            "año": ("Año", 80, "center")
        }

        self.tabla = ttk.Treeview(
            self.frame_api, 
            columns=tuple(columnas.keys()), 
            show="headings", 
            selectmode="browse", 
            style="Prestamos.Treeview"
        )

        for col, (texto, ancho, fija) in columnas.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, minwidth=60, stretch=False, anchor=fija)

        # Scrollbars
        sb_y = ttk.Scrollbar(self.frame_api, orient="vertical", command=self.tabla.yview)
        sb_x = ttk.Scrollbar(self.frame_api, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        self.tabla.grid(row=1, column=0, sticky="nsew")
        sb_y.grid(row=1, column=1, sticky="ns")
        sb_x.grid(row=2, column=0, sticky="ew")

        self.tabla.bind("<Double-1>", lambda e: self.seleccionar_libro_tree())
        
        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(15, 0))
        
        for i in range(3):
            self.frame_botones.columnconfigure(i, weight=1)

        tk.Button(self.frame_botones, text="Guardar Cambios", command=self.guardar_cambios)\
            .grid(row=0, column=0, padx=5, ipady=3, sticky="ew")

        tk.Button(self.frame_botones, text="Cancelar y volver atrás", command=self.descartar)\
            .grid(row=0, column=2, padx=5, ipady=3, sticky="ew")

        if self.libro_datos:
            tk.Button(self.frame_botones, text="Dar de baja", command=self.eliminar_libro)\
                .grid(row=0, column=1, padx=5, ipady=3, sticky="ew")
                
    def crear_etiqueta(self, texto, fila):
        label = tk.Label(self.frame_formulario, text=texto, justify="center", width=30)
        label.grid(row=fila, column=0, pady=2)
        return label
    
    def crear_campo(self, placeholder, fila):
        entry = tk.Entry(self.frame_formulario, justify="center", width=30)
        entry.insert(0, placeholder)
        entry.grid(row=fila, column=0, pady=4, ipady=4)

        entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if entry.get() == placeholder else None)
        entry.bind("<FocusOut>", lambda e: entry.insert(0, placeholder) if not entry.get().strip() else None)
        return entry
    
    def actualizar_treeview(self, datos_libros):
        """Limpia y carga las filas en la tabla del Treeview."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for libro in datos_libros:
            self.tabla.insert("", "end", values=(
                libro.get("id", ""),
                libro.get("titulo", ""),
                libro.get("autor", ""),
                libro.get("año", "")
            ))
            
    def set_entry(self, entry, valor):
        if valor:
            entry.delete(0, tk.END)
            entry.insert(0, str(valor))

    def cargar_datos(self, datos):
        # Desempaquetamos la tupla en el orden exacto que la devuelve la API
        titulo, autor, isbn, anio = datos
        
        self.set_entry(self.txt_titulo, titulo)
        self.set_entry(self.txt_autor, autor)
        self.set_entry(self.txt_isbn, isbn)
        self.set_entry(self.txt_anio, anio)
        
    def buscar_libro(self):
        titulo = self.txt_titulo.get().strip()
        if not titulo or titulo == "Título del Libro":
            messagebox.showwarning("Atención", "Ingresa un título para buscar.")
            return

        self.lbl_busqueda.config(text=f"Buscando: {titulo}")
        self.update() #? Fuerza a Tkinter a repintar el label antes de que la API lo bloquee
        
        datos_libros, self.docs = self.api_busqueda.buscar_titulo(titulo)

        if datos_libros is None:
            self.lbl_busqueda.config(text="No se encontraron libros o falló la conexión.")
            self.actualizar_treeview([])
        else:
            self.lbl_busqueda.config(text=f"Resultados para: {titulo}")
            self.actualizar_treeview(datos_libros)
            
    def seleccionar_libro_tree(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_libro = self.tabla.item(seleccion[0])["values"][0]
        datos = self.api_busqueda.funcion_final(id_libro, self.docs)
        self.cargar_datos(datos)
        
        
    def guardar_cambios(self):
        titulo = self.txt_titulo.get()
        autor = self.txt_autor.get().strip()
        anio = self.txt_anio.get().strip()
        cantidad = self.txt_cantidad.get().strip()
        isbn = self.txt_isbn.get().strip()

        if titulo in ("", "Titulo del Libro") or autor in ("", "Autor"):
            messagebox.showwarning(
                "Datos incompletos",
                "El título y el autor son obligatorios."
            )
            return

        try:
            anio = None if anio in ("", "Año") else int(anio)
            cantidad = int(cantidad)

            if (anio is not None and anio <= 0) or cantidad < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Datos inválidos",
                "Ingresá un año válido y una cantidad entera no negativa."
            )
            return

        try:
            if self.libro_datos:
                self.ApiLibros.actualizar_libro(
                    self.libro_datos["id_libro"],
                    titulo,
                    autor,
                    anio,
                    cantidad,
                    isbn
                )
                mensaje = "Libro modificado correctamente."
            else:
                nuevo_id = self.ApiLibros.crear_libro(titulo, autor, anio, cantidad, isbn)
                mensaje = f"Libro creado correctamente con ID {nuevo_id}."

        except Exception as error:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudo guardar el libro: {error}"
            )
            return

        messagebox.showinfo("Operación exitosa", mensaje)
                # Regresar al listado
        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)
        
    def descartar(self):
        messagebox.showinfo(title="Libro Descartado", message="Libro descartado exitosamente.\nVolviendo atrás...")
        self.volver()
        
    def volver(self):
        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)