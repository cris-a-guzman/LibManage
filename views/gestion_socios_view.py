import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame

class GestionSocios(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        #! Datos de ejemplo para los socios
        self.socios = [
            {"id": 1, "nombre": "Socio 1"},
            {"id": 2, "nombre": "Socio 2"},
            {"id": 3, "nombre": "Socio 3"},
            {"id": 4, "nombre": "Socio 4"},
        ]

        #? Frame Central
        self.frame_central = self.crear_frame_central()
        self.frame_central.columnconfigure(0, weight=1) #? Esto tambien se podria refactorizar
        self.frame_central.columnconfigure(1, weight=1)
        
        #? Titulo
        self.crear_titulo("Gestion de Socios")
        

        #? Barra de busqueda
        self.crear_barra_busqueda("Buscar Socio", self.buscar_socio)
        
        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #Socios
        self.frame_socios = tk.Frame(self.frame_central)
        self.frame_socios.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        self.renderizar_socios()

        #? Boton Crear (Agregar socio)
        self.crear_boton_crear("Agregar Socio", self.agregar_socio)
        
        #? Boton Volver
        self.crear_boton_volver(self.volver_atras)

    def buscar_socio(self):
        pass
        # Se va a implementar luego
    
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