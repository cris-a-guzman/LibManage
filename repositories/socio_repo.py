
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



def obtener_socio_por_id(id_socio):
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError("No se pudo conectar a MySQL")

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_socio, dni, nombre, apellido
            FROM socio
            WHERE id_socio = %s
        """, (id_socio,))

        return cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()



def listar_prestamos_socio(id_socio):
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError("No se pudo conectar a MySQL")

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        consulta = """
            SELECT
                p.id_prestamo AS id,
                GROUP_CONCAT(
                    CONCAT(l.titulo, ' (', dp.cantidad, ')')
                    ORDER BY l.titulo
                    SEPARATOR ', '
                ) AS libro,
                p.fecha_prestamo,
                p.fecha_devolucion_estimada,
                p.fecha_devolucion_real,
                p.estado
            FROM prestamo p
            JOIN detalle_prestamo dp
                ON p.id_prestamo = dp.id_prestamo
            JOIN libro l
                ON dp.id_libro = l.id_libro
            WHERE p.id_socio = %s
            GROUP BY
                p.id_prestamo,
                p.fecha_prestamo,
                p.fecha_devolucion_estimada,
                p.fecha_devolucion_real,
                p.estado
            ORDER BY p.fecha_prestamo DESC
        """

        cursor.execute(consulta, (id_socio,))
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
