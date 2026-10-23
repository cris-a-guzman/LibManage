# Configuración de la conexión de LibManage con MySQL.
# Los datos sensibles se leen del entorno mediante `.env`; no se escriben en el código.
# Referencia de estudio: docs/estudio/README.md#persistencia-y-crud
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

# Intenta construir y devolver una conexión. Si MySQL rechaza la operación,
# informa el error por consola y devuelve None para que el llamador pueda decidir.
def obtener_conexion():
    """Establece y devuelve una conexión directa con MySQL."""
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "usuario_sistema"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "libmanage")
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
