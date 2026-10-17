
import tkinter as tk
from tkinter import ttk


class FormularioDesplazable(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(
            self,
            highlightthickness=0
        )

        barra = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview
        )

        self.contenido = tk.Frame(self.canvas)

        self.ventana = self.canvas.create_window(
            (0, 0),
            window=self.contenido,
            anchor="nw"
        )

        self.contenido.bind(
            "<Configure>",
            self.actualizar_desplazamiento
        )

        self.canvas.bind(
            "<Configure>",
            self.ajustar_ancho
        )

        self.canvas.configure(
            yscrollcommand=barra.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        barra.pack(
            side="right",
            fill="y"
        )

    def actualizar_desplazamiento(self, event):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def ajustar_ancho(self, event):
        self.canvas.itemconfigure(
            self.ventana,
            width=event.width
        )
