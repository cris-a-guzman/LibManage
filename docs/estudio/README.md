# LibManage: guía para estudiar el código

> Esta rama es un recurso colectivo de aprendizaje elaborado con asistencia de IA. Parte de `main` y agrega únicamente comentarios y documentación: no es una nueva entrega académica ni propone integrar cambios funcionales.

## Qué problema resuelve LibManage

LibManage es una aplicación de escritorio para la gestión interna de una biblioteca pequeña. Su objetivo documentado es organizar el catálogo, los socios, los préstamos, las devoluciones, la disponibilidad de ejemplares y el historial. La interfaz está construida con Tkinter, el código de acceso a datos está separado en repositorios y la persistencia usa MySQL.

La documentación vigente del ABP distingue cuatro conjuntos de datos relacionados: `socio`, `libro`, `prestamo` y `detalle_prestamo`. Este último representa la relación muchos-a-muchos entre préstamos y libros y conserva la cantidad de ejemplares incluida en cada operación.

## Estado de las ramas al iniciar este recurso

Verificación realizada el 23/10/2026 sobre GitHub:

- `main` es la versión principal y se tomó como origen en el commit [`daa29a2`](https://github.com/cris-a-guzman/LibManage/commit/daa29a2454d5a7cd15703638a0847a4de1e47070).
- `database` fue integrada por el [PR #32](https://github.com/cris-a-guzman/LibManage/pull/32). Su punta estaba 11 commits adelante y 23 detrás de `main`: conserva una historia divergente y sus commits exclusivos no se interpretan por sí solos como trabajo pendiente.
- `interfaz` fue integrada por el [PR #45](https://github.com/cris-a-guzman/LibManage/pull/45); su punta estaba 5 commits detrás, 0 adelante y es ancestro de `main`.
- `poc-api` parte del `main` verificado y agrega nueve commits experimentales, sin commits detrás en la comparación observada. No forma parte de la versión principal. Véase [Análisis de la API experimental](api-experimental.md).

## Mapa de carpetas y responsabilidades

| Ruta | Responsabilidad en la versión principal |
|---|---|
| `main.py` | Punto de entrada: crea la ventana principal e inicia el bucle de eventos. |
| `views/components/` | Componentes reutilizables de interfaz y navegación entre pantallas. |
| `views/home_view/` | Panel inicial y resumen de cantidades. |
| `views/libros_views/` | Listado, búsqueda, creación, modificación y baja lógica de libros. |
| `views/prestamos_views/` | Listado, filtros, registro y devolución de préstamos. |
| `views/socio_views/` | Listado de socios e historial; parte del alta/modificación aún funciona como maqueta. |
| `repositories/` | Acceso a MySQL: conexión, consultas y escrituras para libros, socios y préstamos. |
| `database/` | Esquema, restricciones, roles, plantilla de cuentas y datos de prueba. |

`MainWindow` actúa como controlador de navegación: elimina la pantalla actual y crea la siguiente dentro de un contenedor común. `BaseFrame` aporta estructura visual, acceso a los repositorios y controles repetidos. Las pantallas concretas heredan de esa clase y coordinan la interacción con el usuario.

## Orden recomendado para estudiar el código

1. `main.py`: observar el punto de entrada y `mainloop()`.
2. `views/components/main_window.py`: seguir cómo se cambia de pantalla.
3. `views/components/base_frame.py`: reconocer herencia, atributos compartidos y composición de widgets.
4. `repositories/conexion.py` y `repositories/base_repository.py`: entender conexión, cursor, parámetros, `commit()` y `rollback()`.
5. `database/01_schema.sql`: relacionar tablas, claves y restricciones con el dominio bibliotecario.
6. `repositories/libro_repo.py` y `views/libros_views/`: recorrer un CRUD relativamente acotado.
7. `repositories/prestamo_repo.py` y `views/prestamos_views/registrar_prestamo_view.py`: estudiar validaciones, disponibilidad y transacciones.
8. `repositories/socio_repo.py` y `views/socio_views/`: comparar lo implementado con las pantallas que todavía son parciales.
9. [Análisis de la API experimental](api-experimental.md): recién después de comprender `main`, estudiar la prueba de concepto sin confundirla con la aplicación principal.

## Recorrido de una operación: registrar un préstamo

1. `RegistrarPrestamo.__init__()` solicita al repositorio los DNI vigentes y la disponibilidad calculada de los libros.
2. La pantalla construye diccionarios en memoria para relacionar cada opción visible con el registro recuperado de MySQL.
3. Los eventos `<<ComboboxSelected>>` guardan el socio y el libro seleccionados. `agregar_libro()` valida una cantidad positiva, disponibilidad suficiente y que el título no esté repetido.
4. `confirmar_prestamo()` valida que existan socio, libros y una fecha estimada igual o posterior al día actual; luego transforma el diccionario de selección en una lista de tuplas `(id_libro, cantidad)`.
5. `PrestamoRepo.crear_prestamo_multiple()` vuelve a validar los datos, inicia una transacción, busca y bloquea el socio y los libros, calcula las unidades ocupadas, crea la cabecera en `prestamo` y agrega los renglones en `detalle_prestamo`.
6. Si todas las escrituras terminan correctamente ejecuta `commit()`. Ante cualquier excepción ejecuta `rollback()`, propaga el error y la interfaz lo informa con un cuadro de diálogo.

Este recorrido conecta interfaz dirigida por eventos, colecciones de Python, funciones, excepciones, reglas de negocio, consultas parametrizadas, relaciones entre tablas y atomicidad de una transacción.

## Reglas de negocio

La fuente de requisitos consultada fue [Copia de LibManage - Recuperatorio Evidencia 5 - Módulo Programador](https://docs.google.com/document/d/1EbcEGX2SjCZjlO-76Wthm9F5aoW_ux6fXSX2yk_euJE/edit), especialmente las secciones **Reglas de negocio**, **Entidades del sistema** y **Diccionario de datos normalizado**.

| Regla documentada | Código relacionado | Estado observado |
|---|---|---|
| Un préstamo pertenece a un socio y contiene uno o varios libros. | `prestamo.id_socio`, `detalle_prestamo`, `crear_prestamo_multiple()` | Implementada en el esquema y en el alta principal. |
| La cantidad incluida debe ser mayor que cero. | `chk_detalle_cantidad`, `agregar_libro()`, `crear_prestamo_multiple()` | Validada en interfaz, repositorio y base. |
| Solo se presta cuando alcanza la disponibilidad. | `obtener_disponibilidad_libros()` y `crear_prestamo_multiple()` | Se calcula y se vuelve a comprobar dentro de la transacción. |
| Los estados válidos son activo, devuelto y cerrado sin devolver. | `chk_prestamo_estado`, consultas de disponibilidad y devolución | El esquema los contempla; la interfaz principal solo permite registrar activo y pasar de activo a devuelto. |
| Un socio puede mantener un único préstamo activo. | Índice `uq_prestamo_socio_activo` | La restricción está en MySQL; el repositorio no presenta una validación previa con mensaje específico. |
| Las bajas de libros y socios deben ser lógicas. | `LibroRepo.dar_baja_libro()` y columnas `fecha_baja` | Implementada para libros. La pantalla de socios no persiste altas, cambios ni bajas. |
| No dar de baja un libro o socio con préstamo activo. | Documento ABP | No se observa una comprobación equivalente en `dar_baja_libro()`; la baja de socios no está implementada. |
| Hasta diez libros distintos por préstamo. | Documento ABP | No se observa el límite en la interfaz, el repositorio ni el esquema. |
| La devolución es total, sin devoluciones parciales. | `devolver_prestamo()` actualiza la cabecera completa | Coherente con el comportamiento implementado. |

Los estados anteriores describen el código de `main` al crear esta rama. Una regla documentada no se considera implementada sólo por aparecer en el ABP o en el esquema.

## Mapa de conceptos y bibliografía

Las páginas indicadas para los PDF son las que figuran en el índice interno del propio material. Los documentos de Google sin paginación estable se identifican por sección.

### Programación modular

| Concepto académico | Fuente institucional verificada | Aparición en LibManage |
|---|---|---|
| Módulo, importación y punto de entrada | Programación I, [Funciones avanzadas y módulos](https://drive.google.com/file/d/10aLioLGfg_LnqZa0ZH7USvt6JugWPEBc/view), **Módulos** (p. 2), **Programación modular** (p. 4) y explicación de `__main__` (p. 6). | `main.py`, importaciones entre `views/` y `repositories/`. |
| Funciones, parámetros y retorno | Programación I, [Python. Introducción](https://drive.google.com/file/d/1_o7PcansHQR1j36Tw2rwy4VCkTeCG_Lc/view), **Funciones** (pp. 72-77). | Métodos de vistas y repositorios; valores retornados por consultas y escrituras. |
| Condicionales, bucles y colecciones | Mismo material, **Estructuras de control** (pp. 37-56) y **Estructuras de datos** (pp. 57-67). | Validaciones con `if`, recorridos de filas, listas, tuplas y diccionarios de selección. |
| Manejo de excepciones | Mismo material, **Manejo de excepciones** (pp. 68-71). | `try/except/finally` de conexión, escrituras, transacciones e interfaz. |

### Programación orientada a objetos

| Concepto académico | Fuente institucional verificada | Aparición en LibManage |
|---|---|---|
| Objetos, clases, instancias, atributos y métodos | Programación I, [POO. Fundamentos](https://drive.google.com/file/d/1T6vr8DepNkH0nefT0LFnNnGXVCQiKjPX/view), **Objetos** (p. 4), **Clases** (p. 6), **Clases e instancias en Python** (pp. 7-10). | `MainWindow`, `BaseFrame`, vistas, repositorios y widgets instanciados. |
| Herencia y asociación | Mismo material, **Herencia** (pp. 19-28) y **Asociación** (p. 32). | Vistas que heredan de `BaseFrame`; cada vista conserva referencias al controlador y a repositorios. |
| UML y relaciones entre clases | Programación I, [POO. Modelado](https://drive.google.com/file/d/167C3dkif_4Aiq_ggVH_xOpI9Ym_W6diS/view), **Diagrama de clases** (p. 3), **Relaciones entre clases** (p. 8) y **Relación entre clases y objetos** (p. 16). | Organización `MainWindow` -> vistas -> repositorios -> conexión. No se atribuye al proyecto un patrón formal que el código no demuestre. |

### Tkinter y programación dirigida por eventos

| Concepto académico | Fuente institucional verificada | Aparición en LibManage |
|---|---|---|
| Ventana, `mainloop`, geometría y widgets | Programación I, [Tkinter - Elementos, widgets y configuraciones](https://docs.google.com/document/d/1_-8J29ahj2cHIpIp_qHEGT4RKL-bfPSB1To_1_yYlUU/edit), secciones 1 a 9. | `main.py`, `MainWindow`, `BaseFrame`, `Frame`, `Entry`, `Button`, `Treeview`, `Canvas` y `Scrollbar`. |
| Eventos, `bind` y callbacks | Programación I, [Eventos en Tkinter](https://docs.google.com/document/d/1rWseXXTyjJOjQgviNmR5ZMmzmUh8TO-G/edit), secciones 1, 2, 5, 6, 9 y 14. | Selección de filas, foco, Enter, doble clic, selección de `Combobox` y funciones `command`. |

### Persistencia y CRUD

| Concepto académico | Fuente institucional verificada | Aparición en LibManage |
|---|---|---|
| Persistencia y conexión a MySQL | Programación I, [POO. Acceso a datos](https://drive.google.com/file/d/17zuW5msMQfKQ_3CLy1Z4O6xYrLBbPRJp/view), **Persistencia** (p. 2), **Conexión a base de datos** (p. 3) y **Conexión a MySQL** (p. 5). | `repositories/conexion.py` y variables de entorno. |
| Operaciones CRUD | Mismo material, **Operaciones CRUD básicas** (pp. 10-16). | `LibroRepo` implementa lectura, alta, actualización y baja lógica mediante `UPDATE`; socios solo tienen lecturas en el repositorio de `main`. |
| Capa de acceso a datos y DAO | Mismo material, **Data Access Object (DAO)** y componentes (pp. 18-24). | `repositories/` separa las consultas de las vistas. Se usa la comparación pedagógica con DAO, sin afirmar que toda la implementación cumpla formalmente el patrón. |
| Consultas parametrizadas y transacciones | Programación I, [Manual CRUD y bases de datos](https://docs.google.com/document/d/1G2Wu9Cj0xozGsq7B3UIGX4WLzeXo0Dvs/edit), secciones 7 y 12. | Marcadores `%s`, tuplas de parámetros, `commit()` y `rollback()`. Material docente complementario. |

### Modelo relacional y SQL

| Concepto académico | Fuente institucional verificada | Aparición en LibManage |
|---|---|---|
| Entidades, relaciones y modelo lógico | Base de Datos, [Bases de Datos](https://drive.google.com/file/d/1EDxa-6VLLIiLemf_3WK3sQ6ebi1meZX8/view), **Diseño conceptual** (p. 8), **Diagrama Entidad-Relación** (p. 9) y **Diseño lógico** (p. 11). | Tablas `socio`, `libro`, `prestamo` y tabla asociativa `detalle_prestamo`. |
| Claves primarias, foráneas y relación N:M | Mismo material, transformación al modelo relacional (pp. 12-13). | Claves simples en tres tablas y clave primaria compuesta en `detalle_prestamo`; restricciones `FOREIGN KEY`. |
| Normalización | Mismo material, **Normalización** y formas normales (pp. 15-19). | Separación de socios, libros, préstamos y detalles; la rama no vuelve a auditar la normalización del ABP. |
| SQL, cláusulas y agregaciones | Mismo material, **¿Qué es SQL?** (p. 21), **Cláusulas** (p. 44), **Funciones de agregación** (p. 45) y **Subconsultas** (p. 46). | `SELECT`, `INSERT`, `UPDATE`, `JOIN`, `LEFT JOIN`, `GROUP BY`, `COUNT`, `SUM`, `COALESCE` y `GROUP_CONCAT`. |
| MySQL y restricciones físicas | Base de Datos, [Clase 15 - MySQL](https://drive.google.com/file/d/1VTYSCv-MsnvD7Bfx1C0obmLqShoMieQe/view), secciones **CREATE DATABASE**, **CREATE TABLE** y operaciones SQL. | `database/01_schema.sql`, tipos, `CHECK`, `UNIQUE`, índices e InnoDB. Material de clase complementario. |

### Reglas de negocio

La correspondencia Código -> necesidad del sistema se centraliza en la tabla de [Reglas de negocio](#reglas-de-negocio). La fuente del proyecto es el documento vigente del ABP, no una inferencia a partir del código.

## Ejecución básica verificada documentalmente

1. Preparar MySQL 8.0.16 o posterior siguiendo `database/README_DB.md` y ejecutar, en orden, `01_schema.sql`, `02_seguridad.sql`, una copia local de `02_cuentas.local.sql.example` y opcionalmente `03_datos_prueba.sql` sobre tablas vacías.
2. Crear un archivo `.env` local con `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` y `DB_NAME`; `repositories/conexion.py` define valores predeterminados para todos menos la contraseña.
3. Asegurar las dependencias que aparecen en los imports: `mysql-connector-python` y `python-dotenv`. `main` no contiene un manifiesto de dependencias, por lo que no se fija aquí una versión no documentada.
4. Ejecutar `python main.py` desde la raíz del repositorio.

La rama educativa fue comprobada con compilación estática de todos los archivos Python. No se realizó una prueba funcional completa porque requiere una instancia MySQL configurada, credenciales locales y un entorno gráfico; tampoco se alteraron datos reales.

## Limitaciones y observaciones

Son aspectos para estudiar, no correcciones aplicadas por esta rama:

- El login navega al inicio sin validar credenciales; el documento ABP también lo identifica como no implementado.
- `RegistrarSocio` muestra mensajes y campos, pero no llama a un repositorio para persistir altas, cambios o bajas.
- `HistorialPrestamosSocio` referencia atributos que no inicializa (`self.socio` y `self.prestamos`); la pantalla usada desde gestión de socios es actualmente `VistaPrestamosSocio`.
- Algunas métricas no coinciden exactamente con su nombre o con el esquema: por ejemplo, atraso se cuenta por fecha de devolución nula y finalizados incluye el estado literal `cerrado`, mientras el esquema usa `cerrado_sin_devolver`.
- La baja lógica de libro no comprueba en Python si existen préstamos activos. El esquema restringe borrados físicos mediante claves foráneas, pero una baja lógica es un `UPDATE` y requiere su propia regla.
- No se observa el límite de diez títulos distintos por préstamo.
- Hay textos con problemas históricos de codificación y nombres de interfaz inconsistentes. Se preservaron para no modificar el comportamiento ni el contenido original.
- No existe una suite de pruebas automatizadas en `main` ni un archivo de dependencias verificable.

