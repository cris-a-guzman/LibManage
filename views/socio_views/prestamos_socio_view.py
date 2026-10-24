"""Pantalla con el historial de prestamos de un socio en LibManage.

Muestra:
    - Una ficha con los datos del socio (ID, nombre completo y DNI).
    - Una tabla con todos sus prestamos: libro, fechas, estado, etc.
      Las filas se pintan alternadas (una clara, una blanca) para leerlas mejor.

Se abre desde la gestion de socios y recibe solo el ID del socio: los datos
del socio y sus prestamos se piden a la base desde esta pantalla.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame


class VistaPrestamosSocio(BaseFrame):
    """Pantalla de solo lectura con los datos de un socio y su historial de prestamos."""

    def __init__(self, parent, controller, id_socio):
        """Pide los datos a la base y arma la ficha del socio y la tabla de prestamos.

        Args:
            parent: Frame contenedor donde se dibuja esta pantalla (el container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar de pantalla.
            id_socio (int): ID del socio del que se quiere ver el historial.
        """
        super().__init__(parent, controller)
        self.controller = controller #* Guardamos la ventana principal para poder volver a la gestion de socios

        # ? Traer datos del socio y sus préstamos de la base de datos mysql
        #? self.socio es un diccionario con los datos del socio; self.prestamos_socio es la lista de sus prestamos
        self.socio = self.ApiSocios.obtener_socio_por_id(id_socio)
        self.prestamos_socio = self.ApiSocios.listar_prestamos_socio(id_socio)

        #? Si el socio no existe avisamos y volvemos a la lista.
        #? El "return" corta __init__ aca: no se arma el resto de la pantalla.
        #? OJO: volver_atras() llama a show_frame desde adentro del constructor de esta misma pantalla;
        #? es muy probable que despues show_frame intente mostrar un widget que ya fue destruido (error de Tkinter).
        if not self.socio:
            messagebox.showerror("Error", "No se encontró el socio.")
            self.volver_atras()
            return

        #? Si la consulta devuelve None (en vez de una lista vacia) lo cambiamos por [],
        #? asi el resto del codigo siempre puede recorrerlo sin errores.
        if self.prestamos_socio is None:
            self.prestamos_socio = []

        # Estilos
        #? ttk.Style define estilos con nombre ("Prestamos.Treeview") que despues se aplican a las tablas.
        #? Los estilos son GLOBALES de toda la aplicacion: una vez creado, cualquier tabla que use este
        #? nombre (por ejemplo, la de CrearLibro) lo toma tambien.
        style = ttk.Style(self)
        style.configure(
            "Prestamos.Treeview",
            rowheight=30, #* Altura de cada fila
            font=("Arial", 10)
        )
        style.configure(
            "Prestamos.Treeview.Heading", #* El estilo de los encabezados siempre se llama "<estilo>.Heading"
            font=("Arial", 10, "bold")
        )

        # Distribución del contenido
        #? frame_central ya viene creado desde BaseFrame. Tiene una columna que se estira
        #? y la fila 2 (la de la tabla) es la que se estira al agrandar la ventana.
        self.frame_central.columnconfigure(0, weight=1)
        self.frame_central.rowconfigure(2, weight=1)

        #? Los f-strings (f"...{valor}") arman el texto metiendo valores del diccionario del socio.
        #? Dos strings seguidos entre parentesis se pegan como uno solo.
        self.crear_titulo(
            f"Préstamos de {self.socio['nombre']} "
            f"{self.socio['apellido']}"
        )

        # Ficha del socio
        #? LabelFrame = frame con borde y un titulo arriba ("Información del socio")
        self.frame_datos = tk.LabelFrame(
            self.frame_central,
            text="Información del socio",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=10
        )
        self.frame_datos.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=10,
            pady=(10, 15)
        )

        #? 3 columnas dentro de la ficha: la del medio (el nombre) es el doble de ancha que las de los costados
        self.frame_datos.columnconfigure((0,2), weight=1)
        self.frame_datos.columnconfigure(1, weight=2)

        #*-- Los tres datos del socio, uno al lado del otro (columnas 0, 1 y 2)
        tk.Label(
            self.frame_datos,
            text=f"ID: {self.socio['id_socio']}",
            font=("Arial", 10)
        ).grid(row=0, column=0, sticky="w", padx=8)

        tk.Label(
            self.frame_datos,
            text=f"Socio: {self.socio['nombre']} "
                 f"{self.socio['apellido']}",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, sticky="w", padx=8)

        tk.Label(
            self.frame_datos,
            text=f"DNI: {self.socio['dni']}",
            font=("Arial", 10)
        ).grid(row=0, column=2, sticky="w", padx=8)

        # Encabezado del historial
        #? Se guarda en self.lbl_historial porque despues actualizar_tabla le cambia el texto (suma la cantidad de registros)
        self.lbl_historial = tk.Label(
            self.frame_central,
            text="Historial de préstamos",
            font=("Arial", 12, "bold"),
            anchor="w" #* Texto pegado a la izquierda
        )
        self.lbl_historial.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 8)
        )

        # Tabla
        self.frame_tabla = tk.Frame(self.frame_central)
        self.frame_tabla.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0, 10)
        )

        self.frame_tabla.rowconfigure(0, weight=1)
        self.frame_tabla.columnconfigure(0, weight=1)

        #? Nombres internos de las columnas. Los textos que se ven y los anchos se definen en los diccionarios de abajo.
        columnas = (
            "id",
            "libro",
            "fecha_prestamo",
            "fecha_devolucion_estimada",
            "fecha_devolucion_real",
            "estado"
        )

        #? A diferencia de otras pantallas, esta tabla se crea a mano (no con crear_treeview de BaseFrame).
        #? show="headings" muestra los encabezados y oculta la columna extra "#0".
        #? selectmode="browse" = se puede seleccionar una sola fila.
        self.tabla = ttk.Treeview(
            self.frame_tabla,
            columns=columnas,
            show="headings",
            selectmode="browse",
            style="Prestamos.Treeview" #* Aplica el estilo definido arriba
        )

        #? Dos diccionarios {nombre interno: valor}: uno con el texto del encabezado y otro con el ancho
        encabezados = {
            "id": "ID",
            "libro": "Libro",
            "fecha_prestamo": "Fecha de préstamo",
            "fecha_devolucion_estimada": "Vencimiento",
            "fecha_devolucion_real": "Devolución real",
            "estado": "Estado"
        }

        anchos = {
            "id": 55,
            "libro": 220,
            "fecha_prestamo": 135,
            "fecha_devolucion_estimada": 135,
            "fecha_devolucion_real": 135,
            "estado": 100
        }

        #? Recorremos las columnas y, con los diccionarios, configuramos cada una (texto, ancho y alineacion).
        #? anchor="center" centra el contenido; minwidth es el ancho minimo al achicar la columna.
        for columna in columnas:
            self.tabla.heading(
                columna,
                text=encabezados[columna]
            )
            self.tabla.column(
                columna,
                width=anchos[columna],
                minwidth=60,
                anchor="center"
            )

        #? La columna "libro" es la excepcion: se alinea a la izquierda ("w" = west) porque tiene texto largo
        self.tabla.column("libro", anchor="w")

        #? Scrollbars conectadas en los dos sentidos con la tabla:
        #?   - command=...yview/xview -> al mover la barra, se mueve la tabla
        #?   - yscrollcommand / xscrollcommand = barra.set -> al mover la tabla, se mueve la barra
        scrollbar_y = ttk.Scrollbar(
            self.frame_tabla,
            orient="vertical",
            command=self.tabla.yview
        )

        scrollbar_x = ttk.Scrollbar(
            self.frame_tabla,
            orient="horizontal",
            command=self.tabla.xview
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns") #* Barra vertical a la derecha
        scrollbar_x.grid(row=1, column=0, sticky="ew") #* Barra horizontal abajo

        # Filas alternadas
        #? Un "tag" es una etiqueta que se le pone a las filas para darles formato.
        #? Aca se definen dos: "par" (gris claro) e "impar" (blanco). Se asignan en actualizar_tabla.
        self.tabla.tag_configure("par", background="#F2F5F9")
        self.tabla.tag_configure("impar", background="#FFFFFF")

        # Botones inferiores de BaseFrame
        self.crear_boton_volver(self.volver_atras)

        # Cargar información
        self.actualizar_tabla(self.prestamos_socio)

    def actualizar_tabla(self, prestamos_socio):
        """Borra las filas de la tabla y la vuelve a llenar con los prestamos recibidos.

        Tambien actualiza el encabezado con la cantidad de registros.

        Args:
            prestamos_socio (list[dict]): Prestamos a mostrar. Cada dict necesita las claves
                "id", "libro", "fecha_prestamo", "fecha_devolucion_estimada",
                "fecha_devolucion_real" y "estado".
        """
        #? get_children() devuelve todas las filas; el "*" las pasa como argumentos separados,
        #? asi un solo delete() las borra a todas de una vez.
        self.tabla.delete(*self.tabla.get_children())

        #? enumerate() da, para cada prestamo, su numero de orden (indice: 0, 1, 2...) ademas del prestamo
        for indice, prestamo in enumerate(prestamos_socio):
            self.tabla.insert(
                "",
                "end",
                values=(
                    prestamo["id"],
                    prestamo["libro"],
                    prestamo["fecha_prestamo"],
                    prestamo["fecha_devolucion_estimada"],
                    #? Si todavia no se devolvio, la fecha real es None (NULL en la base): ahi mostramos "-"
                    prestamo["fecha_devolucion_real"] or "-",
                    prestamo["estado"]
                ),
                #? Fila par -> tag "par", fila impar -> tag "impar" (asi quedan alternadas).
                #? La coma final es necesaria: tags espera una tupla, y ("x",) es una tupla de un solo elemento.
                tags=("par" if indice % 2 == 0 else "impar",)
            )

        #* Actualiza el titulo del historial con la cantidad de prestamos
        cantidad = len(prestamos_socio)
        self.lbl_historial.config(
            text=f"Historial de préstamos  ·  {cantidad} registro(s)"
        )

    def volver_atras(self):
        """Vuelve a la pantalla de gestion de socios (boton "Volver")."""
        #? El import esta aca adentro y no arriba del archivo, seguramente para evitar un
        #? "import circular" (GestionSocios tambien importa a esta pantalla).
        from views.socio_views.gestion_socios_view import GestionSocios
        self.controller.show_frame(GestionSocios)