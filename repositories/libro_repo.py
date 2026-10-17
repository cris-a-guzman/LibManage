# repositories/libro_repository.py
from repositories.base_repository import BaseRepository

class LibroRepo(BaseRepository):

    def listar_libros(self):
        consulta = """
            SELECT id_libro, isbn, titulo, autor, anio, cantidad_total
            FROM libro
            WHERE fecha_baja IS NULL
            ORDER BY titulo
        """
        return self._ejecutar_consulta(consulta)

    def crear_libro(self, titulo, autor, anio, cantidad_total):
        consulta = """
            INSERT INTO libro (titulo, autor, anio, cantidad_total)
            VALUES (%s, %s, %s, %s)
        """
        resultado = self._ejecutar_escritura(consulta, (titulo, autor, anio, cantidad_total))
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