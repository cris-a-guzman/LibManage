import tkinter as tk
from tkinter import messagebox


class RegistrarSocio(tk.Frame):
    def __init__(self, parent, controller, socio_datos=None):
        super().__init__(parent)
        self.controller = controller
        self.socio_datos = socio_datos or {}

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.titulo_label = tk.Label(
            self, 
            text="Registrar Socios", 
            font=("Arial", 14, "bold"),
            bd=1,
            pady=8
        )
        self.titulo_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        #? --- Frame Central
        self.frame_central = tk.Frame(self, bd=1, relief="solid", padx=20, pady=20)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.rowconfigure(0, weight=1)

        #? Contenedor de cajas de texto
        self.frame_formulario = tk.Frame(self.frame_central)
        self.frame_formulario.grid(row=0, column=0)

        #?Textos
        self.txt_titulo = self.crear_campo("Nombre y Apellido", 0)
        self.txt_autor = self.crear_campo("DNI", 1)
        self.txt_anio = self.crear_campo("Telefono", 2)
        self.txt_cantidad = self.crear_campo("Fecha de Asociacion", 3)

        # Ver prestamos del socio. boton
        if self.socio_datos:
            self.btn_ver_prestamos = tk.Button(self.frame_formulario,
                text="Ver prestamos del socio", command=self.ver_prestamos
            )
            self.btn_ver_prestamos.grid(row=4, column=0, pady=8, ipady=6)

        #?Se cargan los datos si existen
        self.cargar_datos()

        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        
        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.columnconfigure(1, weight=1)
        self.frame_botones.columnconfigure(2, weight=1)

        self.btn_guardar = tk.Button(
            self.frame_botones, text="Guardar Cambios", command=self.guardar_cambios
        )
        self.btn_guardar.grid(row=0, column=0, padx=5, ipady=3, sticky="ew")

        self.btn_cancelar = tk.Button(
            self.frame_botones, text="Cancelar y volver atras", command=self.descartar
        )
        self.btn_cancelar.grid(row=0, column=1, padx=5, ipady=3, sticky="ew")

        self.btn_eliminar = tk.Button(
            self.frame_botones, text="Eliminar Socio", command=self.eliminar_socio
        )
        self.btn_eliminar.grid(row=0, column=2, padx=5, ipady=3, sticky="ew")

    def crear_campo(self, placeholder, fila):
        entry = tk.Entry(self.frame_formulario, justify="center", width=40)
        entry.insert(0, placeholder)
        entry.grid(row=fila, column=0, pady=8, ipady=6)
        
        entry.bind("<FocusIn>", lambda e, p=placeholder: entry.delete(0, tk.END) if entry.get() == p else None)
        return entry

    def cargar_datos(self):
        if self.socio_datos:
            self.set_entry(self.txt_titulo, self.socio_datos.get("titulo", ""))
            self.set_entry(self.txt_autor, self.socio_datos.get("autor", ""))
            self.set_entry(self.txt_anio, self.socio_datos.get("anio", ""))
            self.set_entry(self.txt_cantidad, self.socio_datos.get("cantidad", ""))

    def set_entry(self, entry, valor):
        if valor:
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def guardar_cambios(self):
        from views.gestion_socios_view import GestionSocios
        messagebox.showinfo(title="Libro Guardado", message="Libro guardado exitosamente.")
        self.controller.show_frame(GestionSocios)

    def descartar(self):
        from views.gestion_socios_view import GestionSocios
        messagebox.showinfo(title="Edicion Descartad", message="Edicion Descartada exitosamente.\n Volviendo atras...")
        self.controller.show_frame(GestionSocios)

    def eliminar_socio(self):
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este Socio?"):
            messagebox.showinfo(title="Socio eliminado", message="Socio eliminado exitosamente.")
            
    def ver_prestamos(self):
        from views.prestamos_socio_view import VistaPrestamosSocio
        self.controller.show_frame(VistaPrestamosSocio)
            