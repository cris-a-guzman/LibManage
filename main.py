import subprocess
import sys

try:
    import mysql.connector
    import dotenv
    import requests
except ImportError:
    print("Dependencias faltantes detectadas. Instalando desde requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Instalación completada. Iniciando sistema...")
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar instalar las dependencias: {e}")
        sys.exit(1)
        
import tkinter as tk
from views.components.main_window import MainWindow

def main():
    app = MainWindow()
    app.mainloop()
    
if __name__ == "__main__":
    main()
    