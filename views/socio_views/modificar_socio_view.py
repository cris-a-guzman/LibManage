import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from views.components.base_frame import BaseFrame
from datetime import date, datetime
from views.components.estilo import TITULO

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

        self.titulo_label = tb.Label(
            self, 
            text="Modificar Socio", 
            font=TITULO,
            bootstyle=PRIMARY,
            padding=8
        )
        self.titulo_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        #? --- Frame Central
        self.frame_central = tb.Labelframe(self, text="Datos del socio", padding=24, bootstyle=PRIMARY)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))
        
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.rowconfigure(0, weight=1)

        #? Contenedor de cajas de texto
        self.frame_formulario = tb.Frame(self.frame_central)
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
        self.txt_fecha_asociacion = self.crear_campo(resultado['fecha_asociacion'], 4)      

        self.frame_botones = tb.Frame(self.frame_central)
        self.frame_botones.grid(row=1, column=0, sticky="ew", pady=(15, 0))
        
        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.columnconfigure(1, weight=1)
        self.frame_botones.columnconfigure(2, weight=1)

        self.btn_guardar = tb.Button(
            self.frame_botones, text="Guardar Cambios", command=self.guardar_cambios, bootstyle=SUCCESS
        )
        self.btn_guardar.grid(row=0, column=0, padx=6, ipady=8, sticky="ew")

        self.btn_cancelar = tb.Button(
            self.frame_botones, text="Cancelar y volver atras", command=self.descartar, bootstyle="secondary-outline"
        )
        self.btn_cancelar.grid(row=0, column=1, padx=6, ipady=8, sticky="ew")

        self.btn_eliminar = tb.Button(
            self.frame_botones, text="Eliminar Socio", command=self.eliminar_socio, bootstyle="danger-outline"
        )
        self.btn_eliminar.grid(row=0, column=2, padx=6, ipady=8, sticky="ew")


    def crear_etiqueta(self, titulo, fila):
        label = tb.Label(self.frame_formulario, text=titulo, justify="center", width=40, bootstyle=PRIMARY)
        label.grid(row=fila, column=0, pady=4, ipady=6)
        return label
    
    def crear_campo(self, placeholder, fila):
        entry = tb.Entry(self.frame_formulario, justify="center", width=40, bootstyle=PRIMARY)
        entry.insert(0, placeholder)
        entry.grid(row=fila, column=1, pady=8, ipady=6)
        
        entry.bind("<FocusIn>", lambda e, p=placeholder: entry.delete(0, "end") if entry.get() == p else None)
        return entry

    def cargar_datos(self, id_socio):
        resultado = self.ApiSocios.obtener_socio_por_id(id_socio)
        print(resultado)
        return resultado

    def set_entry(self, entry, valor):
        if valor:
            entry.delete(0, "end")
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
                Messagebox.show_warning(
                                "Los datos del socio son obligatorios, intentelo de nuevo.",
                                title="Datos incompletos"
                            )
                return

        if not datos_socio['dni'].isdigit():
            Messagebox.show_warning(
                "El DNI ingresado no corresponde a un DNI valido, intentelo de nuevo",
                title="D.N.I invalido"
            )
            return
        
        if not datos_socio['telefono'].isdigit():
            Messagebox.show_warning(
                    "El telefono ingresado no corresponde a un telefono valido, intentelo de nuevo agregando solo los numeros (el sistema no acepta caracteres no numericos)",
                    title="Telefono invalido"
                )
            return
        
        try:
            fecha_asociacion = datetime.strptime(
                self.txt_fecha_asociacion.get().strip(),
                "%d/%m/%Y"
            ).date()

            datos_socio['fecha_asociacion'] = fecha_asociacion

        except ValueError:
            Messagebox.show_warning(
                "Ocurrio un problema ingresando la fecha del socio, intentelo de nuevo",
                title="Fecha inválida"
            )
            return
        socios_activos = self.ApiSocios.obtener_socios_dni()
        if datos_socio['dni'] in socios_activos:
            Messagebox.show_warning(
                    f"El socio{datos_socio['dni']} ya se encuentra en la base de datos",
                    title="DNI ya registrado"
                )
            return
        resultado = self.ApiSocios.registrar_socio(datos_socio)
        Messagebox.show_info(title="Socio Registrado", message=f"Socio registrado exitosamente.{resultado}")
        self.controller.show_frame(GestionSocios)

    def descartar(self):
        from views.socio_views.gestion_socios_view import GestionSocios
        Messagebox.show_info(title="Edicion Descartad", message="Edicion Descartada exitosamente.\n Volviendo atras...")
        self.controller.show_frame(GestionSocios)

    def eliminar_socio(self):
        from views.socio_views.gestion_socios_view import GestionSocios
        if self.ApiSocios.tiene_prestamos_activos(self.socio_id):
            Messagebox.show_warning(
                "No podés dar de baja a este socio porque tiene préstamos activos sin devolver.",
                title="Acción denegada"
            )
            return
        if Messagebox.show_question("¿Deseas eliminar este Socio?", title="Confirmar") == "Yes":
            if self.ApiSocios.baja_socio(self.socio_id):
                Messagebox.show_info(title="Socio eliminado", message="Socio eliminado exitosamente.")
                self.controller.show_frame(GestionSocios)
            else:
                Messagebox.show_info(title="Error Inesperado", message="Ocurrio un error inesperado")
                return
            
    def ver_prestamos(self):
        from views.socio_views.prestamos_socio_view import VistaPrestamosSocio
        self.controller.show_frame(VistaPrestamosSocio)
            
