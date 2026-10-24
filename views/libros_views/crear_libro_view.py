"""Pantalla para crear o modificar un libro de LibManage.

Tiene dos paneles:
    - Izquierda: formulario con los datos del libro (titulo, autor, año, cantidad e ISBN).
    - Derecha: resultados de buscar el titulo en una API externa (Open Library),
      para autocompletar el formulario con doble click.

Se usa en dos modos:
    - Crear: se abre sin datos (libro_datos=None) y el formulario arranca vacio.
    - Modificar: se abre con un diccionario de un libro existente (libro_datos)
      y aparece el boton "Dar de baja".
"""

import tkinter as tk
from tkinter import ttk, messagebox
from views.components.base_frame import BaseFrame
from views.components.formulario_desplazable import FormularioDesplazable
from api_libros.open_library import LibraryApi

class CrearLibro(BaseFrame):
    """Pantalla con el formulario para crear un libro nuevo o modificar uno existente."""

    def __init__(self, parent, controller, libro_datos=None):
        """Arma toda la pantalla: formulario, panel de busqueda, tabla y botones.

        Args:
            parent: Frame contenedor donde se dibuja esta pantalla (el container de MainWindow).
            controller: La ventana principal (MainWindow). Se usa para cambiar de pantalla.
            libro_datos (dict | None): Datos del libro a modificar (necesita la clave "id_libro").
                Si es None, la pantalla funciona en modo "crear".
        """
        super().__init__(parent, controller)
        self.controller = controller #* Guardamos la ventana principal para poder volver al listado despues
        self.libro_datos = libro_datos or {} #? Si viene None lo cambiamos por {} asi despues "if self.libro_datos" da False (modo crear)
        self.api_busqueda = LibraryApi() #* Objeto que busca libros en la API externa
        self.docs = [] #* Aca se guardan los resultados completos de la ultima busqueda (se usan al elegir uno)

        #*-- Distribucion general de la pantalla
        self.columnconfigure(0, weight=1) #* La unica columna se estira a lo ancho
        self.rowconfigure(1, weight=1) #? La fila 1 (donde va el formulario) se estira a lo alto cuando se agranda la ventana
        self.crear_titulo("Crear Libro")

        #? FormularioDesplazable es un contenedor con scroll: lo que queramos que se pueda
        #? desplazar se pone dentro de su atributo .contenido
        self.scroll_formulario = FormularioDesplazable(self)
        self.scroll_formulario.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        #* Frame principal con borde: adentro van el formulario (izquierda) y la busqueda (derecha)
        self.frame_central = tk.Frame(self.scroll_formulario.contenido, bd=1, relief="solid", padx=20, pady=20)
        self.frame_central.pack(fill="both", expand=True)
        #? uniform="columnas" obliga a que las dos columnas midan exactamente lo mismo (mitad y mitad)
        self.frame_central.columnconfigure((0, 1), weight=1, uniform="columnas")
        self.frame_central.rowconfigure(0, weight=1)

        #*-- Panel izquierdo: formulario
        self.frame_formulario = tk.Frame(self.frame_central)
        self.frame_formulario.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        #? campos (clave, etiqueta, placeholder, fila)
        #? Las filas van de a 2 (0, 2, 4...) porque cada campo usa una fila para la etiqueta
        #? y la siguiente (fila + 1) para el cuadro de texto.
        campos = [
            ("titulo", "Título", "Título del Libro", 0),
            ("autor", "Autor", "Autor", 2),
            ("anio", "Año", "Año", 4),
            ("cantidad", "Cantidad Total", "Cantidad total", 6),
            ("isbn", "ISBN", "ISBN", 8),
        ]

        #? Diccionario {clave: cuadro de texto}. Con el for creamos los 5 campos sin repetir codigo.
        self.entradas = {}
        for clave, texto_label, placeholder, fila in campos:
            self.crear_etiqueta(texto_label, fila)
            entrada = self.crear_campo(placeholder, fila + 1)
            self.entradas[clave] = entrada

        # Alias para mantener compatibilidad con métodos existentes
        #? Son nombres cortos para usar los campos en el resto de la clase (self.txt_titulo.get(), etc.)
        self.txt_titulo = self.entradas["titulo"]
        self.txt_autor = self.entradas["autor"]
        self.txt_anio = self.entradas["anio"]
        self.txt_cantidad = self.entradas["cantidad"]
        self.txt_isbn = self.entradas["isbn"]

        # Botón de búsqueda de libro integrado junto al campo de título
        #? row=1, column=1: la fila 1 es la del cuadro de titulo, y la columna 1 lo deja a su derecha
        self.btn_buscar = tk.Button(self.frame_formulario, text="Buscar Libro", command=self.buscar_libro)
        self.btn_buscar.grid(row=1, column=1, padx=5, pady=4, ipady=4)

        #*-- Panel derecho: resultados de la busqueda
        self.frame_api = tk.Frame(self.frame_central, bd=1, relief="solid")
        self.frame_api.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.frame_api.rowconfigure(1, weight=1) #* La fila de la tabla es la que se estira
        self.frame_api.columnconfigure(0, weight=1)

        #* Mensaje de estado de la busqueda (cambia a "Buscando...", "No se encontraron...", etc.)
        self.lbl_busqueda = tk.Label(self.frame_api, text="Los Resultados se listarón debajo", justify="center")
        self.lbl_busqueda.grid(row=0, column=0, columnspan=2, pady=6)

        # Configuración del Treeview
        #? Cada columna: clave -> (texto del encabezado, ancho en pixeles, alineacion)
        #? Alineacion: "center" = centrado, "w" = izquierda (west)
        columnas = {
            "id": ("ID", 60, "center"),
            "titulo": ("Título", 250, "w"),
            "autor": ("Autor", 200, "w"),
            "año": ("Año", 80, "center")
        }

        self.tabla = ttk.Treeview(
            self.frame_api,
            columns=tuple(columnas.keys()), #* Pasa solo los nombres de las columnas
            show="headings", #? "headings" muestra los encabezados y oculta la columna extra "#0" del arbol
            selectmode="browse", #? "browse" = se puede seleccionar una sola fila a la vez
            style="Prestamos.Treeview" #* Estilo definido aparte (se reutiliza el de la tabla de prestamos)
        )

        for col, (texto, ancho, fija) in columnas.items():
            self.tabla.heading(col, text=texto) #* Pone el texto del encabezado
            #? "fija" en realidad es la alineacion del texto (anchor). stretch=False = ancho fijo.
            self.tabla.column(col, width=ancho, minwidth=60, stretch=False, anchor=fija)

        # Scrollbars
        #? El scroll se conecta en los dos sentidos:
        #?   - command=...yview -> al mover la barra, se mueve la tabla
        #?   - yscrollcommand=sb_y.set -> al mover la tabla (ej: con la rueda), se mueve la barra
        sb_y = ttk.Scrollbar(self.frame_api, orient="vertical", command=self.tabla.yview)
        sb_x = ttk.Scrollbar(self.frame_api, orient="horizontal", command=self.tabla.xview)
        self.tabla.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

        self.tabla.grid(row=1, column=0, sticky="nsew")
        sb_y.grid(row=1, column=1, sticky="ns") #* Barra vertical a la derecha de la tabla
        sb_x.grid(row=2, column=0, sticky="ew") #* Barra horizontal abajo de la tabla

        #? "<Double-1>" = doble click con el boton izquierdo. El lambda recibe el evento (e)
        #? pero no lo usa, solo llama a la funcion que carga el libro elegido.
        self.tabla.bind("<Double-1>", lambda e: self.seleccionar_libro_tree())

        #*-- Botones de abajo (ocupan las dos columnas de frame_central)
        self.frame_botones = tk.Frame(self.frame_central)
        self.frame_botones.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(15, 0))

        #? 3 columnas iguales: izquierda = Guardar, medio = Dar de baja, derecha = Cancelar
        for i in range(3):
            self.frame_botones.columnconfigure(i, weight=1)

        #? Las "\" al final de la linea solo parten la instruccion en dos renglones, es un solo tk.Button(...).grid(...)
        tk.Button(self.frame_botones, text="Guardar Cambios", command=self.guardar_cambios)\
            .grid(row=0, column=0, padx=5, ipady=3, sticky="ew")

        tk.Button(self.frame_botones, text="Cancelar y volver atrás", command=self.descartar)\
            .grid(row=0, column=2, padx=5, ipady=3, sticky="ew")

        #? Solo en modo "modificar" (cuando hay libro_datos) aparece el boton para dar de baja el libro
        if self.libro_datos:
            tk.Button(self.frame_botones, text="Dar de baja", command=self.eliminar_libro)\
                .grid(row=0, column=1, padx=5, ipady=3, sticky="ew")

    def crear_etiqueta(self, texto, fila):
        """Crea una etiqueta (texto fijo) arriba de un campo del formulario.

        Args:
            texto (str): Texto que muestra la etiqueta. Ej: "Título".
            fila (int): Fila de la grilla de frame_formulario donde se coloca.

        Returns:
            tk.Label: La etiqueta ya creada y ubicada.
        """
        label = tk.Label(self.frame_formulario, text=texto, justify="center", width=30)
        label.grid(row=fila, column=0, pady=2)
        return label

    def crear_campo(self, placeholder, fila):
        """Crea un cuadro de texto con "placeholder" (texto de ejemplo que se borra al escribir).

        Tkinter no trae placeholders, asi que se simulan:
            - Al crear el campo se inserta el texto de ejemplo.
            - Al hacer click (FocusIn): si el texto es el de ejemplo, se borra.
            - Al salir del campo (FocusOut): si quedo vacio, se vuelve a poner el de ejemplo.

        Args:
            placeholder (str): Texto de ejemplo que se muestra mientras el campo esta vacio.
            fila (int): Fila de la grilla de frame_formulario donde se coloca.

        Returns:
            tk.Entry: El cuadro de texto ya creado y ubicado.
        """
        entry = tk.Entry(self.frame_formulario, justify="center", width=30)
        entry.insert(0, placeholder) #* Arranca mostrando el texto de ejemplo
        entry.grid(row=fila, column=0, pady=4, ipady=4)

        #? Estos lambda son un "if" en una linea: "hacer A si se cumple la condicion, si no, no hacer nada (None)"
        entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END) if entry.get() == placeholder else None)
        entry.bind("<FocusOut>", lambda e: entry.insert(0, placeholder) if not entry.get().strip() else None)
        return entry

    def actualizar_treeview(self, datos_libros):
        """Limpia y carga las filas en la tabla del Treeview.

        Args:
            datos_libros (list[dict]): Libros a mostrar. Cada dict puede tener las
                claves "id", "titulo", "autor" y "año". Si falta alguna, se muestra vacia.
        """
        #*-- Primero se borran las filas anteriores
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        #*-- Despues se agrega una fila por cada libro
        for libro in datos_libros:
            #? .get("clave", "") devuelve el valor, o "" si la clave no existe (evita errores)
            #? "" = sin padre (fila de primer nivel), "end" = la agrega al final
            self.tabla.insert("", "end", values=(
                libro.get("id", ""),
                libro.get("titulo", ""),
                libro.get("autor", ""),
                libro.get("año", "")
            ))

    def set_entry(self, entry, valor):
        """Reemplaza el texto de un cuadro de texto, solo si el valor nuevo no esta vacio.

        Args:
            entry (tk.Entry): Cuadro de texto a modificar.
            valor: Valor a escribir (se convierte a texto con str()).
        """
        if valor: #? Si el valor viene vacio no tocamos el campo (asi no se pierde lo que ya estaba)
            entry.delete(0, tk.END) #* Borra el contenido actual (de la posicion 0 hasta el final)
            entry.insert(0, str(valor)) #* Escribe el valor nuevo

    def cargar_datos(self, datos):
        """Rellena el formulario con los datos de un libro (titulo, autor, ISBN y año).

        No carga la cantidad: ese dato lo ingresa el usuario a mano.

        Args:
            datos (dict): Datos del libro, con las claves "titulo", "autor", "isbn" y "año".
        """
        self.set_entry(self.txt_titulo, datos.get("titulo", ""))
        self.set_entry(self.txt_autor, datos.get("autor", ""))
        self.set_entry(self.txt_isbn, datos.get("isbn", ""))
        self.set_entry(self.txt_anio, datos.get("año", ""))

    def buscar_libro(self):
        """Busca en la API el titulo escrito en el formulario y muestra los resultados en la tabla.

        Se ejecuta al apretar el boton "Buscar Libro".
        """
        titulo = self.txt_titulo.get().strip() #? .strip() saca los espacios de adelante y atras
        #? No se busca si esta vacio o si todavia tiene el texto de ejemplo
        if not titulo or titulo == "Título del Libro":
            messagebox.showwarning("Atención", "Ingresa un título para buscar.")
            return #* Corta la funcion aca

        self.lbl_busqueda.config(text=f"Buscando: {titulo}") #* Avisa que esta buscando
        resultado = self.api_busqueda.buscar_titulo(titulo)

        if not resultado: #* Si no volvio nada, limpiamos la tabla y avisamos
            self.lbl_busqueda.config(text="No se encontraron libros.")
            self.actualizar_treeview([])
        else:
            #? El resultado trae 2 cosas: la lista resumida para mostrar en la tabla (datos_libros)
            #? y los resultados completos (docs), que guardamos para usarlos cuando se elija un libro.
            datos_libros, self.docs = resultado
            self.lbl_busqueda.config(text=f"Resultados para: {titulo}")
            self.actualizar_treeview(datos_libros)

    def seleccionar_libro_tree(self):
        """Carga en el formulario el libro elegido en la tabla (se ejecuta con doble click)."""
        seleccion = self.tabla.selection() #* Devuelve las filas seleccionadas
        if not seleccion: #* Si no hay ninguna seleccionada, no hacemos nada
            return
        #? .item(...)["values"] devuelve los valores de la fila; el [0] es la primera columna (el ID)
        id_libro = self.tabla.item(seleccion[0])["values"][0]
        #? Con el ID buscamos en los resultados guardados (self.docs) los datos completos de ese libro
        datos = self.api_busqueda.funcion_final(id_libro, self.docs)
        self.cargar_datos(datos)


    def guardar_cambios(self):
        """Valida los datos del formulario y guarda el libro (lo crea o lo modifica).

        Se ejecuta al apretar "Guardar Cambios". Pasos:
            1. Lee los campos.
            2. Valida que titulo y autor esten completos.
            3. Valida que año y cantidad sean numeros validos.
            4. Guarda: modifica si hay libro_datos (modo modificar), si no crea uno nuevo.
            5. Avisa el resultado y vuelve al listado.
        """
        #*-- 1. Leemos los campos
        titulo = self.txt_titulo.get()
        autor = self.txt_autor.get().strip()
        anio = self.txt_anio.get().strip()
        cantidad = self.txt_cantidad.get().strip()
        isbn = self.txt_isbn.get().strip()

        #*-- 2. Titulo y autor son obligatorios: no pueden estar vacios ni con el texto de ejemplo (placeholder)
        if titulo in ("", "Titulo del Libro") or autor in ("", "Autor"):
            messagebox.showwarning(
                "Datos incompletos",
                "El título y el autor son obligatorios."
            )
            return

        #*-- 3. Validamos año y cantidad
        try:
            #? El año es opcional: si esta vacio (o con el placeholder) queda en None (NULL en la base).
            #? Si tiene algo, int() lo pasa a numero; si no es un numero, int() lanza ValueError.
            anio = None if anio in ("", "Año") else int(anio)
            cantidad = int(cantidad)

            #? Año no puede ser 0 ni negativo, y la cantidad no puede ser negativa.
            #? Lanzamos ValueError a proposito para que lo atrape el mismo except de abajo
            #? y se muestre un solo mensaje para todos los casos de datos invalidos.
            if (anio is not None and anio <= 0) or cantidad < 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Datos inválidos",
                "Ingresá un año válido y una cantidad entera no negativa."
            )
            return

        #*-- 4. Guardamos en la base de datos
        try:
            if self.libro_datos: #* Modo modificar: actualiza el libro que ya existe
                self.ApiLibros.actualizar_libro(
                    self.libro_datos["id_libro"], #* ID del libro que se esta editando
                    titulo,
                    autor,
                    anio,
                    cantidad,
                    isbn
                )
                mensaje = "Libro modificado correctamente."
            else: #* Modo crear: inserta un libro nuevo y recibe el ID que le asigno la base
                nuevo_id = self.ApiLibros.crear_libro(titulo, autor, anio, cantidad, isbn)
                mensaje = f"Libro creado correctamente con ID {nuevo_id}."

        except Exception as error: #? Atrapa cualquier error (ej: problema con la base) y lo muestra, para que el programa no se cierre
            messagebox.showerror(
                "Error al guardar",
                f"No se pudo guardar el libro: {error}"
            )
            return

        #*-- 5. Avisamos que salio bien y volvemos al listado
        messagebox.showinfo("Operación exitosa", mensaje)
                # Regresar al listado
        #? El import esta aca adentro y no arriba del archivo, seguramente para evitar un
        #? "import circular" (GestionLibros tambien importa a esta pantalla).
        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)

    def descartar(self):
        """Avisa que se descarto el libro y vuelve al listado (boton "Cancelar y volver atrás")."""
        messagebox.showinfo(title="Libro Descartado", message="Libro descartado exitosamente.\nVolviendo atrás...")
        self.volver()

    def volver(self):
        """Vuelve a la pantalla de gestion de libros."""
        #? Import dentro de la funcion por el mismo motivo que en guardar_cambios (evitar import circular)
        from views.libros_views.gestion_libros_view import GestionLibros
        self.controller.show_frame(GestionLibros)