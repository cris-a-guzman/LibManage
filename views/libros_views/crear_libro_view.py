import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from views.components.base_frame import BaseFrame
from api_libros.open_library import LibraryApi
from views.components.estilo import CUERPO

class CrearLibro(BaseFrame):
    def __init__(self, parent, controller, conexion, libro_datos=None):
        super().__init__(parent, controller, conexion)
        self.controller = controller
        self.libro_datos = libro_datos or {}
        
        # INICIALIZACIÓN PEREZOSA (Lazy Loading): No instanciamos la API aquí.
        # Se instanciará solo cuando el usuario haga clic en "Buscar".
        self.api_busqueda = None 
        self.docs = []

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.crear_titulo("Gestión de Libro")

        # CONTENEDOR PRINCIPAL LIMPIO (Sin bootstyle=PRIMARY)
        self.frame_central = tb.Frame(self)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        self.frame_central.columnconfigure((0, 1), weight=1, uniform="columnas")
        self.frame_central.rowconfigure(0, weight=1)
        
        # 1. SECCIÓN IZQUIERDA: LabelFrame para agrupar visualmente el formulario
        self.frame_formulario = tb.Labelframe(self.frame_central, text="Detalles del Libro", padding=18, bootstyle=PRIMARY)
        self.frame_formulario.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

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

        self.txt_titulo = self.entradas["titulo"]
        self.txt_autor = self.entradas["autor"]
        self.txt_anio = self.entradas["anio"]
        self.txt_cantidad = self.entradas["cantidad"]
        self.txt_isbn = self.entradas["isbn"]

        # Botón con estilo outline para que no sea tan pesado visualmente
        self.btn_buscar = tb.Button(self.frame_formulario, text="Buscar Online", bootstyle="info-outline", command=self.buscar_libro)
        self.btn_buscar.grid(row=1, column=1, padx=10, pady=4, ipady=2)
        
        # 2. SECCIÓN DERECHA: LabelFrame para la API
        self.frame_api = tb.Labelframe(self.frame_central, text="Búsqueda Externa", padding=18, bootstyle=INFO)
        self.frame_api.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        self.frame_api.rowconfigure(1, weight=1)
        self.frame_api.columnconfigure(0, weight=1)

        self.lbl_busqueda = tb.Label(self.frame_api, text="Los Resultados se listarán debajo", justify="center", font=CUERPO, bootstyle=SECONDARY)
        self.lbl_busqueda.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Configuración del Treeview (Bootstyle por defecto para mejor integración)
        columnas = {
            "id": ("ID", 60, "center"),
            "titulo": ("Título", 250, "w"),
            "autor": ("Autor", 200, "w"),
            "año": ("Año", 80, "center")
        }

        self.tabla = tb.Treeview(
            self.frame_api, 
            columns=tuple(columnas.keys()), 
            show="headings", 
            selectmode="browse",
            bootstyle=INFO
        )

        for col, (texto, ancho, fija) in columnas.items():
            self.tabla.heading(col, text=texto)
            self.tabla.column(col, width=ancho, minwidth=60, stretch=False, anchor=fija)

        sb_y = tb.Scrollbar(self.frame_api, orient="vertical", command=self.tabla.yview, bootstyle="round")
        self.tabla.configure(yscrollcommand=sb_y.set)

        self.tabla.grid(row=1, column=0, sticky="nsew")
        sb_y.grid(row=1, column=1, sticky="ns")
        self.tabla.bind("<Double-1>", lambda e: self.seleccionar_libro_tree())
        
        # 3. ZONA DE BOTONES (Sin fondos de color, usando estilos semánticos)
        self.frame_botones = tb.Frame(self.frame_central)
        self.frame_botones.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(20, 0))
        
        for i in range(3):
            self.frame_botones.columnconfigure(i, weight=1)

        tb.Button(self.frame_botones, text="Guardar Cambios", bootstyle=SUCCESS, command=self.guardar_cambios)\
            .grid(row=0, column=0, padx=6, ipady=8, sticky="ew")

        tb.Button(self.frame_botones, text="Cancelar y volver atrás", bootstyle="secondary-outline", command=self.descartar)\
            .grid(row=0, column=2, padx=6, ipady=8, sticky="ew")

        if self.libro_datos:
            tb.Button(self.frame_botones, text="Dar de baja", bootstyle="danger-outline", command=self.eliminar_libro)\
                .grid(row=0, column=1, padx=6, ipady=8, sticky="ew")

    # --- MODIFICACIÓN EN BUSCAR LIBRO ---
    def buscar_libro(self):
        titulo = self.txt_titulo.get().strip()
        if not titulo or titulo == "Título del Libro":
            Messagebox.show_warning("Ingresa un título para buscar.", title="Atención")
            return

        self.lbl_busqueda.config(text=f"Buscando: {titulo}...")
        self.update() 
        
        # Inicializamos la API solo si el usuario decide usarla (evita lentitud al abrir la pantalla)
        if self.api_busqueda is None:
            self.api_busqueda = LibraryApi()

        datos_libros, self.docs = self.api_busqueda.buscar_titulo(titulo)

        if datos_libros is None:
            self.lbl_busqueda.config(text="No se encontraron libros o falló la conexión.")
            self.actualizar_treeview([])
        else:
            self.lbl_busqueda.config(text=f"Resultados para: {titulo}")
            self.actualizar_treeview(datos_libros)

    # (El resto de tus métodos se mantienen exactamente igual)
    def seleccionar_libro_tree(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        id_libro = self.tabla.item(seleccion[0])["values"][0]
        datos = self.api_busqueda.funcion_final(id_libro, self.docs)
        self.cargar_datos(datos)
        
    def crear_etiqueta(self, texto, fila):
        label = tb.Label(self.frame_formulario, text=texto, justify="center", width=30, bootstyle=PRIMARY)
        label.grid(row=fila, column=0, pady=(8, 2))
        return label
    
    def crear_campo(self, placeholder, fila):
        entry = tb.Entry(self.frame_formulario, justify="center", width=30, bootstyle=PRIMARY)
        entry.insert(0, placeholder)
        entry.grid(row=fila, column=0, pady=(0, 6), ipady=6)

        entry.bind("<FocusIn>", lambda e: entry.delete(0, "end") if entry.get() == placeholder else None)
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
            entry.delete(0, "end")
            entry.insert(0, str(valor))

    def cargar_datos(self, datos):
        # Desempaquetamos la tupla en el orden exacto que la devuelve la API
        titulo, autor, isbn, anio = datos
        
        self.set_entry(self.txt_titulo, titulo)
        self.set_entry(self.txt_autor, autor)
        self.set_entry(self.txt_isbn, isbn)
        self.set_entry(self.txt_anio, anio)
        
        
    def guardar_cambios(self):
        titulo = self.txt_titulo.get()
        autor = self.txt_autor.get().strip()
        anio = self.txt_anio.get().strip()
        cantidad = self.txt_cantidad.get().strip()
        isbn = self.txt_isbn.get().strip()

        if titulo in ("", "Titulo del Libro") or autor in ("", "Autor"):
            Messagebox.show_warning(
                "El título y el autor son obligatorios.",
                title="Datos incompletos"
            )
            return

        try:
            anio = None if anio in ("", "Año") else int(anio)
            cantidad = int(cantidad)

            if (anio is not None and anio <= 0) or cantidad < 0:
                raise ValueError

        except ValueError:
            Messagebox.show_warning(
                "Ingresá un año válido y una cantidad entera no negativa.",
                title="Datos inválidos"
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
            Messagebox.show_error(
                f"No se pudo guardar el libro: {error}",
                title="Error al guardar"
            )
            return

        Messagebox.show_info(mensaje, title="Operación exitosa")
                # Regresar al listado
        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)
        
    def descartar(self):
        Messagebox.show_info(title="Libro Descartado", message="Libro descartado exitosamente.\nVolviendo atrás...")
        self.volver()
        
    def volver(self):
        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)
