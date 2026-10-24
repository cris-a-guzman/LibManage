"""Pantalla para registrar un prestamo nuevo en LibManage.

El usuario completa un formulario con estos pasos:
    1. Elige el socio escribiendo o seleccionando su DNI.
    2. Busca un libro por titulo (solo aparecen los que tienen ejemplares disponibles).
    3. Indica la cantidad y lo agrega a la lista del prestamo (se pueden agregar varios libros).
    4. Escribe la fecha de devolucion estimada (dd/mm/aaaa).
    5. Confirma, y el prestamo se guarda en la base.

La fecha de prestamo es automatica (la de hoy).
"""

import tkinter as tk
from tkinter import ttk,messagebox
from datetime import date, datetime
from views.components.lista_desplegable import AutocompleteCombobox
from views.components.base_frame import BaseFrame
from views.components.formulario_desplazable import FormularioDesplazable

class RegistrarPrestamo(BaseFrame):
    """Pantalla con el formulario para registrar un prestamo de uno o varios libros."""

    def __init__(self, parent, controller):
        """Arma la pantalla: carga los datos de socios y libros y crea todo el formulario.

        Args:
            parent: Frame contenedor donde se dibuja esta pantalla (el container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar de pantalla.
        """
        super().__init__(parent, controller)
        self.controller = controller #* Guardamos la ventana principal para poder volver al listado despues

        # Carga de datos desde la API/Repositories
        #? Se piden UNA sola vez al abrir la pantalla: la lista de DNI de los socios
        #? y los libros con la cantidad de ejemplares que hay disponibles de cada uno.
        self.dni_socios = self.ApiSocios.obtener_socios_dni()
        self.libros_catalogo = self.ApiLibros.obtener_disponibilidad_libros()

        #? Diccionario {texto que se ve en la lista desplegable: datos del libro}.
        #? La clave es un texto como "[3 disponibles] Realismo capitalista (ID 1)": asi el usuario ve
        #? cuantos quedan y, cuando elige uno, con esa clave recuperamos el diccionario completo del libro.
        #? El "if" del final deja afuera los libros sin ejemplares disponibles (no se pueden prestar).
        self.opciones_libros = {
            f"[{int(libro['disponibles'])} disponibles] "
            f"{libro['titulo']} (ID {libro['id_libro']})": libro
            for libro in self.libros_catalogo
            if libro["disponibles"] > 0
        }
        #*-- Estado de la pantalla (lo que el usuario fue eligiendo)
        self.socio_seleccionado = None #* DNI del socio elegido (None = todavia no eligio)
        self.libro_seleccionado = None #* Libro elegido en el combo, antes de agregarlo (None = ninguno)
        self.libros_seleccionados = {} #? Libros ya agregados al prestamo: {id_libro: {"titulo": ..., "cantidad": ...}}

        # Configuración del grid del contenedor principal
        self.rowconfigure(0, weight=0) #* Fila 0 (el titulo): no se estira
        self.rowconfigure(1, weight=1) #* Fila 1 (el formulario): se estira al agrandar la ventana
        self.columnconfigure(0, weight=1)

        #* Titulo de la pantalla (armado a mano con un Label)
        tk.Label(
            self, text="Registrar Préstamo", font=("Arial", 14, "bold")
        ).grid(row=0, column=0, sticky="new", pady=12)

        # --- Frame Central
        #? FormularioDesplazable es un contenedor con scroll: lo que se pone dentro de su
        #? atributo .contenido se puede desplazar si no entra en la ventana.
        #? OJO: aca se usa self.frame_central antes de crearlo en esta clase; tiene que venir ya creado desde BaseFrame.
        self.scroll_formulario = FormularioDesplazable(
        self.frame_central
        )
        self.scroll_formulario.pack(fill="both", expand=True)

        #? Ahora self.frame_central pasa a ser el frame que va DENTRO del scroll: ahi se pone todo el formulario
        self.frame_central = tk.Frame(self.scroll_formulario.contenido, padx=20, pady=5)
        self.frame_central.pack(fill="both", expand=True)
        self.frame_central.columnconfigure(0, weight=1) #* Una sola columna que ocupa todo el ancho

        # --- Buscar Socio (DNI)
        tk.Label(
            self.frame_central, text="Ingrese DNI del SOCIO:"
        ).grid(row=0, column=0, sticky="w", pady=(5, 0))

        #? AutocompleteCombobox es un componente propio: una lista desplegable que
        #? va sugiriendo opciones mientras se escribe. set_completion_list le da las opciones (los DNI).
        self.combo_dni_socio = AutocompleteCombobox(
            self.frame_central, width=30, font=("Arial", 10)
        )
        self.combo_dni_socio.set_completion_list(self.dni_socios)
        self._configurar_placeholder(self.combo_dni_socio, "Escribir DNI...")
        self.combo_dni_socio.grid(row=1, column=0, sticky="ew", ipady=5, pady=(0, 5))
        #? "<<ComboboxSelected>>" es el evento que se dispara cuando el usuario ELIGE una opcion de la lista
        self.combo_dni_socio.bind("<<ComboboxSelected>>", self.al_seleccionar_socio)

        #* Etiqueta que confirma que socio se eligio (arranca en gris y pasa a verde al elegir)
        self.lbl_socio_seleccionado = tk.Label(
            self.frame_central,
            text="Ningún socio seleccionado",
            bg="#f0f0f0",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_socio_seleccionado.grid(row=2, column=0, sticky="ew", pady=(0, 10))

        # --- Buscar Libro (Título)
        tk.Label(
            self.frame_central, text="Buscar libro por TÍTULO:"
        ).grid(row=3, column=0, sticky="w", pady=(5, 0))

        #? Mismo componente que el de los socios, pero las opciones son los textos de self.opciones_libros
        self.combo_libro = AutocompleteCombobox(
            self.frame_central, width=30, font=("Arial", 10)
        )
        self.combo_libro.set_completion_list(
            list(self.opciones_libros.keys())
        )
        self._configurar_placeholder(self.combo_libro, "Escribir título...")
        self.combo_libro.grid(row=4, column=0, sticky="ew", ipady=5, pady=(0, 5))
        self.combo_libro.bind("<<ComboboxSelected>>", self.al_seleccionar_libro)

        #* Etiqueta que confirma que libro se eligio
        self.lbl_libro_seleccionado = tk.Label(
            self.frame_central,
            text="Ningún libro seleccionado",
            bg="#f0f0f0",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_libro_seleccionado.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        # --- Libros incluidos en el préstamo
        #? LabelFrame = un frame con borde y un titulo arriba ("Libros del préstamo")
        self.frame_libros = tk.LabelFrame(
            self.frame_central,
            text="Libros del préstamo",
            padx=10,
            pady=10
        )
        self.frame_libros.grid(
            row=6, column=0, sticky="ew", pady=10
        )
        self.frame_libros.columnconfigure(0, weight=1)

        # Controles para agregar ejemplares
        #? Fila con "Cantidad: [__] [Agregar libro]". Se usa pack(side="left") para ponerlos uno al lado del otro.
        self.controles_libros = tk.Frame(self.frame_libros)
        self.controles_libros.grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        tk.Label(
            self.controles_libros,
            text="Cantidad:"
        ).pack(side="left", padx=5)

        #? Spinbox = cuadro numerico con flechitas para subir y bajar (de 1 a 999).
        #? Igual se puede escribir a mano, por eso mas adelante se valida con int().
        self.cantidad_libro = tk.Spinbox(
            self.controles_libros,
            from_=1,
            to=999,
            width=5
        )
        self.cantidad_libro.pack(side="left", padx=5)

        self.btn_agregar_libro = tk.Button(
            self.controles_libros,
            text="Agregar libro",
            command=self.agregar_libro
        )
        self.btn_agregar_libro.pack(side="left", padx=5)

        # Tabla de libros seleccionados
        #? show="headings" muestra los encabezados y oculta la columna extra "#0".
        #? selectmode="browse" = se puede seleccionar una sola fila. height=4 = se ven 4 filas a la vez.
        self.tabla_libros = ttk.Treeview(
            self.frame_libros,
            columns=("titulo", "cantidad"),
            show="headings",
            height=4,
            selectmode="browse"
        )

        self.tabla_libros.heading("titulo", text="Libro")
        self.tabla_libros.heading("cantidad", text="Cantidad")

        self.tabla_libros.column("titulo", width=260)
        self.tabla_libros.column("cantidad", width=80)

        self.tabla_libros.grid(
            row=1, column=0, sticky="ew", pady=10
        )

        #? Scrollbar vertical conectada en los dos sentidos con la tabla:
        #?   - command=...yview -> al mover la barra, se mueve la tabla
        #?   - yscrollcommand=barra_libros.set -> al mover la tabla, se mueve la barra
        barra_libros = ttk.Scrollbar(
            self.frame_libros,
            orient="vertical",
            command=self.tabla_libros.yview
        )
        barra_libros.grid(row=1, column=1, sticky="ns")

        self.tabla_libros.configure(
            yscrollcommand=barra_libros.set
        )

        self.btn_quitar_libro = tk.Button(
            self.frame_libros,
            text="Quitar seleccionado",
            command=self.quitar_libro
        )
        self.btn_quitar_libro.grid(
            row=2, column=0, sticky="e"
        )

        # --- Fecha de préstamo (automática)
        tk.Label(
            self.frame_central, text="Fecha de préstamo (Automática)"
        ).grid(row=7, column=0, sticky="w", pady=(5, 0))

        #? Solo se muestra la fecha de hoy, el usuario no la puede editar (es una etiqueta, no un campo de texto).
        #? strftime("%d/%m/%Y") la escribe como dia/mes/año. Esta fecha no se manda al repositorio:
        #? al confirmar solo se envia la de devolucion, asi que la de prestamo se asigna del otro lado.
        self.lbl_fecha_prestamo = tk.Label(
            self.frame_central,
            text=date.today().strftime("%d/%m/%Y"),
            bg="#d9d9d9",
            bd=1,
            relief="solid",
            pady=8,
        )
        self.lbl_fecha_prestamo.grid(row=8, column=0, sticky="ew", pady=(0, 10))

        # --- Fecha de devolución estimada
        tk.Label(
            self.frame_central, text="Fecha de devolución estimada"
        ).grid(row=9, column=0, sticky="w", pady=(5, 0))

        #* Campo de texto donde el usuario escribe la fecha (con "dd/mm/aaaa" como texto de ejemplo)
        self.entry_fecha_devolucion = tk.Entry(self.frame_central, justify="center")
        self._configurar_placeholder(self.entry_fecha_devolucion, "dd/mm/aaaa")
        self.entry_fecha_devolucion.grid(
            row=10, column=0, sticky="ew", ipady=5, pady=(0, 15)
        )

        # --- Botones Confirmar / Cancelar
        #? Dos columnas con el mismo peso (weight=1): cada boton ocupa la mitad del ancho
        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=11, column=0, sticky="ew")
        self.frame_botones.columnconfigure(0, weight=1)
        self.frame_botones.columnconfigure(1, weight=1)

        self.btn_confirmar = tk.Button(
            self.frame_botones,
            text="Confirmar Préstamo",
            command=self.confirmar_prestamo,
        )
        self.btn_confirmar.grid(row=0, column=0, sticky="ew", padx=(0, 5), ipady=6)

        self.btn_cancelar = tk.Button(
            self.frame_botones, text="Cancelar", command=self.cancelar
        )
        self.btn_cancelar.grid(row=0, column=1, sticky="ew", padx=(5, 0), ipady=6)

    def _configurar_placeholder(self, widget, placeholder):
        """Helper para reutilizar la lógica de placeholders en campos de texto/combos.

        Tkinter no trae placeholders (texto de ejemplo que desaparece al escribir), asi que se simulan:
            - Se inserta el texto de ejemplo al crear el campo.
            - Al hacer click (FocusIn): si el texto es el de ejemplo, se borra.
            - Al salir del campo (FocusOut): si quedo vacio, se vuelve a poner el de ejemplo.

        Args:
            widget: Campo de texto o combo al que se le agrega el placeholder.
            placeholder (str): Texto de ejemplo a mostrar.
        """
        widget.insert(0, placeholder)
        #? Estos lambda son un "if" en una linea: "hacer A si se cumple la condicion, si no, no hacer nada (None)"
        widget.bind(
            "<FocusIn>",
            lambda e: widget.delete(0, tk.END) if widget.get() == placeholder else None,
        )
        widget.bind(
            "<FocusOut>",
            lambda e: widget.insert(0, placeholder) if widget.get().strip() == "" else None,
        )

    def al_seleccionar_socio(self, event):
        """Guarda el DNI elegido y lo confirma en la etiqueta verde.

        Se ejecuta cuando el usuario elige una opcion del combo de DNI. Ojo: no se dispara
        si solo escribe el DNI a mano sin elegirlo de la lista.

        Args:
            event: Evento de Tkinter (no se usa, pero Tkinter lo manda siempre).
        """
        dni_ingresado = self.combo_dni_socio.get().strip()
        #? Solo se guarda si hay algo escrito y no es el texto de ejemplo
        if dni_ingresado and dni_ingresado != "Escribir DNI...":
            # Guardamos la referencia al socio seleccionado
            self.socio_seleccionado = dni_ingresado
            self.lbl_socio_seleccionado.config(
                text=f"Socio Seleccionado (DNI): {dni_ingresado}", bg="#d9f2d9" #* bg verde: indica que ya hay un socio elegido
            )

    def al_seleccionar_libro(self, event):
        """Busca el libro elegido en el combo, lo guarda y lo muestra en la etiqueta verde.

        Se ejecuta cuando el usuario elige una opcion del combo de libros.

        Args:
            event: Evento de Tkinter (no se usa, pero Tkinter lo manda siempre).
        """
        opcion = self.combo_libro.get().strip()

        #? .get(clave) devuelve el libro asociado a ese texto, o None si el texto no esta en el diccionario
        libro = self.opciones_libros.get(opcion)

        #* Si el texto no corresponde a ningun libro, no hay libro seleccionado
        if libro is None:
            self.libro_seleccionado = None
            return

        self.libro_seleccionado = libro

        self.lbl_libro_seleccionado.config(
            text=(
                f"Libro: {libro['titulo']} - "
                f"{int(libro['disponibles'])} disponibles"
            ),
            bg="#d9f2d9"
        )

    def agregar_libro(self):
        """Agrega el libro elegido (con su cantidad) a la lista de libros del prestamo.

        Se ejecuta con el boton "Agregar libro". Valida en este orden:
            1. Que haya un libro seleccionado.
            2. Que el texto del combo siga siendo el de ese libro.
            3. Que la cantidad sea un entero mayor que cero y no supere los disponibles.
            4. Que el libro no este agregado ya.
        Si todo esta bien, lo guarda en memoria y en la tabla, y deja el formulario listo para otro libro.
        """
        libro = self.libro_seleccionado

        #*-- 1. Tiene que haber un libro elegido
        if not libro:
            messagebox.showwarning(
                "Atención",
                "Primero seleccioná un libro."
            )
            return

        # Evitar agregar un título distinto del seleccionado
        #? "is not" compara si son EXACTAMENTE el mismo objeto (no solo si valen lo mismo).
        #? Sirve para detectar que el usuario cambio el texto del combo despues de elegir un libro.
        if self.opciones_libros.get(
            self.combo_libro.get().strip()
        ) is not libro:
            messagebox.showwarning(
                "Atención",
                "Seleccioná nuevamente el libro."
            )
            return

        #*-- 3. Validamos la cantidad
        try:
            #? int() lanza ValueError si lo escrito no es un numero entero
            cantidad = int(self.cantidad_libro.get())

            #? Lanzamos ValueError a proposito para que lo atrape el mismo except de abajo
            if cantidad <= 0:
                raise ValueError

            #? No se pueden prestar mas ejemplares de los que hay disponibles
            if cantidad > libro["disponibles"]:
                messagebox.showwarning(
                    "Sin disponibilidad suficiente",
                    f"Solo hay {int(libro['disponibles'])} "
                    "ejemplares disponibles de este libro."
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Cantidad inválida",
                "Ingresá una cantidad entera mayor que cero."
            )
            return

        id_libro = libro["id_libro"]

        #*-- 4. Un mismo libro no se puede agregar dos veces (en la base la clave de detalle_prestamo es id_prestamo + id_libro)
        if id_libro in self.libros_seleccionados:
            messagebox.showwarning(
                "Libro repetido",
                "Este libro ya está agregado. "
                "Quitalo si querés cambiar su cantidad."
            )
            return

        # Guardar la selección en memoria
        self.libros_seleccionados[id_libro] = {
            "titulo": libro["titulo"],
            "cantidad": cantidad
        }

        # Mostrarla en el Treeview
        #? iid es el identificador de la fila. Usamos el id del libro asi, cuando se
        #? selecciona una fila para quitarla, recuperamos el id directamente de la seleccion.
        self.tabla_libros.insert(
            "",
            "end",
            iid=str(id_libro),
            values=(libro["titulo"], cantidad)
        )

        # Preparar el formulario para otro libro
        self.combo_libro.set("") #* Vacia el combo
        self.libro_seleccionado = None
        self.cantidad_libro.delete(0, tk.END)
        self.cantidad_libro.insert(0, "1") #* Vuelve la cantidad a 1

        self.lbl_libro_seleccionado.config(
            text="Ningún libro seleccionado",
            bg="#f0f0f0"
        )

    def quitar_libro(self):
        """Quita de la lista del prestamo el libro seleccionado en la tabla.

        Se ejecuta con el boton "Quitar seleccionado". Lo borra de la tabla y del
        diccionario en memoria.
        """
        seleccion = self.tabla_libros.selection()

        if not seleccion:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un libro para quitarlo."
            )
            return

        #? seleccion[0] es el iid de la fila, que al agregar el libro se definio como str(id_libro).
        #? Lo pasamos a int porque las claves del diccionario son numeros.
        id_libro = int(seleccion[0])

        #? .pop(clave, None) borra la clave del diccionario; el None evita un error si no existiera
        self.libros_seleccionados.pop(id_libro, None)
        self.tabla_libros.delete(seleccion[0])

    def confirmar_prestamo(self):
        """Valida todo el formulario y registra el prestamo en la base de datos.

        Se ejecuta con el boton "Confirmar Préstamo". Valida en este orden:
            1. Que haya un socio elegido y que el DNI del combo siga siendo el elegido.
            2. Que haya al menos un libro agregado.
            3. Que la fecha de devolucion tenga formato valido y sea igual o posterior a hoy.
        Despues guarda el prestamo, avisa el resultado y vuelve al listado.
        """
        #*-- 1. Validamos el socio
        if not self.socio_seleccionado:
            messagebox.showwarning(
                "Atención",
                "Seleccioná un socio."
            )
            return

        #? Si despues de elegir el socio el usuario cambio el texto del combo, el DNI ya no coincide y hay que elegirlo de nuevo
        if self.combo_dni_socio.get().strip() != self.socio_seleccionado:
            messagebox.showwarning(
                "Atención",
                "Volvé a seleccionar un socio válido."
            )
            return

        #*-- 2. Tiene que haber al menos un libro en el prestamo
        if not self.libros_seleccionados:
            messagebox.showwarning(
                "Atención",
                "Agregá al menos un libro al préstamo."
            )
            return

        # Validar la fecha
        try:
            #? strptime convierte el texto a fecha segun el formato "%d/%m/%Y" (dia/mes/año).
            #? Si el texto no tiene ese formato (ej: sigue el "dd/mm/aaaa" de ejemplo) lanza ValueError.
            fecha_devolucion = datetime.strptime(
                self.entry_fecha_devolucion.get().strip(),
                "%d/%m/%Y"
            ).date()

            #? La fecha no puede ser anterior a hoy. Se lanza ValueError a proposito para usar el mismo except.
            #? Es la misma regla que el CHECK de la base: devolucion estimada >= fecha de prestamo.
            if fecha_devolucion < date.today():
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Fecha inválida",
                "Ingresá una fecha válida igual o posterior a hoy."
            )
            return

        # Preparar los datos para el repositorio
        #? List comprehension: convierte el diccionario {id_libro: {...}} en una lista de
        #? tuplas (id_libro, cantidad), que es el formato que recibe el repositorio.
        libros = [
            (id_libro, datos["cantidad"])
            for id_libro, datos in self.libros_seleccionados.items()
        ]

        #*-- Guardamos en la base. Devuelve el ID del prestamo nuevo.
        try:
            id_prestamo = self.ApiPrestamos.crear_prestamo_multiple(
                dni_socio=self.socio_seleccionado,
                libros=libros,
                fecha_devolucion=fecha_devolucion
            )

        #? Atrapa cualquier error (ej: problema con la base, o que el socio ya tenga un prestamo activo,
        #? que la base rechaza con su indice unico) y lo muestra, para que el programa no se cierre.
        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo registrar el préstamo: {error}"
            )
            return

        messagebox.showinfo(
            "Préstamo registrado",
            f"El préstamo {id_prestamo} se registró correctamente."
        )

        #? Reutilizamos cancelar() solo para volver al listado de prestamos
        self.cancelar()

    def cancelar(self):
        """Vuelve al listado de prestamos (boton "Cancelar", y tambien despues de registrar uno)."""
        #? El import esta aca adentro y no arriba del archivo, seguramente para evitar un
        #? "import circular" (GestionPrestamos tambien importa a esta pantalla).
        from views.prestamos_views.gestion_prestamos_view import GestionPrestamos
        self.controller.show_frame(GestionPrestamos)