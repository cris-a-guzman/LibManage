import requests

class LibraryApi:
    def __init__(self):
        self.URL = "https://openlibrary.org/search.json"

    def buscar_titulo(self, nombre_libro):
        params = {
            "q": nombre_libro,
            "fields": "key,title,author_name,isbn,first_publish_year",
            "limit": 10,
        }

        try:
            x = requests.get(self.URL, params=params, timeout=5)
            x.raise_for_status()
            return self.encontrados2(x.json())
        except requests.RequestException as e:
            print(f"Error de conexión en búsqueda: {e}")
            return None, None 

    def funcion_final(self, id, datos):
        if not datos or id >= len(datos):
            return ("", "", "", "")
            
        doc_seleccionado = datos[id]
        key = doc_seleccionado.get('key', '')
        url_detalle = f"https://openlibrary.org{key}.json"

        try:
            respuesta_work = requests.get(url_detalle, timeout=5)
            respuesta_work.raise_for_status()
            detalle_work = respuesta_work.json()
        except requests.RequestException as e:
            print(f"Error de conexión en detalle: {e}")
            detalle_work = {}

        data = self.limpiar_datos_libro(doc_seleccionado, detalle_work)
        return data  
    
    def encontrados2(self, datos):
        docs = datos.get("docs", [])
        if not docs:
            return None, None
        
        datos_libros = []
        for idx, i in enumerate(docs):
            autores = ", ".join(i.get("author_name", ["Desconocido"]))
            datos_libros.append({
                "autor": autores,
                "titulo": i.get("title", ""),
                "id": idx,
                "año": i.get("first_publish_year", "")
            })
        return datos_libros, docs

    def limpiar_datos_libro(self, doc_busqueda, detalle_work=None):
        titulo = str(doc_busqueda.get("title", ""))
        autores = ", ".join(doc_busqueda.get("author_name", ["Desconocido"]))
        
        isbns = doc_busqueda.get("isbn", [])
        isbn = str(isbns[0]) if isbns else ""
        
        anio = str(doc_busqueda.get("first_publish_year", ""))
        

        return (titulo, autores, isbn, anio)