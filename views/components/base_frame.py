import tkinter as tk
from tkinter import ttk, messagebox

from repositories.libro_repo import LibroRepo
from repositories.prestamo_repo import PrestamoRepo
from repositories.socio_repo import SociosRepo

class BaseFrame(tk.Frame):
    
    def __init__(self, parent, controller, conexion):
        super().__init__(parent)
        self.controller = controller
        self.conexion = conexion
        self.ApiLibros= LibroRepo(self.conexion)
        self.ApiPrestamos = PrestamoRepo(self.conexion)
        self.ApiSocios = SociosRepo(self.conexion)
        #? Configuración del grid principal de la pantalla
        
        self.rowconfigure(0, weight=0) # Título
        self.rowconfigure(1, weight=1) # Contenido principal
        self.rowconfigure(2, weight=0) # Espacio libre
        self.rowconfigure(3, weight=0) # Botones inferiores
        self.columnconfigure(0, weight=1) 
        
        self.frame_central = self.crear_frame_central()
        
        #? Frame para los botones inferiores
        self.frame_inferior = tk.Frame(self)
        self.frame_inferior.grid(
            row=3, column=0, sticky="ew", padx=10, pady=(5, 10)
        )
        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)
        
    def crear_titulo(self, titulo):
        titulo_label = tk.Label(
            self, 
            text= titulo, 
            font=("Arial", 14, "bold"),
            bd=1,
            pady=8
        )
        titulo_label.grid(row=0, column=0, sticky="new", padx=10, pady=(10, 5))
        return titulo_label
        
    def crear_frame_central(self):
        self.frame_central = tk.Frame(self, bd=1, relief="solid")
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        return self.frame_central
    
    def crear_barra_busqueda(self, placeholder, funcion_buscar):
        self.placeholder_busqueda = placeholder
        self.busqueda = tk.Entry(self.frame_central, justify="center")
        self.busqueda.insert(0, placeholder)
        self.busqueda.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=5)

        self.busqueda.bind("<FocusIn>", lambda e: self.busqueda.delete(0, tk.END) if self.busqueda.get() == placeholder else None)
        self.busqueda.bind("<Return>", lambda e: funcion_buscar())
        # Si la barra queda vacía, se vuelve a mostrar la lista completa
        self.busqueda.bind("<KeyRelease>", lambda e: funcion_buscar() if not self.busqueda.get().strip() else None)
        
    def crear_boton_ordenar(self, funcion_ordenar):
        self.btn_ordenar = tk.Button(self.frame_central, text="Ordenar", command=funcion_ordenar)
        self.btn_ordenar.grid(row=1, column=0, sticky="w", pady=(0, 15), ipadx=10)
        
    def crear_boton_filtrar(self, funcion_filtrar):
        self.btn_filtros = tk.Button(self.frame_central, text="Filtros", command=funcion_filtrar)
        self.btn_filtros.grid(row=1, column=1, sticky="e", pady=(0, 15), ipadx=10)
    
    def crear_boton_crear(self, texto, funcion_crear):
        self.btn_crear = tk.Button(
            self.frame_inferior,
            text=texto,
            fg="green",
            command=funcion_crear,
        )
        self.btn_crear.grid(row=0, column=0, sticky="ew", padx=(10,10), pady=(10, 0), ipady=6)
        
    def crear_boton_volver(self, funcion_volver):
        self.btn_volver = tk.Button(
            self.frame_inferior, 
            text="Volver atras", 
            command=funcion_volver
        )
        self.btn_volver.grid(row=0, column=1, sticky="ew", padx=(10,10), pady=(10, 0), ipady=6)
        
    def crear_treeview(self, frame_parent, columnas, modo=None):
        
        
        self.frame_tabla = tk.Frame(frame_parent)
        self.frame_tabla.grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=10
        )

        self.frame_central.rowconfigure(2, weight=1)
        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=tuple(columnas.keys()),
            show="headings",
            selectmode="browse"
        )
        
        for clave, valor in (columnas.items()):
            self.tabla.heading(clave, text=clave.title())
            self.tabla.column(
                clave,
                width=valor,
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def mensaje_advertencia(self, titulo, mensaje):
        messagebox.showwarning(
                titulo,
                mensaje
            )
        
    def mensaje_confirmacion(self, titulo, mensaje):
         return messagebox.askyesno(
            titulo,
            mensaje
        )
         
    def mensaje_info(self, titulo, mensaje):
        messagebox.showinfo(
                titulo,
                mensaje
                    )
    def actualizar_tabla(self, filas):
        """Limpia self.tabla y la rellena. Acepta filas como diccionarios o tuplas."""
        columnas = self.tabla["columns"]
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for fila in filas:
            if isinstance(fila, dict):
                valores = tuple(fila[c] for c in columnas)
            else:
                valores = tuple(fila)
            self.tabla.insert("", "end", values=valores)

    def buscar_por_columnas(self, datos, campos):
        """Muestra solo las filas de `datos` donde el texto aparece en alguno de `campos`.
        `campos` son claves (si las filas son diccionarios) o índices (si son tuplas)."""
        texto = self.busqueda.get().strip().lower()
        if not texto or texto == self.placeholder_busqueda.lower():
            self.actualizar_tabla(datos)
            return

        resultados = [
            fila for fila in datos
            if any(
                texto in str(fila[campo] if fila[campo] is not None else "").lower()
                for campo in campos
            )
        ]
        self.actualizar_tabla(resultados)

    def ordenar_por(self, datos, campo):
        """Muestra `datos` ordenados por `campo` (clave o índice)."""
        self.actualizar_tabla(sorted(datos, key=lambda f: str(f[campo]).lower()))

    def limpiar_busqueda(self, datos):
        """Vacía la barra de búsqueda y muestra todos los datos."""
        self.busqueda.delete(0, tk.END)
        self.actualizar_tabla(datos)