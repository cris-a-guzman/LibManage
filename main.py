# Punto de entrada de LibManage.
# Este módulo crea la ventana principal definida en `views/components/main_window.py`
# y entrega el control a Tkinter mediante su bucle de eventos.
# Referencia de estudio: docs/estudio/README.md#programación-modular
import tkinter as tk
from views.components.main_window import MainWindow

# Crea el objeto raíz de la interfaz; no recibe datos ni devuelve un resultado.
def main():
    app = MainWindow()
    app.mainloop()
    
# Esta condición distingue la ejecución directa de la importación como módulo.
if __name__ == "__main__":
    main()
    