import ttkbootstrap as tb
from ttkbootstrap.constants import *

class AutocompleteCombobox(tb.Combobox):
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
