#Consumidor de api rest django, apiAutores.py, sin permisos (permission_classes = [AllowAny]).
import flet as ft
import requests

def principal(pagina: ft.Page):
    pagina.title = "Consumo API Django"

    def botonClickeado(e):
        # 1. Consumir la API.  Algunos de los atributos y métodos más utilizados del objeto `request` incluyen:
        try:
            respuestaGet = requests.get("http://127.0.0.1:8000/catalogo/apirest/autores/") #Forzamos la negociación de contenido en la renderización condicional de la vista de la api endpoint con el parámetro headers, porque no lo esta agarrando automáticamente.
            respuestaGet_2 = requests.get("http://127.0.0.1:8000/catalogo/apirest/libros/4")
            
        except:
            txt_resultado.value = "hubo un error en conexión"
        else:
        # Algunos de los atributos y métodos más utilizados del objeto Response del modulo requests incluyen:
            #headers
            print("respuestaGet.text:")
            print(respuestaGet.text)
            print("    ***")

            print("respuestaGet.status_code:")
            print(respuestaGet.status_code)
            print("    ***")

            print("respuestaGet.url:")
            print(respuestaGet.url)
            print("    ***")

            print("respuestaGet.headers:")
            print(respuestaGet.headers)
            print("    ***")

            resultadoGet=""
            resultadoGet_2=""

            diccionario = respuestaGet.json() #Analiza el cuerpo de la respuesta como JSON y devuelve un diccionario o lista de Python.
            diccionario_2 = respuestaGet_2.json()
            #print(f'diccionario{diccionario}')
            #Tomamos la cant de autores primero, puesto que vamos a concatenar:
            resultadoGet = f"cantidad de autores:{len(diccionario)}, "

            #Tomamos el primer elemento de results que es una lista de diccionarios:
            listDeDicts = diccionario['results']              

            #Filtramos listDeDicts para extraer los campos deseados de cada uno de los diccionarios que contienen los datos del autor:
            listaFiltrada = [{"id": d["id"], "nombre": d["nombre"], "apellido": d["apellido"], "nacimiento": d["nacimiento"], "muerte": d["muerte"]} for d in listDeDicts]

            #Extraemos los pares clave-valor de la lista de diccionarios y los concatenamos en resultadoGet:
            for diccionario in listaFiltrada:
                for clave, valor in diccionario.items():
                    resultadoGet += f"{clave}: {valor}, "

            # 4. Por último depositamos el string en el atributo value del control:
            txt_resultado.value = resultadoGet
            txt_resultado_2.value = diccionario_2
        
        finally:
            # 5. Claro, finalmente actualizamos la pag para ver los resultados:
            pagina.update()

    txt_resultado = ft.Text()
    txt_resultado_2 = ft.Text()
    btn_cargar = ft.Button("Cargar Datos", on_click=botonClickeado)

    def borrar_texto(e):
        txt_resultado.value = ""  # O texto.value = None
        txt_resultado_2.value = None
        pagina.update()

    pagina.add(btn_cargar, txt_resultado, txt_resultado_2, ft.Button("Borrar", on_click=borrar_texto))

ft.run(principal)