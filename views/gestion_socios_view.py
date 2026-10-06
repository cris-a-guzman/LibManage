import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame

class GestionSocios(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        #! Datos de ejemplo para los socios
        self.socios = self.API.traer_socios()

        #? Frame Central
        self.frame_central.columnconfigure(0, weight=1) #? Esto tambien se podria refactorizar
        self.frame_central.columnconfigure(1, weight=1)
        
        #? Titulo
        self.crear_titulo("Gestion de Socios")
        

        #? Barra de busqueda
        self.crear_barra_busqueda("Buscar Socio", self.buscar)
        
        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #? Frame de tabla 
        self.frame_tabla = tk.Frame(self.frame_central)
        self.frame_tabla.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="nsew",
            pady=10
        )
        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        columnas = ("id_socio", "dni", "nombre", "apellido")
        self.tabla = ttk.Treeview(
            self.frame_tabla, columns=columnas, show="headings"
        )

        self.tabla.heading("id_socio", text="ID")
        self.tabla.heading("dni", text="DNI")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("apellido", text="Apellido")

        self.tabla.column("id_socio", width=40, anchor="center")
        self.tabla.column("dni", width=80)
        self.tabla.column("nombre", width=140)
        self.tabla.column("apellido", width=140, anchor="center")

        scrollbar = ttk.Scrollbar(
            self.frame_tabla, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        #? Ver prestamos
        self.crear_boton_ver("Préstamos / Historial", self.ver_prestamos)

        #? Boton Crear (Agregar socio)
        self.crear_boton_crear("Registrar Socio", self.registrar_socio)
        
        #? Boton Volver
        self.crear_boton_volver(self.volver_atras)
        
        #! Renderizamos los datos de los socios
        self.actualizar_tabla(self.socios)
        
    def crear_boton_ver(self, texto, funcion_ver):
        self.frame_inferior.columnconfigure(2, weight=1)
        self.btn_crear = tk.Button(
            self.frame_inferior,
            text=texto,
            fg="black",
            command=funcion_ver,
        )
        self.btn_crear.grid(row=0, column=2, sticky="ew", padx=(10,10), pady=(10, 0), ipady=6)

    def filtrar(self):
        print("Filtrando")

    def actualizar_tabla(self, lista_socios):
        """Limpia y vuelve a cargar los datos en la tabla."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for socio in lista_socios:
            self.tabla.insert(
                "",
                "end",
                values=(
                    socio["id_socio"],
                    socio["dni"],
                    socio["nombre"],
                    socio["apellido"]
                )
            )


    def buscar(self, event=None):
        """Filtra los socios según lo ingresado."""
        texto = self.busqueda.get().strip().lower()

        if not texto:
            self.actualizar_tabla(self.socios)
            return

        resultados = [
            socio for socio in self.socios
            if texto in str(socio["dni"]).lower()
            or texto in socio["nombre"].lower()
            or texto in socio["apellido"].lower()
        ]

        self.actualizar_tabla(resultados)


    def limpiar_busqueda(self):
        """Restablece la búsqueda y muestra todos los socios."""
        self.busqueda.delete(0, tk.END)
        self.actualizar_tabla(self.socios)


    def ordenar(self):
        """Ordena los socios por apellido."""
        socios_ordenados = sorted(
            self.socios,
            key=lambda socio: socio["apellido"].lower()
        )

        self.actualizar_tabla(socios_ordenados)

    def registrar_socio(self, socio=None):
        from views.registrar_socio_view import RegistrarSocio
        self.controller.show_frame(RegistrarSocio, socio)
        # Una vez con la conexion a la db debemos resolver lo de pasar Socio
        
    def volver_atras(self): #! Esto lo podriamos pasar a controller me parece
        from views.home_view import HomeView
        self.controller.show_frame(HomeView)
    
    def ver_prestamos(self, datos=None):
        seleccionado = self.tabla.selection()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un socio")
            return

        item = self.tabla.item(seleccionado[0])
        id_socio = item["values"][0]

        from views.prestamos_socio_view import VistaPrestamosSocio
        self.controller.show_frame(
            VistaPrestamosSocio,
            id_socio
        )