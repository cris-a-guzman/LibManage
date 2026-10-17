
class BaseRepository:
    
    def __init__(self, conexion):
        self.conexion = conexion
        
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