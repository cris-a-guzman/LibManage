# Consultas de lectura sobre socios y su historial de préstamos.
# En `main` todavía no contiene escrituras para alta, modificación o baja de socios.
# Referencias: docs/estudio/README.md#persistencia-y-crud y
# docs/estudio/README.md#reglas-de-negocio
from repositories.base_repository import BaseRepository

# Repositorio especializado en la tabla `socio` y sus préstamos relacionados.
class SociosRepo(BaseRepository):
    
    # Cuenta todas las filas de socio, incluidas las que tienen baja lógica.
    def cantidad_socios(self):
        consulta = """
            SELECT COUNT(*) AS total
            FROM socio
        """
        resultado = self._ejecutar_consulta(consulta)
        return resultado[0]['total'] if resultado else 0
    
    # Cuenta socios distintos que aparecen al menos una vez en `prestamo`.
    def cantidad_socios_prestamos(self):
        consulta = """
            SELECT count(distinct prestamo.id_socio) as unicos
            from socio
            inner join prestamo On socio.id_socio = prestamo.id_socio;
        """
        resultado = self._ejecutar_consulta(consulta)
        return resultado[0]['unicos'] if resultado else 0
        
    
    # Devuelve una lista de DNI vigentes para el selector de préstamos.
    def obtener_socios_dni(self):
        consulta = """
            SELECT dni
            FROM socio
            WHERE fecha_baja IS NULL
            ORDER BY dni DESC
        """        
        return [i['dni'] for i in self._ejecutar_consulta(consulta)]
        

    # Lista socios sin baja lógica para la pantalla de gestión.
    def listar_socios(self):
        consulta = """
            SELECT id_socio, dni, nombre, apellido
            FROM socio
            WHERE fecha_baja IS NULL
            ORDER BY apellido, nombre
        """
        return self._ejecutar_consulta(consulta)

    # Busca una fila por clave primaria; devuelve un diccionario o None.
    def obtener_socio_por_id(self, id_socio):
        consulta = """
            SELECT id_socio, dni, nombre, apellido
            FROM socio
            WHERE id_socio = %s
        """
        return self._ejecutar_consulta(consulta, (id_socio,), fetchone=True)

    # Une préstamos, detalles y libros para construir el historial de un socio.
    # GROUP_CONCAT reúne en una sola celda los títulos de cada préstamo.
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