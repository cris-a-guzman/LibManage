import tkinter as tk
from tkinter import messagebox
from views.components.base_frame import BaseFrame
from datetime import date, datetime

class RegistrarSocio(BaseFrame):
    def __init__(self, parent, controller, conexion, socio_datos=None):
        super().__init__(parent, controller, conexion)
        self.controller = controller
        self.socio_datos = socio_datos or {}
        self.conexion = conexion
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        #! print(socio_datos) Esto va en una nueva pantalla modificar_socio

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
        self.txt_nombre = self.crear_campo("Nombre", 0)
        self.txt_apellido = self.crear_campo("Apellido", 1)
        self.txt_dni = self.crear_campo("DNI", 2)
        self.txt_telefono = self.crear_campo("Telefono", 3)
        self.txt_fecha_asociacion = self.crear_campo("Fecha de Asociacion", 4)

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
            self.set_entry(self.txt_nombre, self.socio_datos.get("nombre", ""))
            self.set_entry(self.txt_dni, self.socio_datos.get("dni", ""))
            self.set_entry(self.txt_telefono, self.socio_datos.get("telefono", ""))
            self.set_entry(self.txt_fecha_asociacion, self.socio_datos.get("fecha_asociacion", ""))
            

    def set_entry(self, entry, valor):
        if valor:
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def guardar_cambios(self):
        from views.socio_views.gestion_socios_view import GestionSocios
        placeholders = ["Nombre", "Apellido", "DNI", "Telefono", "Fecha de Asociacion"]
        
        datos_socio = {
            "nombre": self.txt_nombre.get().strip(),
            "apellido": self.txt_apellido.get().strip(),
            "telefono": self.txt_telefono.get().strip(),
            "dni":self.txt_dni.get().strip(),
            "fecha_asociacion":self.txt_fecha_asociacion.get().strip()
        }
        for i in datos_socio.values():
            if i in placeholders:
                messagebox.showwarning(
                                "Datos incompletos",
                                "Los datos del socio son obligatorios, intentelo de nuevo."
                            )
                return

        if not datos_socio['dni'].isdigit():
            messagebox.showwarning(
                "D.N.I invalido",
                "El DNI ingresado no corresponde a un DNI valido, intentelo de nuevo"
            )
            return
        
        if not datos_socio['telefono'].isdigit():
            messagebox.showwarning(
                    "Telefono invalido",
                    "El telefono ingresado no corresponde a un telefono valido, intentelo de nuevo agregando solo los numeros (el sistema no acepta caracteres no numericos)"
                )
            return
        
        try:
            fecha_asociacion = datetime.strptime(
                self.txt_fecha_asociacion.get().strip(),
                "%d/%m/%Y"
            ).date()

            datos_socio['fecha_asociacion'] = fecha_asociacion

        except ValueError:
            messagebox.showwarning(
                "Fecha inválida",
                "Ocurrio un problema ingresando la fecha del socio, intentelo de nuevo"
            )
            return
        socios_activos = self.ApiSocios.obtener_socios_dni()
        if datos_socio['dni'] in socios_activos:
            messagebox.showwarning(
                    "DNI ya registrado",
                    f"El socio{datos_socio['dni']} ya se encuentra en la base de datos"
                )
            return
        resultado = self.ApiSocios.registrar_socio(datos_socio)
        messagebox.showinfo(title="Socio Registrado", message=f"Socio registrado exitosamente.{resultado}")
        self.controller.show_frame(GestionSocios)

    def descartar(self):
        from views.socio_views.gestion_socios_view import GestionSocios
        messagebox.showinfo(title="Edicion Descartad", message="Edicion Descartada exitosamente.\n Volviendo atras...")
        self.controller.show_frame(GestionSocios)

    def eliminar_socio(self):
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este Socio?"):
            messagebox.showinfo(title="Socio eliminado", message="Socio eliminado exitosamente.")
            
    def ver_prestamos(self):
        from views.socio_views.prestamos_socio_view import VistaPrestamosSocio
        self.controller.show_frame(VistaPrestamosSocio)
            