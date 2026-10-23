# Funciones comunes de acceso a MySQL para los repositorios del dominio.
# Centraliza el ciclo de vida del cursor y el cierre de una lectura o escritura,
# pero deja que LibroRepo, PrestamoRepo y SociosRepo definan cada consulta.
# Referencia de estudio: docs/estudio/README.md#persistencia-y-crud

# Superclase que guarda una conexión y ofrece operaciones protegidas reutilizables.
class BaseRepository:
    
    # Recibe una conexión abierta; las subclases la reutilizan en consultas simples.
    def __init__(self, conexion):
        self.conexion = conexion
        
    # Ejecuta una lectura parametrizada y permite elegir una o varias filas.
    # `dictionary=True` permite consultar cada columna por su nombre.
    def _ejecutar_consulta(self, consulta, params=None, dictionary=True, fetchall=True, fetchone=False):
        """Metodo para las consultas SELECT"""
        cursor = self.conexion.cursor(dictionary=dictionary)
        try:
            cursor.execute(consulta, params or ())
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()
        finally:
            cursor.close()

    # Ejecuta una modificación y devuelve filas afectadas e identificador generado.
    # Confirma con commit o revierte con rollback si ocurre una excepción.
    def _ejecutar_escritura(self, consulta, params=None):
        """Método auxiliar para INSERT / UPDATE / DELETE"""
        cursor = self.conexion.cursor()
        try:
            cursor.execute(consulta, params or ())
            self.conexion.commit()
            return {
                "rowcount": cursor.rowcount,
                "lastrowid": cursor.lastrowid
            }
        except Exception:
            self.conexion.rollback()
            raise
        finally:
            cursor.close()