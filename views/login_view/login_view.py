import ttkbootstrap as tb
from ttkbootstrap.constants import *
from views.home_view.home_view import HomeView
from views.components.estilo import TITULO, CUERPO


class login_view(tb.Frame):
    
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        tarjeta = tb.Labelframe(
            self,
            text="Acceso",
            padding=28,
            bootstyle=PRIMARY
        )
        tarjeta.grid(row=0, column=0)

        tb.Label(
            tarjeta,
            text="LibManage",
            font=TITULO,
            bootstyle=PRIMARY
        ).pack(pady=(0, 6))

        tb.Label(
            tarjeta,
            text="Ingresá tus credenciales",
            font=CUERPO,
            bootstyle=SECONDARY
        ).pack(pady=(0, 18))
        
        tb.Label(tarjeta, text="Usuario").pack(anchor="w")
        entry_username = tb.Entry(tarjeta, width=32, bootstyle=PRIMARY)
        entry_username.pack(fill="x", pady=(4, 12), ipady=6)
        
        tb.Label(tarjeta, text="Contraseña").pack(anchor="w")
        entry_password = tb.Entry(tarjeta, width=32, show="*", bootstyle=PRIMARY)
        entry_password.pack(fill="x", pady=(4, 18), ipady=6)
        
        tb.Button(
            tarjeta,
            text="Entrar",
            bootstyle=SUCCESS,
            command=lambda: controller.show_frame(HomeView)
        ).pack(fill="x", ipady=8)
