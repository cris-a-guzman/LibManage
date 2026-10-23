# Estudio de la API experimental de Open Library

## Alcance y estado

Este análisis describe el código real del commit [`80a80aa`](https://github.com/cris-a-guzman/LibManage/tree/80a80aab302e065b562fa2e24820b66e40e19dc4) de `poc-api`. La [comparación fijada entre los commits verificados](https://github.com/cris-a-guzman/LibManage/compare/daa29a2454d5a7cd15703638a0847a4de1e47070...80a80aab302e065b562fa2e24820b66e40e19dc4) muestra nueve commits y archivos que no pertenecen a `main`. No se copiaron ejecutables ni se fusionó esta rama con la rama de estudio.

Una interfaz de programación de aplicaciones (API) define una forma acordada para que dos sistemas intercambien solicitudes y respuestas. En esta prueba de concepto, LibManage actúa como cliente: envía una búsqueda al servicio público Open Library y recibe datos estructurados en JSON (JavaScript Object Notation), un formato de texto que representa objetos, listas y valores.

## Archivos experimentales

- [`api_libros/open_library.py`](https://github.com/cris-a-guzman/LibManage/blob/80a80aab302e065b562fa2e24820b66e40e19dc4/api_libros/open_library.py): cliente usado por la pantalla experimental de Tkinter.
- [`views/libros_views/crear_libro_view.py`](https://github.com/cris-a-guzman/LibManage/blob/80a80aab302e065b562fa2e24820b66e40e19dc4/views/libros_views/crear_libro_view.py): presenta resultados externos y permite trasladar una selección al formulario.
- [`api_libros/open_library_client.py`](https://github.com/cris-a-guzman/LibManage/blob/80a80aab302e065b562fa2e24820b66e40e19dc4/api_libros/open_library_client.py): versión de consola que busca, pide elegir un resultado y guarda un JSON local.
- [`api-libros/openlibrary_client.py`](https://github.com/cris-a-guzman/LibManage/blob/80a80aab302e065b562fa2e24820b66e40e19dc4/api-libros/openlibrary_client.py): copia histórica en una carpeta con guion.
- [`api_libros/README.md`](https://github.com/cris-a-guzman/LibManage/blob/80a80aab302e065b562fa2e24820b66e40e19dc4/api_libros/README.md): declara expresamente que la funcionalidad es experimental.

## Cómo se comunica con Open Library

1. `LibraryApi.__init__()` guarda la URL `https://openlibrary.org/search.json`.
2. `buscar_titulo(nombre_libro)` arma el diccionario `params` con el texto, los campos solicitados y un límite de diez resultados.
3. `requests.get(self.URL, params=params)` realiza una solicitud HTTP GET. La biblioteca `requests` codifica esos parámetros en la URL.
4. `x.json()` interpreta el cuerpo JSON y lo convierte en diccionarios y listas de Python.
5. `encontrados2()` toma la lista `docs` y construye registros más pequeños con autor, título, índice y año para la tabla de la interfaz.
6. Tras una selección, `funcion_final()` usa la clave `key` para pedir el detalle de la obra y `limpiar_datos_libro()` prepara título, autor, ISBN y año.

La documentación externa enlazada por la propia prueba de concepto es [Open Library Search API](https://openlibrary.org/dev/docs/api/search). No se localizó en los materiales institucionales consultados una sección teórica específica sobre consumo de API; por eso esta referencia queda identificada como externa.

## Presentación de resultados en Tkinter

`CrearLibro` crea dos sectores: el formulario local y un `ttk.Treeview` para la búsqueda externa. El botón **Buscar libro** llama al cliente; `actualizar_treeview()` recorre los resultados y agrega una fila por libro. Un doble clic obtiene el índice visible, recupera el detalle y completa los `Entry` del formulario mediante `cargar_datos()`.

La información externa no se guarda automáticamente. El intento de integración conserva una decisión humana intermedia: seleccionar un resultado, revisar los campos y luego usar el flujo local de guardado. Pedagógicamente, esto separa **consulta remota**, **transformación de datos**, **presentación** y **persistencia local**.

## Diferencias con `main`

| Aspecto | `main` | `poc-api` |
|---|---|---|
| Alta/modificación de libro | Una única pantalla `ModificarLibro`, sin consulta remota. | Añade `CrearLibro` y una búsqueda en Open Library. |
| Dependencia HTTP | No usa `requests`. | Importa `requests`, pero el `requirements.txt` experimental está vacío. |
| Datos de libro | Se ingresan manualmente; `crear_libro()` no recibe ISBN. | El alta experimental intenta recibir ISBN y completar campos desde la API. |
| Carpeta API | No existe. | Conviven `api_libros/` y `api-libros/`, con implementaciones duplicadas o históricas. |
| Estado | Versión principal. | Prueba de concepto no fusionada. |

## Componentes implementados y límites verificados

Implementado en el código experimental:

- construcción de solicitudes GET de búsqueda y detalle;
- conversión de respuestas JSON a listas y diccionarios de Python;
- visualización de hasta diez resultados en un `Treeview`;
- copiado de datos seleccionados al formulario;
- una variante de consola que guarda el resultado elegido como archivo JSON.

Observaciones para estudiar, sin convertirlas en tareas de corrección:

- No hay manejo de errores de red, códigos inesperados, tiempo de espera ni JSON inválido.
- `buscar_titulo()` contiene código después de un `return`, por lo que ese bloque no puede ejecutarse.
- `limpiar_datos_libro()` accede al primer ISBN con `[0]`; una obra sin ISBN produciría una excepción.
- La pantalla llama a `actualizar_libro(..., isbn)`, pero la firma experimental de `LibroRepo.actualizar_libro()` no recibe ese argumento adicional.
- La variante `open_library_client.py` ejecuta la búsqueda inmediatamente al importarse porque crea un objeto y llama al método al final del archivo.
- La carpeta `api-libros` tiene un guion y no puede referenciarse como un paquete Python mediante la sintaxis normal de `import`.
- `json` está importado en `open_library.py` pero no se usa en ese archivo.
- No se verificó el servicio externo en ejecución: el análisis se limitó al código y a la historia de GitHub, tal como requiere una revisión sin servicios externos.

## Vinculación pedagógica

- Listas, diccionarios, recorridos y valores opcionales: [Python. Introducción](https://drive.google.com/file/d/1_o7PcansHQR1j36Tw2rwy4VCkTeCG_Lc/view), **Estructuras de datos** (pp. 57-67).
- Clases, instancias y métodos: [POO. Fundamentos](https://drive.google.com/file/d/1T6vr8DepNkH0nefT0LFnNnGXVCQiKjPX/view), **Objetos**, **Clases** y **Clases e instancias en Python** (pp. 4-10).
- Interfaz, `Treeview` y eventos: [Tkinter - Elementos, widgets y configuraciones](https://docs.google.com/document/d/1_-8J29ahj2cHIpIp_qHEGT4RKL-bfPSB1To_1_yYlUU/edit), secciones 5, 7 y 8; [Eventos en Tkinter](https://docs.google.com/document/d/1rWseXXTyjJOjQgviNmR5ZMmzmUh8TO-G/edit), secciones 1 y 2.
- Persistencia y separación entre interfaz y acceso a datos: [POO. Acceso a datos](https://drive.google.com/file/d/17zuW5msMQfKQ_3CLy1Z4O6xYrLBbPRJp/view), **Persistencia** (p. 2) y **Acceso a datos** (p. 3).

La comunicación HTTP y el contrato concreto de Open Library no quedaron cubiertos por una fuente institucional específica verificada. Se explican a partir del código real y de la documentación externa indicada por la propia prueba de concepto.
