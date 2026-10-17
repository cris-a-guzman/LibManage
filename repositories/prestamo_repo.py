# repositories/prestamo_repository.py
from datetime import date
from repositories.base_repository import BaseRepository
from repositories.conexion import obtener_conexion

class PrestamoRepo(BaseRepository):

    def listar_prestamos(self, solo_vencidos=False):
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
            JOIN socio s ON p.id_socio = s.id_socio
            LEFT JOIN detalle_prestamo dp ON p.id_prestamo = dp.id_prestamo
            LEFT JOIN libro l ON dp.id_libro = l.id_libro
            WHERE (
                %s = 0 OR (p.estado = 'activo' AND p.fecha_devolucion_estimada < %s)
            )
            GROUP BY p.id_prestamo, s.nombre, s.apellido, p.fecha_devolucion_estimada, p.estado
            ORDER BY p.fecha_devolucion_estimada
        """
        return self._ejecutar_consulta(consulta, (int(solo_vencidos), date.today()), dictionary=False)

    def devolver_prestamo(self, id_prestamo):
        consulta = """
            UPDATE prestamo
            SET estado = 'devuelto',
                fecha_devolucion_real = CURDATE()
            WHERE id_prestamo = %s
              AND estado = 'activo'
              AND fecha_prestamo <= CURDATE()
        """
        resultado = self._ejecutar_escritura(consulta, (id_prestamo,))
        return resultado["rowcount"] > 0
    
    def crear_prestamo(self, dni_socio, id_libro, fecha_devolucion):
        if fecha_devolucion < date.today():
            raise ValueError(
                "La fecha de devolución no puede ser anterior a hoy."
            )

        conexion = obtener_conexion()

        if conexion is None:
            raise ConnectionError("No se pudo conectar a MySQL")

        cursor = None

        try:
            conexion.start_transaction()
            cursor = conexion.cursor(dictionary=True)

            # identificar al socio mediante su DNI
            cursor.execute("""
                SELECT id_socio
                FROM socio
                WHERE dni = %s AND fecha_baja IS NULL
            """, (dni_socio,))

            socio = cursor.fetchone()

            if socio is None:
                raise ValueError("El socio no existe o está dado de baja.")

            # obtener el libro y bloquearlo durante la operación
            cursor.execute("""
                SELECT cantidad_total
                FROM libro
                WHERE id_libro = %s AND fecha_baja IS NULL
                FOR UPDATE
            """, (id_libro,))

            libro = cursor.fetchone()

            if libro is None:
                raise ValueError("El libro no existe o está dado de baja.")

            # calcular ejemplares que todavía no se devolvieron
            cursor.execute("""
                SELECT COALESCE(SUM(dp.cantidad), 0) AS ocupados
                FROM detalle_prestamo dp
                JOIN prestamo p
                    ON dp.id_prestamo = p.id_prestamo
                WHERE dp.id_libro = %s
                  AND p.estado IN ('activo', 'cerrado_sin_devolver')
            """, (id_libro,))

            ocupados = cursor.fetchone()["ocupados"]
            disponibles = libro["cantidad_total"] - ocupados

            if disponibles < 1:
                raise ValueError("No hay ejemplares disponibles.")

            # registrar el préstamo
            cursor.execute("""
                INSERT INTO prestamo (
                    id_socio,
                    fecha_prestamo,
                    fecha_devolucion_estimada,
                    estado
                )
                VALUES (%s, CURDATE(), %s, 'activo')
            """, (socio["id_socio"], fecha_devolucion))

            id_prestamo = cursor.lastrowid

            # asociar un ejemplar del libro al préstamo
            cursor.execute("""
                INSERT INTO detalle_prestamo (
                    id_prestamo,
                    id_libro,
                    cantidad
                )
                VALUES (%s, %s, %s)
            """, (id_prestamo, id_libro, 1))

            # confirmar ambas inserciones
            conexion.commit()

            return id_prestamo

        except Exception:
            conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()
