import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from views.components.base_frame import BaseFrame
from views.components.formulario_desplazable import FormularioDesplazable
from api_libros.open_library import LibraryApi
#! No guarda el ISBN ni los autores de forma correcta

class CrearLibro(BaseFrame):
    def __init__(self, parent, controller, libro_datos=None):
        super().__init__(parent, controller)
        self.controller = controller
        self.libro_datos = libro_datos or {}
        
        self.api_busqueda = LibraryApi()
        # self.ApiLibros = ApiLibros() # Descomentar e inicializar si corresponde

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        
        self.columnconfigure(0, weight=1)
        
        self.crear_titulo("Crear Libro")
            
        # Frame central
        
        self.scroll_formulario = FormularioDesplazable(self)
        self.scroll_formulario.grid(
            row=1, column=0, sticky="nsew", padx=10, pady=(5, 10)
        )

        self.frame_central = tk.Frame(
            self.scroll_formulario.contenido,
            bd=1,
            relief="solid",
            padx=20,
            pady=20
        )
        self.frame_central.pack(fill="both", expand=True)
        # Distribución en dos columnas
        self.frame_central.columnconfigure(0, weight=1, uniform="columnas")
        self.frame_central.columnconfigure(1, weight=1, uniform="columnas")
        self.frame_central.rowconfigure(0, weight=1)

        # Frame del formulario (izquierda)
        self.frame_formulario = tk.Frame(self.frame_central)
        self.frame_formulario.grid(
            row=0, column=0, sticky="nsew", padx=10, pady=10
        )

        # Frame de la API (derecha)
        self.frame_api = tk.Frame(
            self.frame_central,
            bd=1,
            relief="solid"
        )
        self.frame_api.grid(
            row=0, column=1, sticky="nsew", padx=10, pady=10
        )
        
        
        #! Etiqueta de busqueda
        self.lbl_busqueda = tk.Label(self.frame_api, text="Los Resultados se listarón debajo", justify="center", width=40)
        self.lbl_busqueda.grid(row=0, column=0, pady=4, ipady=6)

       #! --- TREEVIEW  CON SCROLL HORIZONTAL ---
        columnas = ("id", "titulo", "autor", "año")
        
        self.tabla = ttk.Treeview(
            self.frame_api,
            columns=columnas,
            show="headings",
            selectmode="browse",
            style="Prestamos.Treeview"
        )

        encabezados = {
            "id": "ID",
            "titulo": "Título",
            "autor": "Autor",
            "año": "Año"
        }

        # Anchos amplios para forzar el scroll horizontal si la ventana es pequeña
        anchos = {
            "id": 60,
            "titulo": 250,
            "autor": 200,
            "año": 80
        }

        for columna in columnas:
            self.tabla.heading(columna, text=encabezados[columna])
            self.tabla.column(
                columna,
                width=anchos[columna],
                minwidth=60,
                stretch=False, 
                anchor="center" if columna in ("id", "año") else "w"
            )

        scrollbar_y = ttk.Scrollbar(
            self.frame_api,
            orient="vertical",
            command=self.tabla.yview
        )

        scrollbar_x = ttk.Scrollbar(
            self.frame_api,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        #? Doble clic sobre una fila = modificar ese libro
        self.tabla.bind("<Double-1>", lambda e: self.seleccionar_libro_tree())

        # Configurar la retícula del contenedor frame_api
        self.frame_api.rowconfigure(1, weight=1)
        self.frame_api.columnconfigure(0, weight=1)
        

        # Ubicación en la grilla
        self.lbl_busqueda.grid(row=0, column=0, columnspan=2, pady=4)
        self.tabla.grid(row=1, column=0, sticky="nsew")
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        scrollbar_x.grid(row=2, column=0, sticky="ew")
        
        # Textos y formulario
        self.lbl_titulo = self.crear_etiqueta("Titulo", 0)
        self.txt_titulo = self.crear_campo("Titulo del Libro", 1)
        self.boton_titulo_buscar = tk.Button(self.frame_formulario, text="Buscar Libro", command=self.buscar_libro)
        self.boton_titulo_buscar.grid(row=1, column=1, pady=4, ipady=6)
        
        self.lbl_autor = self.crear_etiqueta("Autor", 2)
        self.txt_autor = self.crear_campo("Autor", 3)
        self.lbl_anio = self.crear_etiqueta("Año", 4)
        self.txt_anio = self.crear_campo("Año", 5)
        self.lbl_cantidad = self.crear_etiqueta("Cantidad Total", 6)
        self.txt_cantidad = self.crear_campo("Cantidad total", 7)
        self.lbl_isbn = self.crear_etiqueta("ISBN", 8)
        self.txt_isbn = self.crear_campo("ISBN", 9)

        # Frame Botones
        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        
        for i in range(3):
            self.frame_botones.columnconfigure(i, weight=1)

        self.btn_guardar = tk.Button(
            self.frame_botones, text="Guardar Cambios", command=self.guardar_cambios
        )
        self.btn_guardar.grid(row=0, column=0, padx=5, ipady=3, sticky="ew")

        self.btn_cancelar = tk.Button(
            self.frame_botones, text="Cancelar y volver atras", command=self.descartar
        )
        self.btn_cancelar.grid(row=0, column=2, padx=5, ipady=3, sticky="ew")

        if self.libro_datos:
            self.btn_eliminar = tk.Button(
                self.frame_botones, text="Dar de baja", command=self.eliminar_libro
            )
            self.btn_eliminar.grid(row=0, column=1, padx=5, ipady=3, sticky="ew")
    
    def seleccionar_libro_tree(self):
        seleccion = self.tabla.selection()
        id_libro = self.tabla.item(seleccion[0])["values"][0]
        datos = self.api_busqueda.funcion_final(id_libro, self.docs)
        self.cargar_datos(datos)
        
    def buscar_libro(self):
        titulo = self.txt_titulo.get().strip()
        self.lbl_busqueda.config(text=f"Buscando: {titulo}")
        
        resultado = self.api_busqueda.buscar_titulo(titulo)

        # Limpieza previa de la tabla
        #! Esto va en otra funcion
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        if resultado is None:
            self.lbl_busqueda.config(text="No se encontraron libros.")
        else:
            datos_libros, self.docs = resultado
            for i in datos_libros:
                self.tabla.insert(
                    "", "end", values=(
                        i.get("id", ""), 
                        i.get("titulo", ""), 
                        i.get("autor", ""), 
                        i.get("año", "")
                    )
                )

    def actualizar_treeview(self, datos_libros):
        pass
            
    def crear_etiqueta(self, titulo, fila, columna=0):
        label = tk.Label(self.frame_formulario, text=titulo, justify="center", width=40)
        label.grid(row=fila, column=0, pady=4, ipady=6)
        return label
        
    def crear_campo(self, placeholder, fila):
        entry = tk.Entry(self.frame_formulario, justify="center", width=40)
        entry.insert(0, placeholder)
        entry.grid(row=fila, column=0, pady=4, ipady=6)
        
        entry.bind("<FocusIn>", lambda e, p=placeholder: entry.delete(0, tk.END) if entry.get() == p else None)
        return entry

    def cargar_datos(self, datos):
        self.set_entry(self.txt_titulo, datos.get("titulo", ""))
        self.set_entry(self.txt_autor, datos.get("autor", ""))
        self.set_entry(self.txt_isbn, datos.get("isbn", ""))
        self.set_entry(self.txt_anio, datos.get("año", ""))

    def set_entry(self, entry, valor):
        if valor:
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def guardar_cambios(self):
        titulo = self.txt_titulo.get().strip()
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

        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)

    def descartar(self):
        from views.libros_views.gestion_libros_view import GestionLibros
        messagebox.showinfo(title="Libro Descartado", message="Libro Descartado exitosamente.\n Volviendo atrás...")
        self.controller.show_frame(GestionLibros)
