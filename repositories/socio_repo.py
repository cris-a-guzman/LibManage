# repositories/socios_repository.py
from repositories.base_repository import BaseRepository

class SociosRepo(BaseRepository):
    
    def cantidad_socios(self):
        consulta = """
            SELECT COUNT(*) AS total
            FROM socio
        """
        resultado = self._ejecutar_consulta(consulta)
        return resultado[0]['total'] if resultado else 0
    
    def cantidad_socios_prestamos(self):
        consulta = """
            SELECT count(distinct prestamo.id_socio) as unicos
            from socio
            inner join prestamo On socio.id_socio = prestamo.id_socio;
        """
        resultado = self._ejecutar_consulta(consulta)
        return resultado[0]['unicos'] if resultado else 0
        
    
    def obtener_socios_dni(self):
        consulta = """
            SELECT dni
            FROM socio
            WHERE fecha_baja IS NULL
            ORDER BY dni DESC
        """        
        return [i['dni'] for i in self._ejecutar_consulta(consulta)]
        

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