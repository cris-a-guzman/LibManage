"""Pantalla para registrar o modificar un socio en LibManage.

ESTADO ACTUAL: es una maqueta (prototipo visual). Todavia NO guarda ni elimina
nada en la base de datos: los botones solo muestran mensajes y cambian de pantalla.
Ver los comentarios "#!" para saber que falta.

Se usa en dos modos:
    - Registrar: se abre sin datos (socio_datos=None) y el formulario arranca vacio.
    - Modificar: se abre con un diccionario (socio_datos) y aparece el boton "Ver prestamos del socio".
"""

import tkinter as tk
from tkinter import messagebox


#? OJO: esta clase hereda de tk.Frame y no de BaseFrame como las otras pantallas.
#? Por eso no tiene acceso a self.ApiSocios (la capa de datos) y todavia no puede guardar en la base.
class RegistrarSocio(tk.Frame):
    """Pantalla con el formulario para registrar un socio nuevo o modificar uno existente."""

    def __init__(self, parent, controller, socio_datos=None):
        """Arma la pantalla: titulo, formulario y botones.

        Args:
            parent: Frame contenedor donde se dibuja esta pantalla (el container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar de pantalla.
            socio_datos (dict | None): Datos del socio a modificar. Si es None, la pantalla
                funciona en modo "registrar uno nuevo".
        """
        super().__init__(parent)
        self.controller = controller #* Guardamos la ventana principal para poder navegar a otras pantallas
        self.socio_datos = socio_datos or {} #? Si viene None lo cambiamos por {} asi despues "if self.socio_datos" da False (modo registrar)

        #*-- Distribucion general de la pantalla
        self.rowconfigure(0, weight=0) #* Fila 0 (el titulo): no se estira
        self.rowconfigure(1, weight=1) #* Fila 1 (el formulario): se estira al agrandar la ventana
        self.columnconfigure(0, weight=1)

        #* Titulo de la pantalla (armado a mano con un Label)
        self.titulo_label = tk.Label(
            self,
            text="Registrar Socios",
            font=("Arial", 14, "bold"),
            bd=1,
            pady=8
        )
        self.titulo_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        #? --- Frame Central
        #* Frame principal con borde (armado a mano, a diferencia de las pantallas que usan BaseFrame)
        self.frame_central = tk.Frame(self, bd=1, relief="solid", padx=20, pady=20)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.rowconfigure(0, weight=1)

        #? Contenedor de cajas de texto
        #? Sin "sticky" el frame queda centrado dentro de su celda
        self.frame_formulario = tk.Frame(self.frame_central)
        self.frame_formulario.grid(row=0, column=0)

        #?Textos
        #! Los nombres de estas variables (txt_titulo, txt_autor, txt_anio, txt_cantidad) quedaron
        #! copiados de la pantalla de libros. En realidad guardan: nombre y apellido, DNI, telefono y fecha de asociacion.
        #? Ojo: en la base de datos nombre y apellido son DOS columnas separadas, y aca hay un solo campo.
        self.txt_titulo = self.crear_campo("Nombre y Apellido", 0)
        self.txt_autor = self.crear_campo("DNI", 1)
        self.txt_anio = self.crear_campo("Telefono", 2)
        self.txt_cantidad = self.crear_campo("Fecha de Asociacion", 3)

        # Ver prestamos del socio. boton
        #? Este boton solo aparece en modo modificar (cuando hay socio_datos)
        if self.socio_datos:
            self.btn_ver_prestamos = tk.Button(self.frame_formulario,
                text="Ver prestamos del socio", command=self.ver_prestamos
            )
            self.btn_ver_prestamos.grid(row=4, column=0, pady=8, ipady=6)

        #?Se cargan los datos si existen
        self.cargar_datos()

        #*-- Botones de abajo: 3 columnas iguales (Guardar, Cancelar y Eliminar)
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

        #? Este boton se muestra siempre, tambien al registrar un socio nuevo (donde no tiene sentido eliminar)
        self.btn_eliminar = tk.Button(
            self.frame_botones, text="Eliminar Socio", command=self.eliminar_socio
        )
        self.btn_eliminar.grid(row=0, column=2, padx=5, ipady=3, sticky="ew")

    def crear_campo(self, placeholder, fila):
        """Crea un cuadro de texto con "placeholder" (texto de ejemplo que se borra al hacer click).

        Args:
            placeholder (str): Texto de ejemplo que se muestra mientras el campo no se toca.
            fila (int): Fila de la grilla de frame_formulario donde se coloca.

        Returns:
            tk.Entry: El cuadro de texto ya creado y ubicado.
        """
        entry = tk.Entry(self.frame_formulario, justify="center", width=40)
        entry.insert(0, placeholder) #* Arranca mostrando el texto de ejemplo
        entry.grid(row=fila, column=0, pady=8, ipady=6)

        #? Al hacer click (FocusIn): si el texto es el de ejemplo, se borra. El lambda es un "if" en una linea.
        #? "p=placeholder" guarda el valor actual del placeholder dentro del lambda; sin eso, todos
        #? los campos usarian el ultimo placeholder (un problema clasico de los lambda dentro de funciones).
        #? A diferencia de otras pantallas, aca no hay FocusOut: si se deja el campo vacio, el texto de ejemplo no vuelve.
        entry.bind("<FocusIn>", lambda e, p=placeholder: entry.delete(0, tk.END) if entry.get() == p else None)
        return entry

    def cargar_datos(self):
        """Rellena el formulario con los datos del socio (solo en modo modificar)."""
        #! Pendiente: las claves que se leen ("titulo", "autor", "anio", "cantidad") son las de un LIBRO.
        #! Un socio trae otras claves (id_socio, dni, nombre, apellido, telefono, fecha_asociacion),
        #! asi que con datos reales de un socio el formulario no se llenaria.
        if self.socio_datos:
            self.set_entry(self.txt_titulo, self.socio_datos.get("titulo", ""))
            self.set_entry(self.txt_autor, self.socio_datos.get("autor", ""))
            self.set_entry(self.txt_anio, self.socio_datos.get("anio", ""))
            self.set_entry(self.txt_cantidad, self.socio_datos.get("cantidad", ""))

    def set_entry(self, entry, valor):
        """Reemplaza el texto de un cuadro de texto, solo si el valor nuevo no esta vacio.

        Args:
            entry (tk.Entry): Cuadro de texto a modificar.
            valor: Valor a escribir.
        """
        if valor: #? Si el valor viene vacio no tocamos el campo (asi no se pierde el texto de ejemplo)
            entry.delete(0, tk.END) #* Borra el contenido actual (de la posicion 0 hasta el final)
            entry.insert(0, valor) #* Escribe el valor nuevo

    def guardar_cambios(self):
        """Boton "Guardar Cambios". Por ahora solo muestra un mensaje y vuelve al listado de socios."""
        #! Pendiente: no valida los campos ni guarda nada en la base.
        #! Ademas el mensaje dice "Libro guardado" (copiado de la pantalla de libros): deberia decir "Socio".
        #? El import esta aca adentro y no arriba del archivo, seguramente para evitar un
        #? "import circular" (GestionSocios tambien importa a esta pantalla).
        from views.socio_views.gestion_socios_view import GestionSocios
        messagebox.showinfo(title="Libro Guardado", message="Libro guardado exitosamente.")
        self.controller.show_frame(GestionSocios)

    def descartar(self):
        """Boton "Cancelar y volver atras": avisa que se descarto la edicion y vuelve al listado de socios."""
        #? Import dentro de la funcion por el mismo motivo que en guardar_cambios (evitar import circular)
        from views.socio_views.gestion_socios_view import GestionSocios
        messagebox.showinfo(title="Edicion Descartad", message="Edicion Descartada exitosamente.\n Volviendo atras...")
        self.controller.show_frame(GestionSocios)

    def eliminar_socio(self):
        """Boton "Eliminar Socio": pide confirmacion y muestra un mensaje de exito."""
        #! Pendiente: no elimina nada ni vuelve al listado. Ademas, la app no tiene permiso de DELETE en la
        #! base (rol_libmanage_app), asi que lo correcto seria la baja logica: cargar la fecha_baja del socio.
        #? askyesno muestra una ventana con "Si" y "No", y devuelve True si el usuario elige "Si"
        if messagebox.askyesno("Confirmar", "¿Deseas eliminar este Socio?"):
            messagebox.showinfo(title="Socio eliminado", message="Socio eliminado exitosamente.")

    def ver_prestamos(self):
        """Boton "Ver prestamos del socio": abre la pantalla con el historial de prestamos."""
        #! Ojo: VistaPrestamosSocio necesita el id del socio (id_socio) y aca no se le pasa ninguno,
        #! por lo que al apretar el boton daria un error (falta un argumento).
        #? Import dentro de la funcion por el mismo motivo que en guardar_cambios (evitar import circular)
        from views.socio_views.prestamos_socio_view import VistaPrestamosSocio
        self.controller.show_frame(VistaPrestamosSocio)