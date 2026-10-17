from repositories.conexion import obtener_conexion
from datetime import date


def listar_prestamos(solo_vencidos=False):
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
                p.fecha_devolucion_estimada AS vence,
                p.estado

            FROM prestamo p

            JOIN socio s
                ON p.id_socio = s.id_socio

            LEFT JOIN detalle_prestamo dp
                ON p.id_prestamo = dp.id_prestamo

            LEFT JOIN libro l
                ON dp.id_libro = l.id_libro
            WHERE (
                %s = 0
                OR (
                    p.estado = 'activo'
                    AND p.fecha_devolucion_estimada < %s
                )
            )
            GROUP BY
                p.id_prestamo,
                s.nombre,
                s.apellido,
                p.fecha_devolucion_estimada,
                p.estado

            ORDER BY p.fecha_devolucion_estimada
        """

        cursor.execute(consulta, (int(solo_vencidos), date.today()))
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()



def devolver_prestamo(id_prestamo):
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError("No se pudo conectar a MySQL")

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            UPDATE prestamo
            SET estado = 'devuelto',
                fecha_devolucion_real = CURDATE()
            WHERE id_prestamo = %s
              AND estado = 'activo'
              AND fecha_prestamo <= CURDATE()
        """

        cursor.execute(consulta, (id_prestamo,))
        actualizado = cursor.rowcount > 0

        conexion.commit()
        return actualizado

    except Exception:
        conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
