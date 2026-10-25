[README.md](https://github.com/user-attachments/files/33927643/README.md)
# LibManage

Sistema de gestión de biblioteca (libros, socios y préstamos) desarrollado para el ABP. Es una aplicación de escritorio hecha en Python con Tkinter, que guarda sus datos en una base MySQL.

## Contenido

1. [Requisitos](#1-requisitos)
2. [Instalación](#2-instalación)
3. [Ejecutar la aplicación](#3-ejecutar-la-aplicación)
4. [Problemas comunes](#4-problemas-comunes)
5. [Estructura del proyecto](#5-estructura-del-proyecto)
6. [Más documentación](#6-más-documentación)

---

## 1. Requisitos

| Qué | Versión | Notas |
|---|---|---|
| Python | 3.10 o superior | Con `pip`. En Windows, al instalarlo marcá **Add python.exe to PATH**. |
| MySQL | **8.0.16 o superior** | Versiones anteriores ignoran las restricciones `CHECK` del esquema. |
| Cliente SQL | Cualquiera | Por ejemplo DBeaver o MySQL Workbench, para ejecutar los scripts de la base. |
| Git | Cualquiera | Para clonar el proyecto. |

**Tkinter** (la librería de ventanas) viene incluida con el instalador de Python para Windows. En Linux (Ubuntu, Mint, Debian) hay que instalarla aparte:

```bash
sudo apt install python3-tk
```

---

## 2. Instalación

### 2.1 Descargar el proyecto

```bash
git clone https://github.com/cris-a-guzman/LibManage.git
cd LibManage
```

> Si es la primera vez que usás Git en el proyecto, mirá la [guía de uso de Git](docs/guia-git.md) (ramas, `pull`, `commit` y `push`).

### 2.2 Crear la base de datos

Seguí el paso a paso de **[database/README_DB.md](database/README_DB.md)**. En resumen, se ejecutan los scripts de la carpeta `database/` en este orden:

1. `01_schema.sql`: crea la base `libmanage` y las tablas.
2. `02_seguridad.sql`: crea los roles y permisos.
3. `02_cuentas.local.sql`: crea los usuarios (se arma copiando `02_cuentas.local.sql.example` y poniendo contraseñas propias).
4. `03_datos_prueba.sql`: carga datos de ejemplo (opcional, pero recomendado para probar la app).

> Anotá la contraseña que le pusiste a `usuario_sistema`: la necesitás en el paso siguiente.

### 2.3 Configurar el archivo `.env`

La aplicación lee los datos de conexión de un archivo `.env` que está en la carpeta principal del proyecto (al lado de `main.py`). Para crearlo, copiá la plantilla:

```bash
# Windows (cmd o PowerShell)
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

Después abrí `.env` con un editor de texto y completalo:

| Variable | Qué es | Valor por defecto |
|---|---|---|
| `DB_HOST` | Dónde está MySQL | `127.0.0.1` |
| `DB_PORT` | Puerto de MySQL | `3306` |
| `DB_USER` | Usuario de la aplicación | `usuario_sistema` |
| `DB_PASSWORD` | Contraseña de ese usuario | *(no tiene: es obligatoria)* |
| `DB_NAME` | Nombre de la base | `libmanage` |

Lo único que casi siempre hay que cambiar es `DB_PASSWORD`: tiene que ser la contraseña que definiste para `usuario_sistema` en el paso 2.2.

> **Importante:** la aplicación usa la cuenta `usuario_sistema`, **no** `root`. Y el archivo `.env` tiene contraseñas, así que **nunca se sube a GitHub** (ya está excluido en el `.gitignore`; lo que se versiona es la plantilla `.env.example`).

### 2.4 Crear el entorno virtual e instalar las dependencias

Un entorno virtual (`.venv`) mantiene las librerías del proyecto separadas del resto de tu Python. Desde la carpeta principal del proyecto:

```bash
# Crear el entorno virtual
python -m venv .venv

# Activarlo
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / macOS

# Instalar las dependencias
pip install -r requirements.txt
```

Cuando está activo, la terminal muestra `(.venv)` al principio de la línea. Cada vez que abras una terminal nueva para trabajar tenés que volver a activarlo (solo el comando `activate`).

> En Linux/macOS, si `python` no existe, usá `python3` en su lugar.

Las dependencias de `requirements.txt` son:

| Paquete | Para qué se usa |
|---|---|
| `mysql-connector-python` | Conectarse a MySQL desde Python. |
| `python-dotenv` | Leer el archivo `.env`. |
| `requests` | Consultar la API de Open Library (módulo `api_libros`). |

---

## 3. Ejecutar la aplicación

Con MySQL encendido y el entorno virtual activado, desde la carpeta principal del proyecto (donde está `main.py`):

```bash
python main.py
```

Se abre la ventana de **LibManage** en la pantalla de inicio, con el resumen de libros, préstamos y socios y los botones para entrar a cada sección. Por ahora la aplicación no pide usuario ni contraseña.

> La aplicación siempre se inicia con `main.py`. Si ejecutás directamente otro archivo de `views/` o `repositories/`, Python no encuentra los módulos del proyecto.

Si cargaste `03_datos_prueba.sql`, vas a ver 10 socios, 30 libros y 20 préstamos de ejemplo.

---

## 4. Problemas comunes

| Mensaje o síntoma | Qué pasa y cómo se arregla |
|---|---|
| `ModuleNotFoundError: No module named 'views'` (o `repositories`) | Estás ejecutando un archivo interno (por ejemplo `repositories/libro_repo.py`) en vez de `main.py`. Corré `python main.py` desde la carpeta principal. |
| `ModuleNotFoundError: No module named 'mysql'` (o `dotenv`) | Falta activar el entorno virtual o instalar las dependencias: `pip install -r requirements.txt`. |
| `ModuleNotFoundError: No module named 'tkinter'` | En Linux: `sudo apt install python3-tk`. En Windows: reinstalá Python y dejá marcada la opción *tcl/tk and IDLE*. |
| `ConnectionError: No se pudo conectar a la base de datos MySQL` | Es el mensaje general de error de conexión; el detalle viene a continuación. Revisá los casos de abajo. |
| ...`Can't connect to MySQL server` | MySQL está apagado, o `DB_HOST` / `DB_PORT` del `.env` no son los correctos. |
| ...`Access denied for user` | Contraseña o usuario incorrectos en el `.env`, o todavía no ejecutaste `02_cuentas.local.sql`. Si dice `using password: NO`, el `.env` no existe o no está al lado de `main.py`. |
| ...`Unknown database 'libmanage'` | Todavía no ejecutaste `01_schema.sql`. |
| La aplicación abre pero las listas están vacías | Falta cargar `03_datos_prueba.sql` (o todavía no hay datos cargados). |

---

## 5. Estructura del proyecto

```
LibManage/
├── main.py                 Punto de entrada: abre la ventana principal.
├── requirements.txt        Dependencias de Python.
├── .env.example            Plantilla de configuración (se copia a .env).
│
├── views/                  Interfaz gráfica (Tkinter): una carpeta por sección.
│   ├── components/         Piezas reutilizables: ventana principal, base de las pantallas,
│   │                       formulario con scroll y lista desplegable con autocompletado.
│   ├── home_view/          Pantalla de inicio con el resumen.
│   ├── libros_views/       Gestión de libros (listar, crear, modificar).
│   ├── socio_views/        Gestión de socios y su historial de préstamos.
│   ├── prestamos_views/    Gestión de préstamos (listar, registrar, devolver).
│   └── login_view/         Pantalla de login (todavía no se usa).
│
├── repositories/           Acceso a la base de datos (consultas SQL).
│   ├── conexion.py         Abre la conexión a MySQL con los datos del .env.
│   ├── base_repository.py  Métodos comunes para ejecutar consultas y escrituras.
│   └── *_repo.py           Un repositorio por entidad: libro, socio y préstamo.
│
├── api_libros/             Consulta de datos de libros en la API pública de Open Library
│                           (necesita internet y la librería requests).
│
├── database/               Scripts SQL y guía de instalación de la base (README_DB.md).
└── docs/                   Documentación: guía de Git y bitácora semanal.
```

**Cómo se conectan las capas:** las pantallas (`views/`) nunca escriben SQL; le piden los datos a los repositorios (`repositories/`), que son los únicos que hablan con MySQL.

---

## 6. Más documentación

- [Instalación de la base de datos](database/README_DB.md)
- [Guía de uso de Git](docs/guia-git.md)
- [Bitácora semanal](docs/bitacora/)
