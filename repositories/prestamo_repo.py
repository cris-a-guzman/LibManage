from repositories.conexion import obtener_conexion


def listar_prestamos():
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError("No se pudo conectar a MySQL")

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            SELECT
                p.id_prestamo,
                CONCAT(s.nombre, ' ', s.apellido) AS socio,
                COALESCE(
                    GROUP_CONCAT(
                        CONCAT(l.titulo, ' (', dp.cantidad, ')')
                        ORDER BY l.titulo
                        SEPARATOR ', '
                    ),
                    'Sin libros'
                ) AS libro,
                p.fecha_devolucion_estimada AS vence

            FROM prestamo p

            JOIN socio s
                ON p.id_socio = s.id_socio

            LEFT JOIN detalle_prestamo dp
                ON p.id_prestamo = dp.id_prestamo

            LEFT JOIN libro l
                ON dp.id_libro = l.id_libro

            GROUP BY
                p.id_prestamo,
                s.nombre,
                s.apellido,
                p.fecha_devolucion_estimada

            ORDER BY p.fecha_devolucion_estimada
        """

        cursor.execute(consulta)
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
