# LibManage — Instalación de la base de datos

## Requisitos

- MySQL 8.0.16 o superior, instalado y en funcionamiento.
- Un cliente SQL (por ejemplo, DBeaver o MySQL Workbench).
- Una conexión a MySQL con permisos para crear bases, tablas, roles y usuarios (por ejemplo, `root`).

## Instalación paso a paso

1. **Conectarse a MySQL** con una cuenta administradora desde el cliente SQL.
2. **Crear la base y las tablas:** abrir `01_schema.sql` y ejecutar **todo el script**.
3. **Crear los roles y permisos:** abrir y ejecutar `02_seguridad.sql`.
4. **Preparar las cuentas:** copiar `02_cuentas.local.sql.example` y renombrar la copia a `02_cuentas.local.sql`.
5. **Definir las contraseñas:** en `02_cuentas.local.sql`, reemplazar `CAMBIAR_POR_CLAVE_ADMIN_DISTINTA` y `CAMBIAR_POR_CLAVE_APP_DISTINTA` por dos contraseñas seguras y diferentes. Revisar también el host (`'%'`) de las cuentas y restringirlo si corresponde al entorno.
6. **Crear los usuarios:** ejecutar `02_cuentas.local.sql` con la cuenta administradora.
7. **Cargar los ejemplos:** ejecutar `03_datos_prueba.sql` sobre las **tablas vacías**.

> En el cliente SQL, elegir **Ejecutar script completo** (no solamente la sentencia bajo el cursor).

## Comprobación

Conectarse a la base `libmanage` y ejecutar:

```sql
USE libmanage;

SELECT COUNT(*) AS socios FROM socio;
SELECT COUNT(*) AS libros FROM libro;
SELECT COUNT(*) AS prestamos FROM prestamo;
SELECT COUNT(*) AS detalles FROM detalle_prestamo;
```

**Resultado esperado:** 10 socios, 30 libros, 20 préstamos y 50 detalles.

Después, crear una conexión nueva con el usuario `usuario_sistema` y su contraseña, y ejecutar:

```sql
SELECT CURRENT_USER(), CURRENT_ROLE();
SHOW TABLES FROM libmanage;
```

El rol activo debe ser `rol_libmanage_app`, con permisos `SELECT`, `INSERT` y `UPDATE`. El usuario `administrador` tiene el rol `rol_libmanage_admin` con permisos sobre la base `libmanage`.

## Consideraciones

- **No volver a ejecutar la instalación sobre una base con datos.** Los archivos están preparados para una instalación inicial; no borran ni reinician la base existente.
- **No subir contraseñas al repositorio.** Versionar la plantilla `.example`, pero no `02_cuentas.local.sql` (excluido por el `.gitignore`).
- La aplicación Python utilizará la cuenta `usuario_sistema`, **no** `root`.
- Este procedimiento **no requiere Docker**: solamente un servidor MySQL accesible. Su configuración se documentará por separado.
