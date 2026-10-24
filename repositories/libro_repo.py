# repositories/libro_repository.py
from repositories.base_repository import BaseRepository

class LibroRepo(BaseRepository):
    
    def obtener_titulos_ids(self):
        consulta = """
            SELECT titulo, id_libro
            FROM libro
            WHERE fecha_baja IS NULL
        """
        return self._ejecutar_consulta(consulta)
    
    def cantidad_total_ejemplares(self):
        consulta = """
            SELECT COALESCE(SUM(cantidad_total), 0) AS total 
            FROM libro 
            WHERE fecha_baja IS NULL
        """
        resultado = self._ejecutar_consulta(consulta, fetchone=True)
        return resultado["total"] if resultado else 0
    
    def cantidad_ejemplares_prestados(self):
        consulta = """SELECT COALESCE(SUM(dt.cantidad), 0) AS libros_prestados
            FROM detalle_prestamo dt
            JOIN prestamo p ON dt.id_prestamo = p.id_prestamo
            WHERE p.estado = 'activo'
            """
        resultado = self._ejecutar_consulta(consulta)        
        return resultado[0]['libros_prestados'] if resultado else 0

    def listar_libros(self):
        consulta = """
            SELECT id_libro, isbn, titulo, autor, anio, cantidad_total
            FROM libro
            WHERE fecha_baja IS NULL
            ORDER BY titulo
        """
        return self._ejecutar_consulta(consulta)

    def crear_libro(self, titulo, autor, anio, cantidad_total, isbn):
        consulta = """
            INSERT INTO libro (titulo, autor, anio, cantidad_total, isbn)
            VALUES (%s, %s, %s, %s, %s)
        """
        resultado = self._ejecutar_escritura(consulta, (titulo, autor, anio, cantidad_total, isbn))
        return resultado["lastrowid"]

    def actualizar_libro(self, id_libro, titulo, autor, anio, cantidad_total):
        consulta = """
            UPDATE libro
            SET titulo = %s, autor = %s, anio = %s, cantidad_total = %s
            WHERE id_libro = %s
        """
        self._ejecutar_escritura(consulta, (titulo, autor, anio, cantidad_total, id_libro))

    def dar_baja_libro(self, id_libro):
        consulta = """
            UPDATE libro
            SET fecha_baja = NOW()
            WHERE id_libro = %s AND fecha_baja IS NULL
        """
        resultado = self._ejecutar_escritura(consulta, (id_libro,))
        return resultado["rowcount"] > 0
    
    def obtener_disponibilidad_libros(self):
        consulta = """
            SELECT
                l.id_libro,
                l.titulo,
                l.cantidad_total,
                l.cantidad_total - COALESCE(
                    SUM(
                        CASE
                            WHEN p.estado IN (
                                'activo',
                                'cerrado_sin_devolver'
                            )
                            THEN dp.cantidad
                            ELSE 0
                        END
                    ), 0
                ) AS disponibles
            FROM libro l
            LEFT JOIN detalle_prestamo dp
                ON dp.id_libro = l.id_libro
            LEFT JOIN prestamo p
                ON p.id_prestamo = dp.id_prestamo
            WHERE l.fecha_baja IS NULL
            GROUP BY
                l.id_libro,
                l.titulo,
                l.cantidad_total
            ORDER BY l.titulo
        """

        return self._ejecutar_consulta(consulta)
