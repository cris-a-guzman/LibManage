import tkinter as tk
from tkinter import ttk, messagebox

class GestionSocios(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        #! Datos de ejemplo para los socios
        self.socios = [
            {"id": 1, "nombre": "Socio 1"},
            {"id": 2, "nombre": "Socio 2"},
            {"id": 3, "nombre": "Socio 3"},
            {"id": 4, "nombre": "Socio 4"},
        ]

        # Configuración del grid principal de la pantalla
        self.rowconfigure(0, weight=0) # Título
        self.rowconfigure(1, weight=1) # Contenido principal
        self.columnconfigure(0, weight=1)

        #?
        self.titulo_label = tk.Label(
            self, 
            text="Gestion Socios", 
            font=("Arial", 14, "bold"),
            bd=1,
            pady=8
        )
        self.titulo_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        #Framce Central
        self.frame_central = tk.Frame(self, bd=1, relief="solid")
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.columnconfigure(1, weight=1)

        #Barra de busqueda
        self.busqueda = tk.Entry(self.frame_central, justify="center")
        self.busqueda.insert(0, "Barra de Busqueda")
        self.busqueda.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=5)
        
        self.busqueda.bind("<FocusIn>", lambda e: self.busqueda.delete(0, tk.END) if self.busqueda.get() == "Barra de Busqueda" else None)

        #Botones
        self.btn_ordenar = tk.Button(self.frame_central, text="Ordenar", command=self.ordenar)
        self.btn_ordenar.grid(row=1, column=0, sticky="w", pady=(0, 15), ipadx=10)

        self.btn_filtros = tk.Button(self.frame_central, text="Filtros", command=self.filtrar)
        self.btn_filtros.grid(row=1, column=1, sticky="e", pady=(0, 15), ipadx=10)

        #Socios
        self.frame_socios = tk.Frame(self.frame_central)
        self.frame_socios.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        self.renderizar_socios()

        # Agregar Socios
        self.btn_agregar = tk.Button(
            self.frame_central, 
            text="Agregar Socio", 
            command=self.agregar_socio
        )
        
        self.btn_volver_atras = tk.Button(
            self.frame_central, 
            text="Volver Atras", 
            command=self.volver_atras
        )
        self.btn_agregar.grid(row=3, column=0, columnspan=1, sticky="ew", pady=(15, 0), ipady=5)
        self.btn_volver_atras.grid(row=3, column=1, columnspan=1, sticky="ew", pady=(15, 0), ipady=5)

    def renderizar_socios(self):
        # Limpiar widgets previos
        for widget in self.frame_socios.winfo_children():
            widget.destroy()

        for idx, socio in enumerate(self.socios):
            col = idx % 4  # Distribuye hasta 4 elementos por fila
            self.frame_socios.columnconfigure(col, weight=1)


            sub_frame = tk.Frame(self.frame_socios)
            sub_frame.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")


            lbl_socio = tk.Label(
                sub_frame, 
                text=socio["nombre"], 
                bd=1, 
                relief="solid", 
                height=3
            )
            lbl_socio.pack(fill="x", pady=(0, 5))


            btn_mod = tk.Button(
                sub_frame, 
                text="Modificar", 
                command=lambda s=socio: self.agregar_socio(s)
            )
            brn_prestamos = tk.Button(
                sub_frame, 
                text="Ver Prestamos", 
                command=lambda s=socio: self.ver_prestamos(s)
            )
            btn_mod.pack(fill="x")
            brn_prestamos.pack(fill="x")

    def ordenar(self):
        print("Ordenando socios...")

    def filtrar(self):
        print("Filtrando socios...")


    def agregar_socio(self, socio=None):
        from views.registrar_socio_view import RegistrarSocio
        self.controller.show_frame(RegistrarSocio, socio)
        # Una vez con la conexion a la db debemos resolver lo de pasar Socio
        
    def volver_atras(self):
        from views.home_view import HomeView
        self.controller.show_frame(HomeView)
    
    def ver_prestamos(self, datos):
        from views.prestamos_socio_view import VistaPrestamosSocio
        self.controller.show_frame(VistaPrestamosSocio, datos)