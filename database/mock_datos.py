
#! Esto tenemos que eliminarlo cuando hagamos la conexion a sqlite
#! Tambien pudimos haber usado un json pero igual lo vamos a borrar

socios = [
    {
        "id_socio": 1,
        "dni": 23147884,
        "nombre": "Mirtha",
        "apellido": "LeGrand"
    },
    {
        "id_socio": 2,
        "dni": 28456732,
        "nombre": "Carlos",
        "apellido": "Gómez"
    },
    {
        "id_socio": 3,
        "dni": 31984567,
        "nombre": "Lucía",
        "apellido": "Fernández"
    },
    {
        "id_socio": 4,
        "dni": 26743129,
        "nombre": "Martín",
        "apellido": "Rodríguez"
    },
    {
        "id_socio": 5,
        "dni": 35421678,
        "nombre": "Sofía",
        "apellido": "Martínez"
    },
    {
        "id_socio": 6,
        "dni": 29876543,
        "nombre": "Diego",
        "apellido": "Pérez"
    },
    {
        "id_socio": 7,
        "dni": 32654981,
        "nombre": "Valentina",
        "apellido": "López"
    },
    {
        "id_socio": 8,
        "dni": 25134879,
        "nombre": "Julián",
        "apellido": "Sánchez"
    },
    {
        "id_socio": 9,
        "dni": 37482156,
        "nombre": "Camila",
        "apellido": "Torres"
    },
    {
        "id_socio": 10,
        "dni": 28943167,
        "nombre": "Federico",
        "apellido": "Ramírez"
    },
    {
        "id_socio": 11,
        "dni": 33571249,
        "nombre": "Agustina",
        "apellido": "Díaz"
    },
    {
        "id_socio": 12,
        "dni": 27654321,
        "nombre": "Nicolás",
        "apellido": "Herrera"
    }
]

libros = [
    {
        "id_libro": 1,
        "isbn": "9789507300011",
        "titulo": "El Aleph",
        "autor": "Jorge Luis Borges",
        "anio": 1949,
        "cantidad_total": 5
    },
    {
        "id_libro": 2,
        "isbn": "9788420412146",
        "titulo": "1984",
        "autor": "George Orwell",
        "anio": 1949,
        "cantidad_total": 8
    },
    {
        "id_libro": 3,
        "isbn": "9788437604947",
        "titulo": "Cien años de soledad",
        "autor": "Gabriel García Márquez",
        "anio": 1967,
        "cantidad_total": 6
    },
    {
        "id_libro": 4,
        "isbn": "9789505110018",
        "titulo": "Rayuela",
        "autor": "Julio Cortázar",
        "anio": 1963,
        "cantidad_total": 4
    },
    {
        "id_libro": 5,
        "isbn": "9788420428659",
        "titulo": "El principito",
        "autor": "Antoine de Saint-Exupéry",
        "anio": 1943,
        "cantidad_total": 10
    },
    {
        "id_libro": 6,
        "isbn": "9789500726350",
        "titulo": "Martín Fierro",
        "autor": "José Hernández",
        "anio": 1872,
        "cantidad_total": 7
    },
    {
        "id_libro": 7,
        "isbn": "9788497592208",
        "titulo": "Fahrenheit 451",
        "autor": "Ray Bradbury",
        "anio": 1953,
        "cantidad_total": 5
    },
    {
        "id_libro": 8,
        "isbn": "9789871138141",
        "titulo": "Crónica de una muerte anunciada",
        "autor": "Gabriel García Márquez",
        "anio": 1981,
        "cantidad_total": 4
    },
    {
        "id_libro": 9,
        "isbn": "9788420664194",
        "titulo": "Don Quijote de la Mancha",
        "autor": "Miguel de Cervantes",
        "anio": 1605,
        "cantidad_total": 6
    },
    {
        "id_libro": 10,
        "isbn": "9789504910176",
        "titulo": "La sombra del viento",
        "autor": "Carlos Ruiz Zafón",
        "anio": 2001,
        "cantidad_total": 5
    }
]

