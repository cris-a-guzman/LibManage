from repositories.conexion import obtener_conexion


def listar_libros():
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError("No se pudo conectar a MySQL")

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
            SELECT id_libro, isbn, titulo, autor, anio, cantidad_total
            FROM libro
            WHERE fecha_baja IS NULL
            ORDER BY titulo
        """)

        libros = cursor.fetchall()
        return libros

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()





def crear_libro(titulo, autor, anio, cantidad_total):
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError("No se pudo conectar a MySQL")

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            INSERT INTO libro (titulo, autor, anio, cantidad_total)
            VALUES (%s, %s, %s, %s)
        """

        datos = (titulo, autor, anio, cantidad_total)

        cursor.execute(consulta, datos)
        conexion.commit()

        return cursor.lastrowid

    except Exception:
        conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()






def actualizar_libro(id_libro, titulo, autor, anio, cantidad_total):
    conexion = obtener_conexion()

    if conexion is None:
        raise ConnectionError("No se pudo conectar a MySQL")

    cursor = None

    try:
        cursor = conexion.cursor()

        consulta = """
            UPDATE libro
            SET titulo = %s,
                autor = %s,
                anio = %s,
                cantidad_total = %s
            WHERE id_libro = %s
        """

        datos = (titulo, autor, anio, cantidad_total, id_libro)

        cursor.execute(consulta, datos)
        conexion.commit()

    except Exception:
        conexion.rollback()
        raise

    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()