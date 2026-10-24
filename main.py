import tkinter as tk
from views.components.main_window import MainWindow

def main():
    """Esta funcion ejecuta el programa entero"""
    app = MainWindow() #* Esto crea la ventana principal del programa
    app.mainloop()
    
if __name__ == "__main__":
    """Manda a ejecutar la funcion main() solo si el archivo desde
    cual se ejecuta es main.py"""
    main()
    