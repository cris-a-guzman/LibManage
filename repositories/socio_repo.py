
from repositories.conexion import obtener_conexion


def listar_socios():
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError("No se pudo conectar a MySQL")

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_socio, dni, nombre, apellido
            FROM socio
            WHERE fecha_baja IS NULL
            ORDER BY apellido, nombre
        """)

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
