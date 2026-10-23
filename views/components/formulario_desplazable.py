# Componente reutilizable para formularios más altos que la ventana disponible.
# Un Canvas contiene el Frame real y una barra modifica su posición vertical.
# Referencia: docs/estudio/README.md#tkinter-y-programación-dirigida-por-eventos
import tkinter as tk
from tkinter import ttk


# Frame compuesto que expone `contenido` para que otras vistas agreguen widgets.
class FormularioDesplazable(tk.Frame):

    # Crea Canvas, Scrollbar y Frame interno y enlaza sus eventos de tamaño.
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

    # Recalcula la región recorrible cuando cambia el tamaño del contenido.
    def actualizar_desplazamiento(self, event):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    # Mantiene el Frame interno con el mismo ancho visible que el Canvas.
    def ajustar_ancho(self, event):
        self.canvas.itemconfigure(
            self.ventana,
            width=event.width
        )
