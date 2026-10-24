"""Pantalla de gestion de socios de LibManage.

Muestra el listado de socios en una tabla y permite:
    - Buscar por DNI, nombre o apellido.
    - Ordenar por apellido.
    - Registrar un socio nuevo.
    - Ver los prestamos / historial del socio seleccionado.
    - Volver al inicio.

Igual que las otras pantallas de gestion, usa metodos heredados de BaseFrame
para armar la barra de busqueda, los botones y la tabla.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame


class GestionSocios(BaseFrame):
    """Pantalla con el listado de socios y las acciones para gestionarlos."""

    def __init__(self, parent, controller):
        """Arma la pantalla: pide los socios a la base, crea los controles y llena la tabla.

        Args:
            parent: Frame contenedor donde se dibuja esta pantalla (el container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar de pantalla.
        """
        super().__init__(parent, controller)
        self.controller = controller #* Guardamos la ventana principal para poder navegar a otras pantallas

        #? Traer socios de la base de datos
        #? Se piden UNA sola vez al abrir la pantalla y se guardan en self.socios.
        #? Buscar y ordenar trabajan sobre esta lista, sin volver a consultar la base.
        self.socios = self.ApiSocios.listar_socios()

        #? Frame Central
        #? Aca se usa self.frame_central directamente (sin crearlo): ya viene creado desde BaseFrame.
        #? Se le configuran 2 columnas que se reparten el ancho por igual.
        self.frame_central.columnconfigure(0, weight=1) #? Esto tambien se podria refactorizar
        self.frame_central.columnconfigure(1, weight=1)

        #? Titulo
        self.crear_titulo("Gestion de Socios")

        #? Barra de busqueda
        #? Se le pasa self.buscar SIN parentesis: es la funcion que se va a ejecutar al buscar (no se ejecuta ahora)
        self.crear_barra_busqueda("Buscar Socio", self.buscar)

        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #? Creando el treeview
        #? Nombres de las columnas y ancho de cada una (en pixeles), en el mismo orden:
        #? id_socio=40, dni=80, nombre=140, apellido=140
        columnas = ("id_socio", "dni", "nombre", "apellido")
        ancho = (40,80,140,140)
        #? crear_treeview (de BaseFrame) arma la tabla y la deja guardada en self.tabla
        self.crear_treeview(self.frame_central, columnas, ancho)

        #? Ver prestamos
        #? Este boton se define mas abajo, en esta misma clase (crear_boton_ver)
        self.crear_boton_ver("Préstamos / Historial", self.ver_prestamos)

        #? Boton Crear (Agregar socio)
        self.crear_boton_crear("Registrar Socio", self.registrar_socio)

        #? Boton Volver
        self.crear_boton_volver(self.volver_atras)

        #! Renderizamos los datos de los socios
        self.actualizar_tabla(self.socios)

    def crear_boton_ver(self, texto, funcion_ver):
        """Crea el boton "ver" en la barra de botones de abajo.

        Se define aca (y no en BaseFrame) porque es un boton propio de esta pantalla.

        Args:
            texto (str): Texto que muestra el boton.
            funcion_ver: Funcion que se ejecuta al hacer click (se pasa sin parentesis).
        """
        self.frame_inferior.columnconfigure(2, weight=1) #? La columna 2 de la barra de abajo se estira (ahi va este boton)
        self.btn_ver = tk.Button(
            self.frame_inferior,
            text=texto,
            fg="black", #* Color del texto
            command=funcion_ver,
        )
        self.btn_ver.grid(row=0, column=2, sticky="ew", padx=(10,10), pady=(10, 0), ipady=6)

    def filtrar(self):
        """Boton "Filtrar". Por ahora es un marcador: solo imprime un mensaje en la consola."""
        #! Pendiente: todavia no filtra nada
        print("Filtrando")

    def actualizar_tabla(self, lista_socios):
        """Limpia y vuelve a cargar los datos en la tabla.

        Args:
            lista_socios (list[dict]): Socios a mostrar. Cada dict necesita las claves
                "id_socio", "dni", "nombre" y "apellido".
        """
        #*-- Primero se borran todas las filas actuales
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        #*-- Despues se agrega una fila por cada socio
        #? "" = sin padre (fila de primer nivel), "end" = la agrega al final.
        #? El orden de values tiene que coincidir con el orden de las columnas de la tabla.
        for socio in lista_socios:
            self.tabla.insert(
                "",
                "end",
                values=(
                    socio["id_socio"],
                    socio["dni"],
                    socio["nombre"],
                    socio["apellido"]
                )
            )

    def buscar(self, event=None):
        """Filtra los socios según lo ingresado.

        Busca el texto en el DNI, el nombre o el apellido, sin distinguir
        mayusculas de minusculas. Si la barra esta vacia, muestra todos.

        Args:
            event: Evento de Tkinter (no se usa). Tiene valor por defecto None para
                poder usar la funcion tanto desde un boton como desde una tecla.
        """
        texto = self.busqueda.get().strip().lower() #? Pasamos todo a minusculas para comparar sin importar mayusculas

        #* Si no escribio nada mostramos todos y cortamos
        if not texto:
            self.actualizar_tabla(self.socios)
            return

        #? List comprehension: arma una lista nueva solo con los socios donde el texto aparece
        #? en el DNI, en el nombre o en el apellido ("in" = "esta contenido en").
        #? str() convierte el DNI a texto por si llega como numero, asi lower() no falla.
        resultados = [
            socio for socio in self.socios
            if texto in str(socio["dni"]).lower()
            or texto in socio["nombre"].lower()
            or texto in socio["apellido"].lower()
        ]

        self.actualizar_tabla(resultados)

    def limpiar_busqueda(self):
        """Restablece la búsqueda y muestra todos los socios."""
        self.busqueda.delete(0, tk.END) #* Borra el texto de la barra (de la posicion 0 hasta el final)
        self.actualizar_tabla(self.socios)

    def ordenar(self):
        """Ordena los socios por apellido."""
        #? sorted() devuelve una lista nueva ordenada (no modifica self.socios).
        #? key=lambda socio: ... le dice por que campo ordenar; .lower() hace que no importe si empieza con mayuscula o minuscula.
        socios_ordenados = sorted(
            self.socios,
            key=lambda socio: socio["apellido"].lower()
        )

        self.actualizar_tabla(socios_ordenados)

    def registrar_socio(self, socio=None):
        """Va a la pantalla para registrar un socio (boton "Registrar Socio").

        Args:
            socio (dict | None): Datos de un socio ya existente, para precargarlos en la pantalla.
                Con el boton llega None, y la pantalla funciona en modo "registrar uno nuevo".
        """
        #? El import esta aca adentro y no arriba del archivo, seguramente para evitar un
        #? "import circular" (RegistrarSocio tambien importa a esta pantalla).
        from views.socio_views.registrar_socio_view import RegistrarSocio
        #? Si socio es None, show_frame arma la pantalla sin pasarle datos
        self.controller.show_frame(RegistrarSocio, socio)

    def volver_atras(self):
        """Vuelve a la pantalla de inicio (boton "Volver")."""
        #? Import dentro de la funcion por el mismo motivo que en registrar_socio (evitar import circular)
        from views.home_view.home_view import HomeView
        self.controller.show_frame(HomeView)

    def ver_prestamos(self, datos=None):
        """Abre la pantalla de prestamos del socio seleccionado en la tabla.

        Se ejecuta con el boton "Préstamos / Historial". Si no hay ningun socio
        seleccionado, muestra un aviso.

        Args:
            datos: No se usa. Queda por defecto en None porque el boton llama a la funcion sin parametros.
        """
        seleccionado = self.tabla.selection() #* Devuelve las filas seleccionadas

        #* Si no hay ninguna fila seleccionada, avisamos y cortamos
        if not seleccionado:
            messagebox.showwarning("Aviso", "Seleccione un socio")
            return

        #? .item(...)["values"] devuelve los valores de la fila; el [0] es la primera columna (el id_socio)
        item = self.tabla.item(seleccionado[0])
        id_socio = item["values"][0]

        #? Import dentro de la funcion por el mismo motivo que en registrar_socio (evitar import circular)
        from views.socio_views.prestamos_socio_view import VistaPrestamosSocio
        #? Al abrir la pantalla nueva solo se le pasa el id del socio (el tercer valor es el parametro "datos" de show_frame)
        self.controller.show_frame(
            VistaPrestamosSocio,
            id_socio
        )