prestamos = [
    {
        "id_prestamo": 1,
        "id_socio": 1,
        "fecha_prestamo": "2026-09-20",
        "fecha_devolucion_estimada": "2026-10-04",
        "fecha_devolucion_real": None,
        "estado": "vencido",
        "observaciones": "El socio aún no realizó la devolución."
    },
    {
        "id_prestamo": 2,
        "id_socio": 1,
        "fecha_prestamo": "2026-08-10",
        "fecha_devolucion_estimada": "2026-08-24",
        "fecha_devolucion_real": "2026-08-22",
        "estado": "devuelto",
        "observaciones": None
    },
    {
        "id_prestamo": 3,
        "id_socio": 2,
        "fecha_prestamo": "2026-09-28",
        "fecha_devolucion_estimada": "2026-10-12",
        "fecha_devolucion_real": None,
        "estado": "activo",
        "observaciones": None
    },
    {
        "id_prestamo": 4,
        "id_socio": 3,
        "fecha_prestamo": "2026-07-05",
        "fecha_devolucion_estimada": "2026-07-19",
        "fecha_devolucion_real": "2026-07-18",
        "estado": "devuelto",
        "observaciones": "Devuelto en buen estado."
    },
    {
        "id_prestamo": 5,
        "id_socio": 3,
        "fecha_prestamo": "2026-09-15",
        "fecha_devolucion_estimada": "2026-09-29",
        "fecha_devolucion_real": None,
        "estado": "vencido",
        "observaciones": "Se notificó al socio."
    },
    {
        "id_prestamo": 6,
        "id_socio": 5,
        "fecha_prestamo": "2026-09-30",
        "fecha_devolucion_estimada": "2026-10-14",
        "fecha_devolucion_real": None,
        "estado": "activo",
        "observaciones": None
    },
    {
        "id_prestamo": 7,
        "id_socio": 7,
        "fecha_prestamo": "2026-08-01",
        "fecha_devolucion_estimada": "2026-08-15",
        "fecha_devolucion_real": "2026-08-14",
        "estado": "devuelto",
        "observaciones": None
    },
    {
        "id_prestamo": 8,
        "id_socio": 7,
        "fecha_prestamo": "2026-09-25",
        "fecha_devolucion_estimada": "2026-10-09",
        "fecha_devolucion_real": None,
        "estado": "activo",
        "observaciones": "Renovación autorizada."
    },
    {
        "id_prestamo": 9,
        "id_socio": 8,
        "fecha_prestamo": "2026-06-10",
        "fecha_devolucion_estimada": "2026-06-24",
        "fecha_devolucion_real": None,
        "estado": "cerrado_sin_devolver",
        "observaciones": "El libro fue declarado como no devuelto."
    },
    {
        "id_prestamo": 10,
        "id_socio": 11,
        "fecha_prestamo": "2026-09-29",
        "fecha_devolucion_estimada": "2026-10-13",
        "fecha_devolucion_real": None,
        "estado": "activo",
        "observaciones": None
    },
    {
        "id_prestamo": 11,
        "id_socio": 11,
        "fecha_prestamo": "2026-08-05",
        "fecha_devolucion_estimada": "2026-08-19",
        "fecha_devolucion_real": "2026-08-21",
        "estado": "devuelto",
        "observaciones": "Devuelto con demora."
    },
    {
        "id_prestamo": 12,
        "id_socio": 12,
        "fecha_prestamo": "2026-09-10",
        "fecha_devolucion_estimada": "2026-09-24",
        "fecha_devolucion_real": None,
        "estado": "vencido",
        "observaciones": "Pendiente de devolución."
    }
]

detalle_prestamo = [
    {
        "id_prestamo": 1,
        "id_libro": 3,
        "cantidad": 1
    },
    {
        "id_prestamo": 2,
        "id_libro": 5,
        "cantidad": 1
    },
    {
        "id_prestamo": 3,
        "id_libro": 2,
        "cantidad": 1
    },
    {
        "id_prestamo": 3,
        "id_libro": 7,
        "cantidad": 1
    },
    {
        "id_prestamo": 4,
        "id_libro": 1,
        "cantidad": 1
    },
    {
        "id_prestamo": 5,
        "id_libro": 4,
        "cantidad": 1
    },
    {
        "id_prestamo": 6,
        "id_libro": 8,
        "cantidad": 1
    },
    {
        "id_prestamo": 7,
        "id_libro": 6,
        "cantidad": 1
    },
    {
        "id_prestamo": 8,
        "id_libro": 2,
        "cantidad": 1
    },
    {
        "id_prestamo": 8,
        "id_libro": 9,
        "cantidad": 1
    },
    {
        "id_prestamo": 9,
        "id_libro": 10,
        "cantidad": 1
    },
    {
        "id_prestamo": 10,
        "id_libro": 3,
        "cantidad": 1
    },
    {
        "id_prestamo": 11,
        "id_libro": 5,
        "cantidad": 1
    },
    {
        "id_prestamo": 12,
        "id_libro": 7,
        "cantidad": 1
    }
]