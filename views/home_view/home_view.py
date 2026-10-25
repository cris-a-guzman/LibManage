import ttkbootstrap as tb
from ttkbootstrap.constants import *
from views.libros_views.gestion_libros_view import GestionLibros
from views.prestamos_views.gestion_prestamos_view import GestionPrestamos
from views.socio_views.gestion_socios_view import GestionSocios
from views.components.base_frame import BaseFrame
from views.components.estilo import SUBTITULO, CUERPO, DESTACADO


class HomeView(BaseFrame):

    def __init__(self, parent, controller, conexion):
        super().__init__(parent, controller, conexion)
        
        datos_libro = [
            ("Cantidad de Libros:", self.ApiLibros.cantidad_total_ejemplares()),
            ("Libros Prestados:", (self.ApiLibros.cantidad_ejemplares_prestados())),
            ("Libros Disponibles:", (self.ApiLibros.cantidad_total_ejemplares() - self.ApiLibros.cantidad_ejemplares_prestados())),
        ]
        
        
        datos_prestamos = [
            ("Prestamos Activos:", self.ApiPrestamos.cantidad_prestamos_activos()),
            ("Prestamos Finalizados:", self.ApiPrestamos.cantidad_prestamos_finalizados()),
            ("Prestamos Con Atraso:", self.ApiPrestamos.cantidad_prestamos_atraso()),
        ]
        
        datos_socios = [ 
            ("Cantidad de Socios:", self.ApiSocios.cantidad_socios()),
            ("Socios Con Prestamos:", self.ApiSocios.cantidad_socios_prestamos())
            ]
        
        self.crear_titulo("Inicio")
        
        self.frame_central.columnconfigure((0,1,2), weight=1)
        self.frame_central.rowconfigure(2, weight=1)
        
        tb.Button(
            self.frame_central,
            text="Gestión de Libros",
            padding=(22, 18),
            bootstyle=PRIMARY,
            command=lambda: controller.show_frame(GestionLibros)
        ).grid(row=0, column=0, padx=12, pady=(8, 14), sticky="ew")
        
        tb.Button(
            self.frame_central,
            text="Gestión de Préstamos",
            padding=(22, 18),
            bootstyle=INFO,
            command=lambda: controller.show_frame(GestionPrestamos)
        ).grid(row=0, column=1, padx=12, pady=(8, 14), sticky="ew")
        
        tb.Button(
            self.frame_central,
            text="Gestión de Socios",
            padding=(22, 18),
            bootstyle=SUCCESS,
            command=lambda: controller.show_frame(GestionSocios)
        ).grid(row=0, column=2, padx=12, pady=(8, 14), sticky="ew")
        
        self.subtitulo = tb.Label(
            self.frame_central,
            text="Resumen",
            font=SUBTITULO,
            bootstyle=PRIMARY
        )
        self.subtitulo.grid(row=1, column=0, columnspan=3, sticky="w", padx=12, pady=(4, 8)) 
        
        self.tree_libros = self.crear_tree(self.frame_central, 0, "Libros", PRIMARY)
        self.renderizar_datos(datos_libro, self.tree_libros)
        
        self.tree_prestamos = self.crear_tree(self.frame_central, 1, "Préstamos", INFO)
        self.renderizar_datos(datos_prestamos, self.tree_prestamos)
        
        self.tree_socios = self.crear_tree(self.frame_central, 2, "Socios", SUCCESS)
        self.renderizar_datos(datos_socios, self.tree_socios)        
        
    def crear_tree(self, frame_parent, col, titulo, estilo):
        tarjeta = tb.Labelframe(
            frame_parent,
            text=titulo,
            padding=16,
            bootstyle=estilo
        )
        tarjeta.grid(row=2, column=col, padx=12, pady=8, sticky="nsew")
        return tarjeta

    def renderizar_datos(self, datos, tree):
        for clave, valor in datos:
            fila = tb.Frame(tree)
            fila.pack(fill="x", pady=8)
            tb.Label(fila, text=clave, font=CUERPO).pack(side="left")
            tb.Label(
                fila,
                text=str(valor),
                font=DESTACADO,
                bootstyle=PRIMARY
            ).pack(side="right")
