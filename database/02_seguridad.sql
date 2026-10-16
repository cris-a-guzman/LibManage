-- ============================================================
-- LibManage - 02_seguridad.sql
-- MySQL 8.0 - Definicion de roles y permisos
-- Este archivo SI se versiona en Git.
-- Ejecutar con una cuenta administradora, despues de 01_schema.sql.
-- No contiene contrasenas ni crea cuentas de conexion.
-- ============================================================

USE libmanage;

-- Administracion de la base LibManage (no de todo MySQL).
CREATE ROLE IF NOT EXISTS 'rol_libmanage_admin';

-- Operaciones permitidas a la aplicacion Python.
CREATE ROLE IF NOT EXISTS 'rol_libmanage_app';

GRANT ALL PRIVILEGES ON libmanage.*
    TO 'rol_libmanage_admin';

GRANT SELECT, INSERT, UPDATE ON libmanage.*
    TO 'rol_libmanage_app';
