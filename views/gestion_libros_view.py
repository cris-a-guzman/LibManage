import tkinter as tk
from tkinter import messagebox
from views.components.base_frame import BaseFrame

class GestionLibros(BaseFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.controller = controller

        self.libros_datos = [
            {"id": 1, "titulo": "Don Quijote", "autor": "Cervantes"},
            {"id": 2, "titulo": "Cien años de soledad", "autor": "García Márquez"},
            {"id": 3, "titulo": "El Principito", "autor": "Saint-Exupéry"},
            {"id": 4, "titulo": "Ficciones", "autor": "Borges"},
        ]
        
        #? Frame principal
        self.frame_central = self.crear_frame_central()
        
        #? Titulo
        self.crear_titulo("Gestion de Libro")
        
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.columnconfigure(1, weight=1) #? Esto tambien se podria refactorizar
        self.frame_central.rowconfigure(2, weight=1)

        #? Barra de busqueda
        self.crear_barra_busqueda("Buscar Libro", self.buscar)

        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #? Frame contenedor de libros
        self.frame_libros = tk.Frame(self.frame_central)
        self.frame_libros.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        self.renderizar_libros(self.libros_datos)
        
        #? Boton Crear Libro
        self.crear_boton_crear("Crear Libro", self.modificar_libro)

        #? Boton Volver Atras
        self.crear_boton_volver(self.volver_atras)

    def renderizar_libros(self, lista_libros):
        for widget in self.frame_libros.winfo_children():
            widget.destroy()

        for idx, libro in enumerate(lista_libros):
            col = idx % 4 #? Lo que hace esto es calcular la columna a la que debe ir mediante el modulo
            self.frame_libros.columnconfigure(col, weight=1)

            sub_frame = tk.Frame(self.frame_libros)
            sub_frame.grid(row=0, column=col, padx=5, pady=5, sticky="nsew")

            lbl_libro = tk.Label(
                sub_frame, 
                text=f"Libro\n{libro['titulo']}", 
                bd=1,
                height=4,
                wraplength=100
            )
            lbl_libro.pack(fill="x", pady=(0, 5))

            btn_mod = tk.Button( #! Boton
                sub_frame, 
                text="Modificar", 
                command=lambda l=libro: self.modificar_libro(l)
            )
            
            btn_mod.pack(fill="x")

    def buscar(self):
        texto = self.busqueda.get().strip().lower()
        if not texto or texto == "barra de busqueda":
            self.renderizar_libros(self.libros_datos)
            return

        resultados = [
            l for l in self.libros_datos if texto in l["titulo"].lower() or texto in l["autor"].lower()
        ]
        self.renderizar_libros(resultados)

    def ordenar(self):
        libros_ordenados = sorted(self.libros_datos, key=lambda x: x["titulo"])
        self.renderizar_libros(libros_ordenados)

    def filtrar(self):
        self.busqueda.delete(0, tk.END)
        self.renderizar_libros(self.libros_datos)

    def modificar_libro(self, libro=None):
        from views.modificar_libro_view import ModificarLibro
        self.controller.show_frame(ModificarLibro)

        
    def volver_atras(self):
        from views.home_view import HomeView
        self.controller.show_frame(HomeView)