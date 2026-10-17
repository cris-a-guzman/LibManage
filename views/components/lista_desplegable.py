import tkinter as tk
from tkinter import ttk

class AutocompleteCombobox(ttk.Combobox):
    def set_completion_list(self, lista_opciones):
        """Establece la lista completa de opciones."""
        self._lista_completa = sorted(lista_opciones, key=str.lower)
        self['values'] = self._lista_completa

        self.bind('<Return>', self._filtrar_opciones)

    def _filtrar_opciones(self, event):
        """Filtra las opciones del desplegable según el texto ingresado."""

        if event.keysym in ("Up", "Down", "Escape", "Tab", "Right", "Left"):
            return

        texto_ingresado = self.get().strip().lower()

        if texto_ingresado == '':
            # Si borra todo, muestra la lista completa
            self['values'] = self._lista_completa
        else:
            # Filtra las opciones que COMIENZAN con el texto ingresado
            filtrados = [
                item for item in self._lista_completa 
                if item.lower().startswith(texto_ingresado)
            ]
            self['values'] = filtrados

        # Despliega automáticamente la lista si hay coincidencias
        if self['values']:
            self.event_generate('<Down>')


    # def on_focus_in(event):
    # # Si el texto actual es el placeholder, lo borramos y cambiamos el texto a negro
    #     if self.busqueda_libro.get() == PLACEHOLDER:
    #         self.busqueda_libro.delete(0, tk.END)
    #         self.busqueda_libro.configure(foreground="black")

    # def on_focus_out(event):
    #     # Si el usuario hace clic fuera y dejó el campo vacío, restauramos el placeholder
    #     if not self.busqueda_libro.get().strip():
    #         self.busqueda_libro.insert(0, PLACEHOLDER)
    #         self.busqueda_libro.configure(foreground="gray")

    # def on_key_release(event):
    #     # Ignorar teclas de navegación
    #     if event.keysym in ("Up", "Down", "Return", "Escape", "Tab", "Right", "Left"):
    #         return

    #     texto = self.busqueda_libro.get().strip().lower()

    #     if not texto or texto == PLACEHOLDER.lower():
    #         self.busqueda_libro['values'] = titulos_libros
    #     else:
    #         # Filtrar títulos que contengan o empiecen con lo escrito
    #         filtrados = [lib for lib in titulos_libros if texto in lib.lower()]
    #         self.busqueda_libro['values'] = filtrados