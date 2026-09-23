import tkinter as tk
from tkinter import messagebox

class GestionLibros(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.libros_datos = [
            {"id": 1, "titulo": "Don Quijote", "autor": "Cervantes"},
            {"id": 2, "titulo": "Cien años de soledad", "autor": "García Márquez"},
            {"id": 3, "titulo": "El Principito", "autor": "Saint-Exupéry"},
            {"id": 4, "titulo": "Ficciones", "autor": "Borges"},
        ]

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.titulo_label = tk.Label(
            self, 
            text="Gestion de Libros", 
            font=("Arial", 14, "bold"),
            bd=1, 
            relief="solid", 
            pady=8
        )
        self.titulo_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        self.frame_central = tk.Frame(self, bd=1, relief="solid", padx=15, pady=15)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.columnconfigure(1, weight=1)
        self.frame_central.rowconfigure(2, weight=1)

        self.busqueda = tk.Entry(self.frame_central, justify="center")
        self.busqueda.insert(0, "barra de busqueda")
        self.busqueda.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 15), ipady=5)
        
        self.busqueda.bind("<FocusIn>", lambda e: self.busqueda.delete(0, tk.END) if self.busqueda.get() == "barra de busqueda" else None)
        self.busqueda.bind("<Return>", lambda e: self.buscar())

        self.btn_ordenar = tk.Button(self.frame_central, text="Ordenar", command=self.ordenar)
        self.btn_ordenar.grid(row=1, column=0, sticky="w", pady=(0, 15), ipadx=10)

        self.btn_filtros = tk.Button(self.frame_central, text="Filtros", command=self.filtrar)
        self.btn_filtros.grid(row=1, column=1, sticky="e", pady=(0, 15), ipadx=10)


        self.frame_libros = tk.Frame(self.frame_central)
        self.frame_libros.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        self.renderizar_libros(self.libros_datos)

        self.btn_crear = tk.Button(
            self.frame_central, 
            text="Crear Libro", 
            command=self.modificar_libro
        )
        self.btn_atras = tk.Button(
            self.frame_central, 
            text="Volver atras", 
            command=self.volver_atras
        )
        self.btn_crear.grid(row=3, column=0, columnspan=1, sticky="ew", pady=(15, 0), ipady=5)
        self.btn_atras.grid(row=3, column=1, columnspan=1, sticky="ew", pady=(15, 0), ipady=5)

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

            btn_mod = tk.Button(
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