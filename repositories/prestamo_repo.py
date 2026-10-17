# repositories/prestamo_repository.py
from datetime import date
from repositories.base_repository import BaseRepository

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