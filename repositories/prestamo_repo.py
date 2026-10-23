# Acceso a datos y reglas de registro/devolución de préstamos.
# Este archivo concentra la lógica más sensible: disponibilidad y escritura atómica.
# Referencias: docs/estudio/README.md#persistencia-y-crud y
# docs/estudio/README.md#reglas-de-negocio
from datetime import date
from repositories.base_repository import BaseRepository
from repositories.conexion import obtener_conexion

# Repositorio especializado en préstamos y la relación con sus libros.
class PrestamoRepo(BaseRepository):
    
    # Cuenta préstamos cuyo estado es exactamente `activo`.
    def cantidad_prestamos_activos(self):
        consulta = """
            SELECT count(*) as prestamos_activos FROM prestamo where estado = "activo"
        """
        resultado = self._ejecutar_consulta(consulta)
        print(resultado)
        return resultado[0]['prestamos_activos'] if resultado else 0
    
    # Cuenta estados considerados finalizados por esta consulta.
    # La diferencia con `cerrado_sin_devolver` se documenta en la guía.
    def cantidad_prestamos_finalizados(self):
        consulta = """
            SELECT count(*) as prestamos_finalizados FROM prestamo WHERE estado = 'cerrado' OR estado = 'devuelto'
        """
        resultado = self._ejecutar_consulta(consulta)
        return resultado[0]['prestamos_finalizados'] if resultado else 0
    
    # Cuenta préstamos sin fecha real; el método no compara con la fecha estimada.
    def cantidad_prestamos_atraso(self):
        consulta = """
            SELECT count(*) AS cantidad FROM prestamo where fecha_devolucion_real is null
        """
        resultado = self._ejecutar_consulta(consulta)
        return resultado[0]['cantidad'] if resultado else 0

    # Devuelve filas para el Treeview y, opcionalmente, solo activos vencidos.
    # El booleano se transforma en 0/1 para activar o anular el filtro SQL.
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

    # Marca un préstamo activo como devuelto en la fecha actual.
    # Devuelve True únicamente cuando MySQL modificó una fila.
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
    
    # Adaptador para registrar un ejemplar usando la operación múltiple.
    def crear_prestamo(self, dni_socio, id_libro, fecha_devolucion):
        return self.crear_prestamo_multiple(
            dni_socio=dni_socio,
            libros=[(id_libro, 1)],
            fecha_devolucion=fecha_devolucion
        )


    # Registra varios títulos en una transacción. Recibe DNI, tuplas
    # `(id_libro, cantidad)` y fecha estimada; devuelve el id generado.
    def crear_prestamo_multiple(self, dni_socio, libros, fecha_devolucion):
        # libros: [(id_libro, cantidad), ...]
        if not libros:
            raise ValueError("Debés seleccionar al menos un libro.")

        if fecha_devolucion < date.today():
            raise ValueError("La devolución no puede ser anterior a hoy.")

        # Validar los libros y sus cantidades
        # El diccionario también permite detectar un mismo título repetido.
        seleccion = {}

        for id_libro, cantidad in libros:
            if (
                type(id_libro) is not int
                or id_libro <= 0
                or type(cantidad) is not int
                or cantidad <= 0
            ):
                raise ValueError("Libro o cantidad inválida.")

            if id_libro in seleccion:
                raise ValueError("El mismo libro está repetido.")

            seleccion[id_libro] = cantidad

        conexion = obtener_conexion()

        if conexion is None:
            raise ConnectionError("No se pudo conectar a MySQL")

        cursor = None

        try:
            # Las comprobaciones y escrituras se confirman o revierten como una unidad.
            conexion.start_transaction()
            cursor = conexion.cursor(dictionary=True)

            # Buscar el socio mediante su DNI
            cursor.execute("""
                SELECT id_socio
                FROM socio
                WHERE dni = %s AND fecha_baja IS NULL
                FOR UPDATE
            """, (dni_socio,))

            socio = cursor.fetchone()

            if socio is None:
                raise ValueError("El socio no existe o está dado de baja.")

            # Bloquear todos los libros en un orden fijo
            # Se bloquean filas en orden fijo para leer existencias estables.
            existencias = {}

            for id_libro in sorted(seleccion):
                cursor.execute("""
                    SELECT cantidad_total
                    FROM libro
                    WHERE id_libro = %s
                      AND fecha_baja IS NULL
                    FOR UPDATE
                """, (id_libro,))

                libro = cursor.fetchone()

                if libro is None:
                    raise ValueError(
                        f"El libro {id_libro} no está disponible."
                    )

                existencias[id_libro] = libro["cantidad_total"]

            # Verificar disponibilidad de cada libro
            for id_libro, cantidad in seleccion.items():
                cursor.execute("""
                    SELECT COALESCE(SUM(dp.cantidad), 0) AS ocupados
                    FROM detalle_prestamo dp
                    JOIN prestamo p
                        ON dp.id_prestamo = p.id_prestamo
                    WHERE dp.id_libro = %s
                      AND p.estado IN (
                          'activo',
                          'cerrado_sin_devolver'
                      )
                """, (id_libro,))

                # La disponibilidad se recalcula dentro de la transacción.
                ocupados = cursor.fetchone()["ocupados"]
                disponibles = existencias[id_libro] - ocupados

                if cantidad > disponibles:
                    raise ValueError(
                        f"El libro {id_libro} tiene "
                        f"{disponibles} ejemplares disponibles."
                    )

            # Crear la cabecera del préstamo
            cursor.execute("""
                INSERT INTO prestamo (
                    id_socio,
                    fecha_prestamo,
                    fecha_devolucion_estimada,
                    estado
                )
                VALUES (%s, CURDATE(), %s, 'activo')
            """, (socio["id_socio"], fecha_devolucion))

            # La clave generada enlaza la cabecera con cada detalle posterior.
            id_prestamo = cursor.lastrowid

            # Registrar todos los libros asociados
            for id_libro, cantidad in seleccion.items():
                cursor.execute("""
                    INSERT INTO detalle_prestamo (
                        id_prestamo,
                        id_libro,
                        cantidad
                    )
                    VALUES (%s, %s, %s)
                """, (id_prestamo, id_libro, cantidad))

            conexion.commit()
            return id_prestamo

        except Exception:
            conexion.rollback()
            raise

        finally:
            if cursor is not None:
                cursor.close()
            conexion.close()

