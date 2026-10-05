# Lo de abajo es un mock de como vienen los datos desde la db
# Es un ejemplo para tenerlo de referencia y ver como quedaria

class ApiDatabase:
    
    def __init__(self):
        pass
    
    def traer_socios(self):
        self.socios = [
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
        
        return self.socios

