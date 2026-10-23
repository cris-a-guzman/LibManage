# Base visual compartida por la mayoría de las pantallas.
# También crea la conexión y los repositorios que las vistas usan para leer o escribir.
# Referencias: docs/estudio/README.md#programación-orientada-a-objetos y
# docs/estudio/README.md#tkinter-y-programación-dirigida-por-eventos
import tkinter as tk
from tkinter import ttk, messagebox
from repositories.conexion import obtener_conexion
from repositories.libro_repo import LibroRepo
from repositories.prestamo_repo import PrestamoRepo
from repositories.socio_repo import SociosRepo

# Superclase de pantalla: reúne estructura, navegación indirecta y controles repetidos.
class BaseFrame(tk.Frame):
    
    # Recibe el contenedor padre y el controlador que cambia de pantalla.
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.conexion = obtener_conexion()
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
        
    # Crea y devuelve la etiqueta de título en la primera fila.
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
        
    # Crea el contenedor donde cada subclase organiza su contenido específico.
    def crear_frame_central(self):
        self.frame_central = tk.Frame(self, bd=1, relief="solid")
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        return self.frame_central
    
    # Recibe un texto inicial y una función callback que se ejecuta al presionar Enter.
    def crear_barra_busqueda(self, placeholder , funcion_buscar):

        self.busqueda = tk.Entry(self.frame_central, justify="center")
        self.busqueda.insert(0, placeholder)
        self.busqueda.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=5)
        
        self.busqueda.bind("<FocusIn>", lambda e: self.busqueda.delete(0, tk.END) if self.busqueda.get() == placeholder else None)
        self.busqueda.bind("<Return>", lambda e: funcion_buscar())
        #? Agregar funcion para que cuando este vacio se reinicie el renderizado
        
    # Crea un botón y asocia la función recibida sin ejecutarla todavía.
    def crear_boton_ordenar(self, funcion_ordenar):
        self.btn_ordenar = tk.Button(self.frame_central, text="Ordenar", command=funcion_ordenar)
        self.btn_ordenar.grid(row=1, column=0, sticky="w", pady=(0, 15), ipadx=10)
        
    # Crea el botón reutilizable de filtros.
    def crear_boton_filtrar(self, funcion_filtrar):
        self.btn_filtros = tk.Button(self.frame_central, text="Filtros", command=funcion_filtrar)
        self.btn_filtros.grid(row=1, column=1, sticky="e", pady=(0, 15), ipadx=10)
    
    # Crea el botón principal de alta con texto y callback configurables.
    def crear_boton_crear(self, texto, funcion_crear):
        self.btn_crear = tk.Button(
            self.frame_inferior,
            text=texto,
            fg="green",
            command=funcion_crear,
        )
        self.btn_crear.grid(row=0, column=0, sticky="ew", padx=(10,10), pady=(10, 0), ipady=6)
        
    # Crea el botón que delega la navegación de regreso en cada subclase.
    def crear_boton_volver(self, funcion_volver):
        self.btn_volver = tk.Button(
            self.frame_inferior, 
            text="Volver atras", 
            command=funcion_volver
        )
        self.btn_volver.grid(row=0, column=1, sticky="ew", padx=(10,10), pady=(10, 0), ipady=6)
        
    # Construye una tabla visual a partir de nombres y anchos de columnas.
    # El bucle configura cada encabezado y evita repetir esa lógica en las vistas.
    def crear_treeview(self, frame_parent, columnas, ancho, modo=None):
        self.frame_tabla = tk.Frame(frame_parent)
        self.frame_tabla.grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=10
        )

        self.frame_central.rowconfigure(2, weight=1)
        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse"
        )

        for idx, columna in enumerate(columnas):
            self.tabla.heading(columna, text=columna.title())
            self.tabla.column(
                columna,
                width=ancho[idx],
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

    # Muestra un diálogo de advertencia sin devolver datos.
    def mensaje_advertencia(self, titulo, mensaje):
        messagebox.showwarning(
                titulo,
                mensaje
            )
        
    # Devuelve True o False según la decisión de la persona usuaria.
    def mensaje_confirmacion(self, titulo, mensaje):
         return messagebox.askyesno(
            titulo,
            mensaje
        )
         
    # Muestra un diálogo informativo.
    def mensaje_info(self, titulo, mensaje):
        messagebox.showinfo(
                titulo,
                mensaje
                    )