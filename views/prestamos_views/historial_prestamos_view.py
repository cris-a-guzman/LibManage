"""Pantalla de historial de prestamos de un socio en LibManage.

Tiene dos columnas:
    - Izquierda: datos del socio (nombre, DNI, telefono y fecha de asociacion)
      y un boton "Ver prestamos del socio".
    - Derecha: listado de los prestamos del socio, escrito como texto.

Se abre desde la gestion de socios y recibe los datos del socio elegido.
"""

import tkinter as tk
from tkinter import messagebox
from views.components.base_frame import BaseFrame

class HistorialPrestamosSocio(BaseFrame):
    """Pantalla que muestra los datos de un socio y el listado de sus prestamos."""

    def __init__(self, parent, controller, datos):
        """Arma la pantalla: datos del socio a la izquierda y listado de prestamos a la derecha.

        Args:
            parent: Frame contenedor donde se dibuja esta pantalla (el container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar de pantalla.
            datos (dict): Datos del socio elegido. Se usan las claves "nombre", "dni",
                "telefono" y "fecha_asociacion". Llega desde show_frame(frame_class, datos).
        """
        super().__init__(parent, controller)
        self.controller = controller #* Guardamos la ventana principal para poder volver a la gestion de socios
        self.datos_socio = datos #* Datos del socio que recibe la pantalla
        self.datos_prestamos = {} #* Aca van los prestamos del socio (por ahora arranca vacio)

        #? OJO: mas abajo el codigo usa self.socio y self.prestamos, pero aca se guardan como
        #? self.datos_socio y self.datos_prestamos. Si esos nombres no existen en BaseFrame, da AttributeError.
        #! Revisar: unificar los nombres (self.socio / self.datos_socio y self.prestamos / self.datos_prestamos)

        #? Aca se crea un frame central con el metodo de BaseFrame, pero unas lineas mas abajo
        #? self.frame_central se vuelve a crear a mano y pisa a este. Seguramente alcanza con uno solo.
        self.frame_central = self.crear_frame_central()

        self.crear_titulo("Historial de prestamos del socio")

        #? --- Frame Central
        #* Frame principal con borde: adentro van las dos columnas (datos del socio y listado)
        self.frame_central = tk.Frame(self, bd=1, relief="solid", padx=15, pady=15)
        self.frame_central.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        self.frame_central.columnconfigure((0,1), weight=1) #* Dos columnas que se reparten el ancho por igual
        self.frame_central.rowconfigure(4, weight=1) #? La fila 4 se estira al agrandar la ventana

        #? --- Columna izquierda: Datos del socio
        #? Cada dato es un Label con borde (bd=1, relief="solid"). Los f-strings (f"...{valor}")
        #? arman el texto metiendo el valor del diccionario del socio dentro del mensaje.
        #? sticky="ew" estira la etiqueta a lo ancho de la columna.
        self.lbl_nombre = tk.Label(
            self.frame_central,
            text=f"Nombre y Apellido: {self.socio['nombre']}",
            bd=1,
            relief="solid",
            pady=10,
        )
        self.lbl_nombre.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=(0, 10), ipady=5)

        self.lbl_dni = tk.Label(
            self.frame_central,
            text=f"DNI: {self.socio['dni']}",
            bd=1,
            relief="solid",
            pady=10,
        )
        self.lbl_dni.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 10), ipady=5)

        self.lbl_telefono = tk.Label(
            self.frame_central,
            text=f"Telefono: {self.socio['telefono']}",
            bd=1,
            relief="solid",
            pady=10,
        )
        self.lbl_telefono.grid(row=2, column=0, sticky="ew", padx=(0, 10), pady=(0, 10), ipady=5)

        self.lbl_fecha_asociacion = tk.Label(
            self.frame_central,
            text=f"Fecha de Asociacion: {self.socio['fecha_asociacion']}",
            bd=1,
            relief="solid",
            pady=10,
        )
        self.lbl_fecha_asociacion.grid(row=3, column=0, sticky="ew", padx=(0, 10), pady=(0, 10), ipady=5)

        #? sticky="new" pega el boton arriba (n) y lo estira a lo ancho (e, w) de su celda
        self.btn_ver_prestamos = tk.Button(
            self.frame_central,
            text="Ver prestamos del socio",
            command=self.ver_prestamos,
        )
        self.btn_ver_prestamos.grid(row=4, column=0, sticky="new", padx=(0, 10), ipady=8)

        #? --- Columna derecha: Listado de prestamos
        #* Titulo del listado (fila 0, columna 1)
        self.lbl_listado_titulo = tk.Label(
            self.frame_central,
            text="Listado De Prestamos",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_listado_titulo.grid(row=0, column=1, sticky="ew", pady=(0, 10), ipady=3)

        #? rowspan=4: este frame ocupa 4 filas (de la 1 a la 4), asi tiene la misma altura que toda la columna izquierda
        self.frame_listado = tk.Frame(self.frame_central, bd=1, relief="solid")
        self.frame_listado.grid(row=1, column=1, rowspan=4, sticky="nsew")

        #? Un solo Label donde se escribe todo el listado como texto (se completa en renderizar_listado).
        #? justify="left" alinea las lineas a la izquierda y anchor="nw" pega el texto arriba a la izquierda.
        self.lbl_listado = tk.Label(
            self.frame_listado,
            text="",
            justify="left",
            anchor="nw",
            padx=10,
            pady=10,
        )
        self.lbl_listado.pack(fill="both", expand=True) #* pack con fill + expand: el label ocupa todo el frame

        self.renderizar_listado() #* Llena el label con los prestamos

        #? --- Volver Atras
        self.crear_boton_volver(self.volver_atras)

    def renderizar_listado(self):
        """Arma el texto del listado de prestamos del socio.

        Recorre los prestamos y escribe, para cada uno, su numero, estado, fechas y
        dias de retraso, separados por una linea en blanco. Cada prestamo tiene que ser
        un diccionario con las claves "numero", "estado", "fecha_prestamo",
        "fecha_devolucion" y "dias_retraso".
        """
        texto = "" #* Texto final: arranca vacio y se le va sumando cada prestamo
        #? OJO: aca se usa self.prestamos, pero en __init__ se guardo self.datos_prestamos (ver nota de arriba)
        for prestamo in self.prestamos:
            #? "+=" agrega al final del texto. Los strings entre parentesis se pegan uno atras del otro.
            #? "\n" es un salto de linea; "\n\n" deja una linea en blanco entre un prestamo y el siguiente.
            texto += (
                f"Prestamo {prestamo['numero']}:\n"
                f"Estado: {prestamo['estado']}\n"
                f"Dia de prestamo: {prestamo['fecha_prestamo']}\n"
                f"Dia de Devolucion: {prestamo['fecha_devolucion']}\n"
                f"Dias de retraso: {prestamo['dias_retraso']}\n\n"
            )
        #? .strip() saca los saltos de linea sobrantes del final y config(text=...) cambia el texto del Label
        self.lbl_listado.config(text=texto.strip())

    def ver_prestamos(self):
        """Boton "Ver prestamos del socio". Por ahora es un marcador: solo imprime un mensaje en la consola."""
        #! Pendiente: todavia no muestra nada en pantalla
        print(f"Mostrando prestamos completos de {self.socio['nombre']}...")

    def volver_atras(self):
        """Vuelve a la pantalla de gestion de socios (boton "Volver")."""
        #? El import esta aca adentro y no arriba del archivo, seguramente para evitar un
        #? "import circular" (GestionSocios tambien importa a esta pantalla).
        from views.socio_views.gestion_socios_view import GestionSocios
        self.controller.show_frame(GestionSocios)