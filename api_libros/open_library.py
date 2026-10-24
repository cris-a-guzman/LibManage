import json
import requests

#! TIENE QUE DEVOLVER ("Titulo", "Autor", "ISBN", "AÑO")

class LibraryApi:

    def __init__(self):
        self.URL = "https://openlibrary.org/search.json"

    def buscar_titulo(self, nombre_libro):

        params = {
            "q": nombre_libro,
            "fields": "key,title,author_name,isbn,first_publish_year",
            "limit": 10,
        }

        x = requests.get(self.URL, params=params)

        print(x)
        print(x.url)
        
        encontrado =  self.encontrados2(x.json())
        return encontrado
    
        libro_limpio = self.encontrados(x.json())

        return libro_limpio
    
    def funcion_final(self, id, datos):
        doc_seleccionado = datos[id]

        url_detalle = f"https://openlibrary.org{doc_seleccionado['key']}.json"
        respuesta_work = requests.get(url_detalle)

        detalle_work = (
            respuesta_work.json() if respuesta_work.status_code == 200 else {}
        )

        data = self.limpiar_datos_libro(doc_seleccionado, detalle_work)
        print(data)
        return data  
    
    def encontrados2(self, datos):
        docs = datos.get("docs",[])
        if not docs:
            return None
        
        datos_libros = []
        
        for idx, i in enumerate(docs):
            autores = ", ".join(i.get("author_name", ["Desconocido"]))
            datos_libros.append({
                "autor":autores,
                "titulo": i.get("title"),
                "id":idx,
                "año":i.get("first_publish_year")
            })
        print(datos_libros)
        return datos_libros, docs
        
    def encontrados(self, datos):
        docs = datos.get("docs", [])

        if not docs:
            print("No se encontraron libros.")
            return None

        for idx, i in enumerate(docs):
            autores = ", ".join(i.get("author_name", ["Desconocido"]))
            print(f"{idx} Autor: {autores} - Titulo: {i.get('title')}")

        elegido = int(
            input("\nIngresa el numero del libro al que queres acceder: ")
        )
        doc_seleccionado = docs[elegido]

        url_detalle = f"https://openlibrary.org{doc_seleccionado['key']}.json"
        respuesta_work = requests.get(url_detalle)

        detalle_work = (
            respuesta_work.json() if respuesta_work.status_code == 200 else {}
        )

        data = self.limpiar_datos_libro(doc_seleccionado, detalle_work)
        return data  

    def limpiar_datos_libro(self, doc_busqueda, detalle_work=None):
        
        datos = {"key": doc_busqueda.get("key"),
                    "titulo": doc_busqueda.get("title"),
                    "autor": doc_busqueda.get("author_name", ["Desconocido"]),
                    "isbn": doc_busqueda.get("isbn", [])[0],
                    "año": doc_busqueda.get("first_publish_year")
        }
        print(datos)
        return datos

# API = LibraryApi()

# API.buscar_titulo("harry potter")