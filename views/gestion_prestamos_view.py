import tkinter as tk
from tkinter import ttk

class GestionPrestamos(tk.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        tk.Label(
            self,
            text="Pantalla Gestion Préstamos"
        ).grid(row=0, column=0, sticky="ew")
        
        self.rowconfigure(1, weight=1)