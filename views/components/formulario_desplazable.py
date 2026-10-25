
import ttkbootstrap as tb
from ttkbootstrap.constants import *



class FormularioDesplazable(tb.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        colores = tb.Style().colors
        self.canvas = tb.Canvas(
            self,
            highlightthickness=0,
            background=colores.bg,
            borderwidth=0
        )

        barra = tb.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            bootstyle="round"
        )

        self.contenido = tb.Frame(self.canvas)

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
