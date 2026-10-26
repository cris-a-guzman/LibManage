import tkinter as tk
from tkinter import messagebox
from views.components.base_frame import BaseFrame
from datetime import date, datetime
from mysql.connector import Error, IntegrityError

class ModificarSocio(BaseFrame):
    def __init__(self, parent, controller, conexion, socio_datos=None):
        super().__init__(parent, controller, conexion)
        self.controller = controller
        self.socio_id = socio_datos or {}
        self.conexion = conexion
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        print(socio_datos)

        self.titulo_label = tk.Label(
            self, 
            text="Modificar Socio", 
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
        
        #?Se cargan los datos
        resultado = self.cargar_datos(self.socio_id)

        #?Textos
        self.lbl_nombre = self.crear_etiqueta("Nombre",0)
        self.txt_nombre = self.crear_campo(resultado['nombre'], 0)
        self.lbl_apellido = self.crear_etiqueta("Apellido",1)
        self.txt_apellido = self.crear_campo(resultado['apellido'], 1)
        self.lbl_dni = self.crear_etiqueta("DNI",2)
        self.txt_dni = self.crear_campo(resultado['dni'], 2)
        self.lbl_telefono = self.crear_etiqueta("Telefono",3)
        self.txt_telefono = self.crear_campo(resultado['telefono'], 3)
        self.lbl_fecha_asociacion = self.crear_etiqueta("Fecha de asociacion",4)
        fecha = resultado["fecha_asociacion"]

        if isinstance(fecha, (date, datetime)):
            fecha = fecha.strftime("%d/%m/%Y")

        self.txt_fecha_asociacion = self.crear_campo(fecha, 4)
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


    def crear_etiqueta(self, titulo, fila):
        label = tk.Label(self.frame_formulario, text=titulo, justify="center", width=40)
        label.grid(row=fila, column=0, pady=4, ipady=6)
        return label
    
    def crear_campo(self, valor, fila):
        entry = tk.Entry(
            self.frame_formulario,
            justify="center",
            width=40
        )
        entry.insert(0, valor)
        entry.grid(row=fila, column=1, pady=8, ipady=6)
        return entry

    def cargar_datos(self, id_socio):
        resultado = self.ApiSocios.obtener_socio_por_id(id_socio)
        print(resultado)
        return resultado

    def set_entry(self, entry, valor):
        if valor:
            entry.delete(0, tk.END)
            entry.insert(0, valor)

    def guardar_cambios(self):
        from views.socio_views.gestion_socios_view import GestionSocios

        # 1. Obtener los valores del formulario
        datos_socio = {
            "nombre": self.txt_nombre.get().strip(),
            "apellido": self.txt_apellido.get().strip(),
            "telefono": self.txt_telefono.get().strip(),
            "dni": self.txt_dni.get().strip(),
            "fecha_asociacion": self.txt_fecha_asociacion.get().strip()
        }

        # 2. Verificar que no existan campos vacíos
        if any(not valor for valor in datos_socio.values()):
            messagebox.showwarning(
                "Datos incompletos",
                "Todos los campos son obligatorios."
            )
            return

        # 3. Validar DNI
        if not datos_socio["dni"].isdigit():
            messagebox.showwarning(
                "DNI inválido",
                "El DNI debe contener solamente números."
            )
            return

        # 4. Validar teléfono
        if not datos_socio["telefono"].isdigit():
            messagebox.showwarning(
                "Teléfono inválido",
                "El teléfono debe contener solamente números."
            )
            return

        # 5. Validar y convertir la fecha
        try:
            datos_socio["fecha_asociacion"] = datetime.strptime(
                datos_socio["fecha_asociacion"],
                "%d/%m/%Y"
            ).date()

        except ValueError:
            messagebox.showwarning(
                "Fecha inválida",
                "La fecha debe tener el formato DD/MM/AAAA."
            )
            return

        # 6. Validar DNI y actualizar el socio
        try:
            # Verificar que el DNI no pertenezca a otro socio
            if self.ApiSocios.dni_asignado_a_otro(
                datos_socio["dni"],
                self.socio_id
            ):
                messagebox.showwarning(
                    "DNI duplicado",
                    "El DNI ingresado pertenece a otro socio."
                )
                return

            # Actualizar el registro existente
            resultado = self.ApiSocios.modificar_socio(
                self.socio_id,
                datos_socio
            )

            if resultado > 0:
                messagebox.showinfo(
                    "Socio modificado",
                    "Los datos del socio se actualizaron correctamente."
                )
                self.controller.show_frame(GestionSocios)

            else:
                # Un UPDATE sin cambios también devuelve rowcount = 0
                socio = self.ApiSocios.obtener_socio_por_id(
                    self.socio_id
                )

                if socio is None:
                    messagebox.showerror(
                        "Error",
                        "No se encontró el socio que intentás modificar."
                    )
                else:
                    messagebox.showinfo(
                        "Sin cambios",
                        "No se detectaron cambios en los datos del socio."
                    )
                    self.controller.show_frame(GestionSocios)

        # 7. Manejar errores por restricciones de MySQL
        except IntegrityError as error:
            if error.errno == 1062:
                messagebox.showwarning(
                    "DNI duplicado",
                    "El DNI ingresado ya está registrado."
                )
            else:
                messagebox.showerror(
                    "Error de integridad",
                    "No se pudieron guardar los cambios."
                )

        # 8. Manejar otros errores de base de datos
        except Error as error:
            print(f"Error al modificar socio: {error}")
            messagebox.showerror(
                "Error de base de datos",
                "Ocurrió un error al actualizar el socio."
            )

    def descartar(self):
        from views.socio_views.gestion_socios_view import GestionSocios
        messagebox.showinfo(title="Edicion Descartad", message="Edicion Descartada exitosamente.\n Volviendo atras...")
        self.controller.show_frame(GestionSocios)

    def eliminar_socio(self):
        from views.socio_views.gestion_socios_view import GestionSocios
        if self.ApiSocios.tiene_prestamos_activos(self.socio_id):
            messagebox.showwarning(
                "Acción denegada", 
                "No podés dar de baja a este socio porque tiene préstamos activos sin devolver."
            )
            return
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este Socio?"):
            if self.ApiSocios.baja_socio(self.socio_id):
                messagebox.showinfo(title="Socio eliminado", message="Socio eliminado exitosamente.")
                self.controller.show_frame(GestionSocios)
            else:
                messagebox.showinfo(title="Error Inesperado", message="Ocurrio un error inesperado")
                return
            
    def ver_prestamos(self):
        from views.socio_views.prestamos_socio_view import VistaPrestamosSocio
        self.controller.show_frame(VistaPrestamosSocio)
            