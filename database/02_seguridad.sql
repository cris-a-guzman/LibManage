-- ============================================================
-- LibManage - 02_seguridad.sql
-- MySQL 8.0 - Definicion de roles y permisos
-- Este archivo SI se versiona en Git.
-- Ejecutar con una cuenta administradora, despues de 01_schema.sql.
-- No contiene contrasenas ni crea cuentas de conexion.
-- Principio aplicado: la aplicación recibe SELECT/INSERT/UPDATE, mientras que
-- las tareas administrativas conservan un rol separado con más privilegios.
-- Guía: docs/estudio/README.md#modelo-relacional-y-sql
-- ============================================================

USE libmanage;

-- Administracion de la base LibManage (no de todo MySQL).
CREATE ROLE IF NOT EXISTS 'rol_libmanage_admin';

-- Operaciones permitidas a la aplicacion Python.
CREATE ROLE IF NOT EXISTS 'rol_libmanage_app';

GRANT ALL PRIVILEGES ON libmanage.*
    TO 'rol_libmanage_admin';

-- No se concede DELETE al rol de la aplicación: las bajas del modelo son
-- lógicas mediante fecha_baja y así se preserva el historial.
GRANT SELECT, INSERT, UPDATE ON libmanage.*
    TO 'rol_libmanage_app';
