import tkinter as tk

class BaseFrame(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        #? Configuración del grid principal de la pantalla
        
        self.rowconfigure(0, weight=0) # Título
        self.rowconfigure(1, weight=1) # Contenido principal
        self.columnconfigure(0, weight=1) # Botones para volver
        
    def crear_titulo(self, titulo):
        titulo_label = tk.Label(
            self, 
            text= titulo, 
            font=("Arial", 14, "bold"),
            bd=1,
            pady=8
        )
        titulo_label.grid(row=0, column=0, sticky="new", padx=10, pady=(10, 5))
        
        self.frame_central.columnconfigure(0, weight=4)
        self.frame_central.rowconfigure(0, weight=0)
        
    def crear_frame_central(self):
        self.frame_central = tk.Frame(self, bd=1, relief="solid")
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        return self.frame_central
    
    def crear_barra_busqueda(self, placeholder , funcion_buscar):

        self.busqueda = tk.Entry(self.frame_central, justify="center")
        self.busqueda.insert(0, placeholder)
        self.busqueda.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=5)
        
        self.busqueda.bind("<FocusIn>", lambda e: self.busqueda.delete(0, tk.END) if self.busqueda.get() == placeholder else None)
        self.busqueda.bind("<Return>", lambda e: funcion_buscar())
        #? Agregar funcion para que cuando este vacio se reinicie el renderizado
        
    def crear_boton_ordenar(self, funcion_ordenar):
        self.btn_ordenar = tk.Button(self.frame_central, text="Ordenar", command=funcion_ordenar)
        self.btn_ordenar.grid(row=1, column=0, sticky="w", pady=(0, 15), ipadx=10)
        
    def crear_boton_filtrar(self, funcion_filtrar):
        self.btn_filtros = tk.Button(self.frame_central, text="Filtros", command=funcion_filtrar)
        self.btn_filtros.grid(row=1, column=1, sticky="e", pady=(0, 15), ipadx=10)
    
    def crear_boton_crear(self, texto, funcion_crear):
        self.btn_crear = tk.Button(
            self.frame_central,
            text=texto,
            fg="red",
            command=funcion_crear,
        )
        self.btn_crear.grid(row=4, column=0, columnspan=1, sticky="ew", pady=(10, 0), ipady=6)
        
    def crear_boton_volver(self, funcion_volver):
        self.btn_volver = tk.Button(
            self.frame_central, 
            text="Volver atras", 
            command=self.volver_atras
        )
        self.btn_volver.grid(row=4, column=1, columnspan=1, sticky="ew", pady=(15, 0), ipady=5)