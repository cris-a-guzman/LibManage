import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from repositories.conexion import obtener_conexion
from views.home_view.home_view import HomeView
from views.components.estilo import TEMA, TITULO, CUERPO, aplicar_estilos

class MainWindow(tb.Window):
    
    def __init__(self):
        super().__init__(themename=TEMA)
        aplicar_estilos()
        
        self.title("LibManage")
        self.centrar_pantalla()
        self.minsize(980, 640)
        self.resizable(True, True)
        
        try:
            self.conexion = obtener_conexion()
        except ConnectionError as e:

            Messagebox.show_error(
                f"No se pudo establecer la conexión a la base de datos.\n\nDetalle técnico: {e}",
                title="Error Crítico de Conexión"
            )
            self.destroy() 
            return
        
        self._crear_header()
        

        self.container = tb.Frame(self, padding=8)

        self.container.pack(fill="both", expand=True, padx=18, pady=(12, 18)) 
        
        self.show_frame(HomeView)
        
    def show_frame(self, frame_class, datos=None):
        for widget in self.container.winfo_children():
            widget.destroy()
        
        if datos is not None:
            frame = frame_class(self.container, self, self.conexion, datos)
        else:
            frame = frame_class(self.container, self, self.conexion)
            
        frame.pack(fill="both", expand=True)
        
    def _crear_header(self):

        header = tb.Frame(self, bootstyle=PRIMARY)
        header.pack(fill="x")
        
        tb.Label(
            header,
            text="LibManage", 
            font=TITULO,
            bootstyle="inverse-primary"
        ).pack(pady=(14, 2))
        
        tb.Label(
            header,
            text="Gestor de Libros y Préstamos",
            font=CUERPO,
            bootstyle="inverse-primary"
        ).pack(pady=(0, 14))
        
    def centrar_pantalla(self):
        ancho = 1100 
        alto = 720
        ancho_pantalla = self.winfo_screenwidth() 
        alto_pantalla = self.winfo_screenheight() 

        x = (ancho_pantalla - ancho) // 2 
        y = (alto_pantalla - alto) // 2 
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
