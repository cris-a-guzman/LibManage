# repositories/socios_repository.py
from repositories.base_repository import BaseRepository

class SociosRepo(BaseRepository):

    def listar_socios(self):
        consulta = """
            SELECT id_socio, dni, nombre, apellido
            FROM socio
            WHERE fecha_baja IS NULL
            ORDER BY apellido, nombre
        """
        return self._ejecutar_consulta(consulta)

    def obtener_socio_por_id(self, id_socio):
        consulta = """
            SELECT id_socio, dni, nombre, apellido
            FROM socio
            WHERE id_socio = %s
        """
        return self._ejecutar_consulta(consulta, (id_socio,), fetchone=True)

    def listar_prestamos_socio(self, id_socio):
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
            JOIN detalle_prestamo dp ON p.id_prestamo = dp.id_prestamo
            JOIN libro l ON dp.id_libro = l.id_libro
            WHERE p.id_socio = %s
            GROUP BY p.id_prestamo, p.fecha_prestamo, p.fecha_devolucion_estimada, p.fecha_devolucion_real, p.estado
            ORDER BY p.fecha_prestamo DESC
        """
        return self._ejecutar_consulta(consulta, (id_socio,))