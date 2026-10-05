import tkinter as tk
from tkinter import ttk
from views.components.base_frame import BaseFrame

class GestionPrestamos(BaseFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller      


        # ?--- Frame Central
        self.frame_central = self.crear_frame_central()

        
        #? -- TItulo
        self.crear_titulo("Gestion de Prestamos")
        
        self.frame_central.columnconfigure(0, weight=4)
        self.frame_central.columnconfigure(1, weight=1)
        self.frame_central.rowconfigure(0, weight=0)
        self.frame_central.rowconfigure(1, weight=0) #? Esto tambien se podria refactorizar
        self.frame_central.rowconfigure(2, weight=1)
        self.frame_central.rowconfigure(3, weight=0)

        #? --- Barra de busqueda
        self.crear_barra_busqueda("Buscar Prestamo", self.buscar)

        self.boton = tk.Button(
            self.frame_central, text="Buscar", command=self.buscar
        )
        self.boton.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        #? --- Filtros y Ordenar
        self.botones_filtros_frame = tk.Frame(self.frame_central)
        self.botones_filtros_frame.grid(
            row=1, column=0, columnspan=2, sticky="nsew", pady=5
        )
        self.botones_filtros_frame.columnconfigure(0, weight=1)
        self.botones_filtros_frame.columnconfigure(1, weight=1)

        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #? --- Tabla de Prestamos
        self.frame_tabla = tk.Frame(self.frame_central)
        self.frame_tabla.grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=10
        )
        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        columnas = ("id", "socio", "libro", "vence")
        self.tabla = ttk.Treeview(
            self.frame_tabla, columns=columnas, show="headings"
        )

        self.tabla.heading("id", text="ID")
        self.tabla.heading("socio", text="Socio")
        self.tabla.heading("libro", text="Libro")
        self.tabla.heading("vence", text="Vence")

        self.tabla.column("id", width=40, anchor="center")
        self.tabla.column("socio", width=140)
        self.tabla.column("libro", width=140)
        self.tabla.column("vence", width=80, anchor="center")

        scrollbar = ttk.Scrollbar(
            self.frame_tabla, orient="vertical", command=self.tabla.yview
        )
        self.tabla.configure(yscroll=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # --- Botones de Acción (Inferiores)
        self.frame_acciones = tk.Frame(self.frame_central)
        self.frame_acciones.grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=5
        )
        self.frame_acciones.columnconfigure(0, weight=1)

        self.btn_devolver = tk.Button(
            self.frame_acciones,
            text="devolver",
            command=self.marcar_devuelto,
        )
        self.btn_devolver.pack(side="right", padx=5)

        #? Boton Crear (Registrar prestamo)
        self.crear_boton_crear("Registrar Prestamo", self.registrar_prestamo)
        
        #? Boton Volver Atras
        self.crear_boton_volver(self.volver_atras)
        
        #! Ejemplo de datos
        self.prestamos_datos = [
            (1, "Juan Perez", "1984", "12/09"),
            (2, "Lucia Diaz", "Rayuela", "02/09"),
        ]
        self.actualizar_tabla(self.prestamos_datos)

    def filtrar(self):
        print("Filtrando")

    def actualizar_tabla(self, lista_prestamos):
        """Limpia y vuelve a cargar los datos en la tabla."""
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for prestamo in lista_prestamos:
            self.tabla.insert("", "end", values=prestamo)

    def buscar(self, event=None):
        """Filtra la lista de prestamos según lo ingresado."""
        texto = self.busqueda.get().strip().lower()
        if not texto:
            self.actualizar_tabla(self.prestamos_datos)
            return

        resultados = [
            p for p in self.prestamos_datos
            if texto in p[1].lower() or texto in p[2].lower()
        ]
        self.actualizar_tabla(resultados)

    def limpiar_busqueda(self):
        """Restablece la búsqueda y muestra todos los datos."""
        self.busqueda.delete(0, tk.END)
        self.actualizar_tabla(self.prestamos_datos)

    def ordenar(self):
        """Ordena los prestamos por fecha de vencimiento."""
        prestamos_ordenados = sorted(self.prestamos_datos, key=lambda x: x[3])
        self.actualizar_tabla(prestamos_ordenados)

    def marcar_devuelto(self):
        """Elimina de la lista el prestamo seleccionado (ya devuelto)."""
        seleccion = self.tabla.selection()
        if not seleccion:
            tk.messagebox.showwarning(
                "Atención", "Por favor, selecciona un préstamo de la lista."
            )
            return

        item = self.tabla.item(seleccion)
        prestamo_id = item["values"][0]

        self.prestamos_datos = [
            p for p in self.prestamos_datos if p[0] != prestamo_id
        ]
        self.actualizar_tabla(self.prestamos_datos)

    def registrar_prestamo(self):
        from views.registrar_prestamo_view import RegistrarPrestamo
        self.controller.show_frame(RegistrarPrestamo)
        
    def volver_atras(self): #! Esto lo podriamos pasar a controller me parece
        from views.home_view import HomeView
        self.controller.show_frame(HomeView)