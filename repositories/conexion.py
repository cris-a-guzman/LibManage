import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

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
        raise ConnectionError(f"No se pudo conectar a la base de datos MySQL:\n{e}")
