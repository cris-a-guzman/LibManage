# Lo de abajo es un mock de como vienen los datos desde la db
# Es un ejemplo para tenerlo de referencia y ver como quedaria
print("Entro en database.py")
class ApiDatabase:
    
    def __init__(self):
        from database.mock_datos import socios, libros, prestamos, detalle_prestamo
        self.socios = socios
        self.libros = libros
        self.prestamos = prestamos
        self.detalle_prestamo = detalle_prestamo
        
    def traer_socio_por_id(self, id_socio):
            return next(
                (socio for socio in self.socios
                if socio.get("id_socio") == id_socio),
                None
            )
        
    def traer_socios(self):
        return self.socios
    
    def traer_prestamos_socio(self, id_socio):
        resultado = []

        for prestamo in self.prestamos:
            if prestamo["id_socio"] != id_socio:
                continue

            libros = []

            for detalle in self.detalle_prestamo:
                if detalle["id_prestamo"] == prestamo["id_prestamo"]:

                    libro = next(
                        (
                            libro for libro in self.libros
                            if libro["id_libro"] == detalle["id_libro"]
                        ),
                        None
                    )

                    if libro:
                        libros.append(libro["titulo"])

            resultado.append({
                "id": prestamo["id_prestamo"],
                "libro": ", ".join(libros),
                "fecha_prestamo": prestamo["fecha_prestamo"],
                "fecha_devolucion_estimada": prestamo["fecha_devolucion_estimada"],
                "fecha_devolucion_real": prestamo["fecha_devolucion_real"],
                "estado": prestamo["estado"]
            })

        return resultado
        
            
        
        

