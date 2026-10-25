import tkinter as tk
from tkinter import messagebox
from views.components.base_frame import BaseFrame
from views.components.formulario_desplazable import FormularioDesplazable


class ModificarLibro(BaseFrame):
    def __init__(self, parent, controller, conexion, libro_datos=None):
        super().__init__(parent, controller, conexion)
        self.controller = controller
        self.libro_datos = libro_datos or {}

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        if libro_datos is not None:
            self.titulo = self.crear_titulo(f"Modificar Libro: {self.libro_datos.get('titulo', '')}")
        else:
            self.titulo_label = self.crear_titulo("Crear Libro")
            
        #? --- Frame Central
        self.scroll_formulario = FormularioDesplazable(
            self.frame_central
        )
        self.scroll_formulario.pack(fill="both", expand=True)

        self.frame_central = tk.Frame(self.scroll_formulario.contenido, bd=1, relief="solid", padx=20, pady=20)
        self.frame_central.pack(fill="both", expand=True)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.rowconfigure(0, weight=1)

        #? Contenedor de cajas de texto
        self.frame_formulario = tk.Frame(self.frame_central)
        self.frame_formulario.grid(row=0, column=0)

        #?Textos
        self.lbl_titulo = self.crear_etiqueta("Titulo", 0)
        self.txt_titulo = self.crear_campo("Titulo del Libro", 1)
        self.lbl_autor = self.crear_etiqueta("Autor", 2)
        self.txt_autor = self.crear_campo("Autor", 3)
        self.lbl_anio = self.crear_etiqueta("Año", 4)
        self.txt_anio = self.crear_campo("Año", 5)
        self.lbl_cantidad = self.crear_etiqueta("Cantidad Total", 6)
        self.txt_cantidad = self.crear_campo("Cantidad total", 7)

        #?Se cargan los datos si existen
        self.cargar_datos()

        #? Frame Botones
        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        
        self.frame_botones.columnconfigure((0,1,2), weight=1)

        #? Botones
        self.btn_guardar = tk.Button(
            self.frame_botones, text="Guardar Cambios", command=self.guardar_cambios
        )
        self.btn_guardar.grid(row=0, column=0, padx=5, ipady=3, sticky="ew")

        self.btn_cancelar = tk.Button(
            self.frame_botones, text="Cancelar y volver atras", command=self.descartar
        )
        self.btn_cancelar.grid(row=0, column=2, padx=5, ipady=3, sticky="ew")

        if self.libro_datos:
            self.btn_eliminar = tk.Button(
                self.frame_botones, text="Dar de baja", command=self.eliminar_libro
            )
            self.btn_eliminar.grid(row=0, column=1, padx=5, ipady=3, sticky="ew")
            
    def crear_etiqueta(self, titulo, fila):
        label = tk.Label(self.frame_formulario, text=titulo, justify="center", width=40)
        label.grid(row=fila, column=0, pady=4, ipady=6)
        return label
        
    def crear_campo(self, placeholder, fila):
        entry = tk.Entry(self.frame_formulario, justify="center", width=40)
        entry.insert(0, placeholder)
        entry.grid(row=fila, column=0, pady=4, ipady=6)
        
        entry.bind("<FocusIn>", lambda e, p=placeholder: entry.delete(0, tk.END) if entry.get() == p else None)
        return entry

    def cargar_datos(self):
        if self.libro_datos:
            self.set_entry(self.txt_titulo, self.libro_datos.get("titulo", ""))
            self.set_entry(self.txt_autor, self.libro_datos.get("autor", ""))
            self.set_entry(self.txt_anio, self.libro_datos.get("anio", ""))
            self.set_entry(self.txt_cantidad, self.libro_datos.get("cantidad_total", ""))
            # self.set_entry(self.txt_isbn), self.libro_datos.get("isbn", "")

    def set_entry(self, entry, valor):
        if valor:
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def guardar_cambios(self):
        # Recuperar los datos del formulario
        titulo = self.txt_titulo.get().strip()
        autor = self.txt_autor.get().strip()
        anio = self.txt_anio.get().strip()
        cantidad = self.txt_cantidad.get().strip()

        # Validar campos obligatorios
        if titulo in ("", "Titulo del Libro") or autor in ("", "Autor"):
            messagebox.showwarning(
                "Datos incompletos",
                "El título y el autor son obligatorios."
            )
            return

        # Validar los valores numéricos
        try:
            anio = None if anio in ("", "Año") else int(anio)
            cantidad = int(cantidad)

            if (anio is not None and anio <= 0) or cantidad < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Datos inválidos",
                "Ingresá un año válido y una cantidad entera no negativa."
            )
            return

        # Guardar en MySQL
        try:
            if self.libro_datos:
                self.ApiLibros.actualizar_libro(
                    self.libro_datos["id_libro"],
                    titulo,
                    autor,
                    anio,
                    cantidad
                )
                mensaje = "Libro modificado correctamente."
            else:
                nuevo_id = self.ApiLibros.crear_libro(titulo, autor, anio, cantidad)
                mensaje = f"Libro creado correctamente con ID {nuevo_id}."

        except Exception as error:
            messagebox.showerror(
                "Error al guardar",
                f"No se pudo guardar el libro: {error}"
            )
            return

        # Confirmar al usuario
        messagebox.showinfo("Operación exitosa", mensaje)

        # Regresar al listado
        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)


    def descartar(self):
        from views.libros_views.gestion_libros_view import GestionLibros
        messagebox.showinfo(title="Libro Descartad", message="Libro Descartado exitosamente.\n Volviendo atras...")
        self.controller.show_frame(GestionLibros)

    
    def eliminar_libro(self):
        if not self.libro_datos:
            return

        confirmar = messagebox.askyesno(
            "Confirmar baja",
            "¿Deseás dar de baja este libro?"
        )

        if not confirmar:
            return

        try:
            resultado = self.ApiLibros.dar_baja_libro(
                self.libro_datos["id_libro"]
            )

            if not resultado:
                messagebox.showwarning(
                    "Atención",
                    "El libro no existe o ya fue dado de baja."
                )
                return

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo dar de baja el libro: {error}"
            )
            return

        messagebox.showinfo(
            "Operación exitosa",
            "El libro fue dado de baja correctamente."
        )

        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)