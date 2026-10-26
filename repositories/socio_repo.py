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

    def obtener_socio_por_id(self, id_socio): #! Buscar a donde mas se usa esto
        consulta = """
            SELECT id_socio, dni, nombre, apellido, fecha_asociacion, telefono
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
    
    def registrar_socio(self, datos_socio):
        consulta = """
            INSERT INTO socio (dni, nombre, apellido, fecha_asociacion, telefono)
            VALUES (%s, %s, %s, %s, %s)
        """
        resultado = self._ejecutar_escritura(consulta, (datos_socio['dni'],
                                                        datos_socio['nombre'],
                                                        datos_socio['apellido'],
                                                        datos_socio['fecha_asociacion'],
                                                        datos_socio['telefono']))
        return resultado["lastrowid"]
    
    def baja_socio(self, id_socio):
        consulta = """
            UPDATE socio SET fecha_baja = NOW() WHERE id_socio = %s;
        """
        
        resultado = self._ejecutar_escritura(consulta, (id_socio,))
        return resultado['rowcount'] > 0
    
    def tiene_prestamos_activos(self, id_socio):
        consulta = """
            SELECT COUNT(*) AS total
            FROM prestamo
            WHERE id_socio = %s AND estado = 'activo'
        """
        resultado = self._ejecutar_consulta(consulta, (id_socio,), fetchone=True)
        return resultado['total'] > 0 if resultado else False

    def modificar_socio(self, id_socio, datos):
        consulta = """
            UPDATE socio
            SET dni = %s,
                nombre = %s,
                apellido = %s,
                telefono = %s,
                fecha_asociacion = %s
            WHERE id_socio = %s
            AND fecha_baja IS NULL
        """

        parametros = (
            datos["dni"],
            datos["nombre"],
            datos["apellido"],
            datos["telefono"],
            datos["fecha_asociacion"],
            id_socio
        )

        return self._ejecutar_escritura(
            consulta, parametros
        )["rowcount"]

    
    def dni_asignado_a_otro(self, dni, id_socio):
        consulta = """
            SELECT 1 FROM socio
            WHERE dni = %s
            AND id_socio <> %s
            LIMIT 1
        """

        resultado = self._ejecutar_consulta(
            consulta, (dni, id_socio), fetchone=True
        )
        return resultado is not None
