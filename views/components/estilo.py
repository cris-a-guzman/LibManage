import ttkbootstrap as tb

FUENTE = "Segoe UI"
TITULO = (FUENTE, 18, "bold")
SUBTITULO = (FUENTE, 12, "bold")
CUERPO = (FUENTE, 10)
DESTACADO = (FUENTE, 16, "bold")
TEMA = "superhero"


def aplicar_estilos():
    style = tb.Style()
    style.configure("TLabel", font=CUERPO)
    style.configure("TButton", font=(FUENTE, 10, "bold"), padding=(14, 8))
    style.configure("TLabelframe.Label", font=(FUENTE, 10, "bold"))
    style.configure("TEntry", padding=7)
    style.configure("TCombobox", padding=6)
    style.configure(
        "Treeview",
        rowheight=34,
        font=CUERPO,
    )
    style.configure(
        "Treeview.Heading",
        font=(FUENTE, 10, "bold"),
        padding=8,
    )
    style.configure("Metric.TLabel", font=DESTACADO)
    return style
