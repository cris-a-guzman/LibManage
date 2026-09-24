import json
import requests


class LibraryApi:

    def __init__(self):
        self.URL = "https://openlibrary.org/search.json"

    def buscar_titulo(self):
        nombre_libro = input("Ingresa el nombre del libro: ")

        params = {
            "q": nombre_libro,
            "fields": "key,title,author_name,isbn",
            "limit": 10,
        }

        x = requests.get(self.URL, params=params)

        print(x)
        print(x.url)

        libro_limpio = self.encontrados(x.json())

        if libro_limpio:
            with open(f"{nombre_libro}.json", "w", encoding="utf-8") as file:
                json.dump(libro_limpio, file, indent=4, ensure_ascii=False)
            print(f"Libro guardado exitosamente en {nombre_libro}.json")

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


        return {
            "key": doc_busqueda.get("key"),
            "title": doc_busqueda.get("title"),
            "authors": doc_busqueda.get("author_name", ["Desconocido"]),
            "isbns": doc_busqueda.get("isbn", [])[:5]
        }


api = LibraryApi()
api.buscar_titulo()