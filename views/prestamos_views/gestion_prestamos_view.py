"""Pantalla de gestion de prestamos de LibManage.

Muestra el listado de prestamos en una tabla y permite:
    - Buscar por socio o por libro.
    - Ordenar por fecha de vencimiento.
    - Alternar entre ver todos los prestamos o solo los vencidos.
    - Marcar como devuelto el prestamo seleccionado (solo si esta activo).
    - Ir a registrar un prestamo nuevo y volver al inicio.

Igual que las otras pantallas, usa metodos heredados de BaseFrame para armar
la barra de busqueda, los botones y la tabla.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame

class GestionPrestamos(BaseFrame):
    """Pantalla con el listado de prestamos y las acciones para gestionarlos."""

    def __init__(self, parent, controller):
        """Arma la pantalla: controles, tabla y carga inicial de prestamos desde la base.

        Args:
            parent: Frame contenedor donde se dibuja esta pantalla (el container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar de pantalla.
        """
        super().__init__(parent, controller)
        self.controller = controller #* Guardamos la ventana principal para poder navegar a otras pantallas
        #? Recuerda si el filtro "Solo vencidos" esta activo (True) o si se ven todos (False).
        #? Arranca en False: al abrir la pantalla se muestran todos los prestamos.
        self.solo_vencidos = False


        # ?--- Frame Central
        self.frame_central = self.crear_frame_central() #* Frame donde va todo el contenido (metodo de BaseFrame)
        #? Dos columnas con proporcion 4 a 1: la 0 (barra de busqueda) ocupa 4/5 del ancho
        #? y la 1 (boton "Buscar") el 1/5 restante.
        self.frame_central.columnconfigure(0, weight=4)
        self.frame_central.columnconfigure(1, weight=1)

        #? weight=0 = esas filas no se estiran (tienen la altura justa).
        #? La fila 2 (la tabla) es la unica que se estira al agrandar la ventana.
        self.frame_central.rowconfigure((0,1,3), weight=0)
        self.frame_central.rowconfigure(2, weight=1)

        #? -- TItulo
        self.crear_titulo("Gestion de Prestamos")

        #? --- Barra de busqueda
        #? Se le pasa self.buscar SIN parentesis: es la funcion que se va a ejecutar al buscar (no se ejecuta ahora)
        self.crear_barra_busqueda("Buscar préstamo", self.buscar)

        #? La barra de busqueda viene de BaseFrame y probablemente ocupa las 2 columnas.
        #? Con columnspan=1 la achicamos a una sola columna para que al lado entre el boton "Buscar".
        self.busqueda.grid_configure(columnspan=1, padx=(0, 5))

        #* Boton "Buscar" al lado de la barra (hace lo mismo que apretar la tecla de busqueda de la barra)
        self.boton = tk.Button( #! se puede refactorizar
            self.frame_central, text="Buscar", command=self.buscar
        )
        self.boton.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        #? Boton Ordenar
        self.crear_boton_ordenar(self.ordenar)

        #? Boton Filtrar
        self.crear_boton_filtrar(self.filtrar)

        #? Boton Solo Vencidos
        #? Reutilizamos el boton generico de filtrar (self.btn_filtros) y solo le cambiamos el texto.
        #? Cuando se aprieta, filtrar() lo alterna entre "Solo vencidos" y "Mostrar todos".
        self.btn_filtros.config(text="Solo vencidos")

        #? --- Tabla de Prestamos
        #? Nombres de las columnas y ancho de cada una (en pixeles), en el mismo orden.
        #? Cada fila que se inserta tiene que traer sus 5 valores en este orden: id, socio, libro, vence, estado.
        columnas = ("id", "socio", "libro", "vence", "estado")
        ancho = (40, 140, 180, 90, 100)
        #? crear_treeview (de BaseFrame) arma la tabla y la deja guardada en self.tabla
        self.crear_treeview(self.frame_central, columnas, ancho)

        # --- Botones de Acción (Inferiores)
        self.frame_acciones = tk.Frame(self.frame_central)
        self.frame_acciones.grid(row=3, column=0, columnspan=2, sticky="ew", pady=5)
        self.frame_acciones.columnconfigure(0, weight=1)

        #* Boton "devolver": se ubica a la derecha y arranca deshabilitado (no hay nada seleccionado)
        self.btn_devolver = tk.Button(self.frame_acciones, text="devolver", command=self.marcar_devuelto, )
        self.btn_devolver.pack(side="right", padx=5)
        self.btn_devolver.config(state="disabled")

        #? "<<TreeviewSelect>>" es un evento que Tkinter dispara cada vez que cambia la fila seleccionada.
        #? Asi el boton "devolver" se habilita o deshabilita solo, segun el prestamo elegido.
        self.tabla.bind("<<TreeviewSelect>>", self.actualizar_boton_devolver)

        #? Boton Crear (Registrar prestamo)
        self.crear_boton_crear("Registrar Prestamo", self.registrar_prestamo)

        #? Boton Volver Atras
        self.crear_boton_volver(self.volver_atras)

        #? Traer prestamos de la base de datos
        #? Se guardan en self.prestamos_datos: buscar y ordenar trabajan sobre esta lista, sin volver a consultar la base.
        self.prestamos_datos = self.ApiPrestamos.listar_prestamos()
        self.actualizar_tabla(self.prestamos_datos)


    def filtrar(self):
        """Alterna entre mostrar todos los prestamos y mostrar solo los vencidos.

        Se ejecuta con el boton de filtro. Cada vez que se aprieta cambia de modo
        y el texto del boton cambia entre "Solo vencidos" y "Mostrar todos".
        """
        nuevo_estado = not self.solo_vencidos #? "not" invierte el valor: True pasa a False y viceversa

        #*-- Pedimos a la base la lista segun el modo nuevo
        try:
            datos = self.ApiPrestamos.listar_prestamos(
                solo_vencidos=nuevo_estado
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudieron filtrar los préstamos: {error}"
            )
            return

        #? Recien ahora, con la consulta ya exitosa, guardamos el modo nuevo.
        #? Asi, si la consulta falla, el estado no cambia y el boton no queda desincronizado con la tabla.
        self.solo_vencidos = nuevo_estado
        self.prestamos_datos = datos

        self.busqueda.delete(0, tk.END) #* Borra el texto de la barra de busqueda
        self.actualizar_tabla(self.prestamos_datos)

        #* Cambiamos el texto del boton segun el modo actual
        if self.solo_vencidos:
            self.btn_filtros.config(text="Mostrar todos")
        else:
            self.btn_filtros.config(text="Solo vencidos")

    def actualizar_tabla(self, lista_prestamos):
        """Limpia y vuelve a cargar los datos en la tabla.

        Args:
            lista_prestamos (list[tuple]): Prestamos a mostrar. Cada uno trae sus valores
                en el orden de las columnas: (id, socio, libro, vence, estado).
        """
        #*-- Primero se borran todas las filas actuales
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        #*-- Despues se agrega una fila por cada prestamo
        #? "" = sin padre (fila de primer nivel), "end" = la agrega al final.
        #? Como cada prestamo ya viene como tupla en el orden de las columnas, se pasa directo a values.
        for prestamo in lista_prestamos:
            self.tabla.insert("", "end", values=prestamo)

        #? Al recargar la tabla se pierde la seleccion, asi que re-evaluamos si el boton "devolver" debe quedar habilitado
        self.actualizar_boton_devolver()


    def actualizar_boton_devolver(self, event=None):
        """Habilita el boton "devolver" solo si hay un prestamo seleccionado y esta activo.

        Args:
            event: Evento de Tkinter (lo manda <<TreeviewSelect>>, no se usa). Tiene valor
                por defecto None para poder llamar a la funcion tambien sin evento.
        """
        seleccion = self.tabla.selection() #* Devuelve las filas seleccionadas

        #* Sin nada seleccionado: boton deshabilitado y cortamos
        if not seleccion:
            self.btn_devolver.config(state="disabled")
            return

        #? .item(fila, "values") devuelve los valores de la fila; el [4] es la columna "estado".
        #? Se usa str(), strip() y lower() para comparar sin errores por espacios, mayusculas o tipo de dato.
        valores = self.tabla.item(seleccion[0], "values")
        estado = str(valores[4]).strip().lower()

        #? Solo se puede devolver un prestamo "activo" (los otros estados son "devuelto" y "cerrado_sin_devolver")
        if estado == "activo":
            self.btn_devolver.config(state="normal")
        else:
            self.btn_devolver.config(state="disabled")

    def buscar(self, event=None):
        """Filtra la lista de prestamos según lo ingresado.

        Busca el texto en el nombre del socio o en el libro, sin distinguir
        mayusculas de minusculas. Si la barra esta vacia, muestra todos.

        Args:
            event: Evento de Tkinter (no se usa). Tiene valor por defecto None para
                poder usar la funcion tanto desde un boton como desde una tecla.
        """
        texto = self.busqueda.get().strip().lower() #? Pasamos todo a minusculas para comparar sin importar mayusculas
        #* Si no escribio nada mostramos todos y cortamos
        if not texto:
            self.actualizar_tabla(self.prestamos_datos)
            return

        #? List comprehension: arma una lista nueva solo con los prestamos donde el texto aparece
        #? en el socio (p[1]) o en el libro (p[2]). Los numeros son las posiciones de las columnas.
        resultados = [
            p for p in self.prestamos_datos
            if texto in p[1].lower() or texto in p[2].lower()
        ]
        self.actualizar_tabla(resultados)

    def limpiar_busqueda(self):
        """Restablece la búsqueda y muestra todos los datos."""
        self.busqueda.delete(0, tk.END) #* Borra el texto de la barra (de la posicion 0 hasta el final)
        self.actualizar_tabla(self.prestamos_datos)

    def ordenar(self):
        """Ordena los prestamos por fecha de vencimiento."""
        #? sorted() devuelve una lista nueva ordenada (no modifica self.prestamos_datos).
        #? key=lambda x: x[3] le dice que ordene por la posicion 3, que es la columna "vence".
        prestamos_ordenados = sorted(self.prestamos_datos, key=lambda x: x[3])
        self.actualizar_tabla(prestamos_ordenados)


    def marcar_devuelto(self):
        """Marca como devuelto el prestamo seleccionado, previa confirmacion.

        Se ejecuta con el boton "devolver". Pasos:
            1. Verifica que haya un prestamo seleccionado.
            2. Pide confirmacion al usuario.
            3. Registra la devolucion en la base.
            4. Recarga la tabla desde la base y avisa que salio bien.
        """
        seleccion = self.tabla.selection()

        #*-- 1. Verificamos que haya algo seleccionado
        if not seleccion:
            self.mensaje_advertencia("Atención", "Seleccioná un préstamo.")
            return

        #? .item(...)["values"][0] es el id del prestamo (primera columna). Se pasa a int porque la tabla lo guarda como texto.
        item = self.tabla.item(seleccion[0])
        id_prestamo = int(item["values"][0])

        #*-- 2. Pedimos confirmacion (devuelve True si el usuario acepta)
        confirmar = self.mensaje_confirmacion("Confirmar devolución", f"¿Confirmás la devolución del préstamo {id_prestamo}?")

        if not confirmar:
            return

        #*-- 3 y 4. Registramos la devolucion y actualizamos la tabla
        try:
            resultado = self.ApiPrestamos.devolver_prestamo(id_prestamo)

            #? Si devuelve un valor "falso" es que no se pudo devolver (ej: el prestamo ya no estaba activo)
            if not resultado:
                self.mensaje_advertencia("Atención", "El préstamo no está activo o no puede devolverse.")
                return

            # Volver a consultar MySQL para actualizar la tabla
            #? Se respeta el filtro actual (todos o solo vencidos) al volver a pedir la lista
            self.prestamos_datos = self.ApiPrestamos.listar_prestamos(
                solo_vencidos=self.solo_vencidos
            )
            self.actualizar_tabla(self.prestamos_datos)

            self.mensaje_info("Devolución registrada","El préstamo fue devuelto correctamente.")

        except Exception as error: #? Atrapa cualquier error (ej: problema con la base) y lo muestra, para que el programa no se cierre
            messagebox.showerror(
                "Error",
                f"No se pudo registrar la devolución: {error}"
            )


    def registrar_prestamo(self):
        """Va a la pantalla para registrar un prestamo nuevo (boton "Registrar Prestamo")."""
        #? El import esta aca adentro y no arriba del archivo, para evitar un
        #? "import circular" (RegistrarPrestamo tambien importa a esta pantalla).
        from views.prestamos_views.registrar_prestamo_view import RegistrarPrestamo
        self.controller.show_frame(RegistrarPrestamo)

    def volver_atras(self): #! Esto lo podriamos pasar a controller me parece
        """Vuelve a la pantalla de inicio (boton "Volver")."""
        #? Import dentro de la funcion por el mismo motivo que en registrar_prestamo (evitar import circular)
        from views.home_view.home_view import HomeView
        self.controller.show_frame(HomeView)