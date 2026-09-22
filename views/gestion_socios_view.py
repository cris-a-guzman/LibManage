import tkinter as tk
from tkinter import ttk

class GestionSocios(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        tk.Label(
            self,
            text="Pantalla Gestion Socios"
        ).grid(row=0, column=0, sticky="ew")
        
        self.rowconfigure(1, weight=1)