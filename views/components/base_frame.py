import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

from repositories.libro_repo import LibroRepo
from repositories.prestamo_repo import PrestamoRepo
from repositories.socio_repo import SociosRepo
from views.components.estilo import TITULO

class BaseFrame(tb.Frame):
    
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
        self.frame_inferior = tb.Frame(self)
        self.frame_inferior.grid(
            row=3, column=0, sticky="ew", padx=12, pady=(8, 4)
        )
        self.frame_inferior.columnconfigure(0, weight=1)
        self.frame_inferior.columnconfigure(1, weight=1)
        
    def crear_titulo(self, titulo):
        caja = tb.Frame(self)
        caja.grid(row=0, column=0, sticky="ew", padx=12, pady=(6, 2))
        titulo_label = tb.Label(
            caja, 
            text= titulo, 
            font=TITULO,
            bootstyle=PRIMARY
        )
        titulo_label.pack(anchor="w")
        tb.Separator(caja, bootstyle=PRIMARY).pack(fill="x", pady=(8, 4))
        return titulo_label
        
    def crear_frame_central(self):
        self.frame_central = tb.Frame(self, padding=4)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=12, pady=(4, 8))
        return self.frame_central
    
    def crear_barra_busqueda(self, placeholder , funcion_buscar):

        self.busqueda = tb.Entry(self.frame_central, justify="center", bootstyle="info")
        self.busqueda.insert(0, placeholder)
        self.busqueda.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12), ipady=7)
        
        self.busqueda.bind("<FocusIn>", lambda e: self.busqueda.delete(0, "end") if self.busqueda.get() == placeholder else None)
        self.busqueda.bind("<Return>", lambda e: funcion_buscar())
        #? Agregar funcion para que cuando este vacio se reinicie el renderizado
        
    def crear_boton_ordenar(self, funcion_ordenar):
        self.btn_ordenar = tb.Button(self.frame_central, text="Ordenar", command=funcion_ordenar, bootstyle="info-outline")
        self.btn_ordenar.grid(row=1, column=0, sticky="w", pady=(0, 12), ipadx=12)
        
    def crear_boton_filtrar(self, funcion_filtrar):
        self.btn_filtros = tb.Button(self.frame_central, text="Filtros", command=funcion_filtrar, bootstyle="info-outline")
        self.btn_filtros.grid(row=1, column=1, sticky="e", pady=(0, 12), ipadx=12)
    
    def crear_boton_crear(self, texto, funcion_crear):
        self.btn_crear = tb.Button(
            self.frame_inferior,
            text=texto,
            command=funcion_crear,
            bootstyle=SUCCESS
        )
        self.btn_crear.grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 0), ipady=8)
        
    def crear_boton_volver(self, funcion_volver):
        self.btn_volver = tb.Button(
            self.frame_inferior, 
            text="Volver atras", 
            command=funcion_volver,
            bootstyle="secondary-outline"
        )
        self.btn_volver.grid(row=0, column=1, sticky="ew", padx=8, pady=(8, 0), ipady=8)
        
    def crear_treeview(self, frame_parent, columnas, modo=None):
        
        
        self.frame_tabla = tb.Frame(frame_parent)
        self.frame_tabla.grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=10
        )

        self.frame_central.rowconfigure(2, weight=1)
        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        self.tabla = tb.Treeview(
            self.frame_tabla,
            columns=tuple(columnas.keys()),
            show="headings",
            selectmode="browse",
            bootstyle=INFO
        )
        
        for clave, valor in (columnas.items()):
            self.tabla.heading(clave, text=clave.title())
            self.tabla.column(
                clave,
                width=valor,
                anchor="center"
            )

        scrollbar = tb.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla.yview,
            bootstyle="round"
        )
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def mensaje_advertencia(self, titulo, mensaje):
        Messagebox.show_warning(mensaje, title=titulo)

    def mensaje_confirmacion(self, titulo, mensaje):
        # Retorna "Yes" o "No"
        respuesta = Messagebox.show_question(mensaje, title=titulo)
        return respuesta == "Yes"

    def mensaje_info(self, titulo, mensaje):
        Messagebox.show_info(mensaje, title=titulo)
