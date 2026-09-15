import tkinter as tk
from views.home_view import HomeView


class login_view(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        tk.Label(self, text="Pantalla de login").pack(fill="x")
        
        label_username = tk.Label(self, text="Ingrese su usuario")
        label_username.pack()
        
        entry_username = tk.Entry(self, width=30)
        entry_username.pack()
        
        label_password = tk.Label(self, text="Ingrese su contraseña")
        label_password.pack()
        
        entry_password = tk.Entry(self, width=30)
        entry_password.pack()
        
        accept_button = tk.Button(self, text="Entrar",command=lambda: controller.show_frame(HomeView))
        accept_button.pack()