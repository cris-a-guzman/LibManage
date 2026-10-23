# Pantalla inicial de autenticación visual.
# En la versión principal los campos no se validan: el botón siempre navega al inicio.
# Esta diferencia con una autenticación real se documenta en la guía de estudio.
import tkinter as tk
from views.home_view.home_view import HomeView


# Frame independiente que recibe el controlador para cambiar a HomeView.
class login_view(tk.Frame):
    
    # Crea etiquetas, entradas y el callback del botón Entrar.
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Pantalla de login").pack(fill="x")
        
        label_username = tk.Label(self, text="Ingrese su usuario")
        label_username.pack()
        
        entry_username = tk.Entry(self, width=30)
        entry_username.pack()
        
        label_password = tk.Label(self, text="Ingrese su contraseña")
        label_password.pack()
        
        entry_password = tk.Entry(self, width=30, show="*")
        entry_password.pack()
        
        accept_button = tk.Button(self, text="Entrar",command=lambda: controller.show_frame(HomeView))
        accept_button.pack()