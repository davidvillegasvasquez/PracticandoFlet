#Consumidor de api rest django, fletDrfClient.py
import flet as ft
import requests

def principal(pagina: ft.Page):
    pagina.title = "Consumo API Django"

    def botonClickeado(e):
        # 1. Consumir la API
        try:
            respuesta = requests.get("http://127.0.0.1:8000/catalogo/api-todosLosAutores/")
        except:
            txt_resultado.value = "hubo un error en conexión"
        else:
            resultado=""
            data = respuesta.json()

            # 2. Convertimos el json a dict
            diccionario = dict(data)

            #Tomamos la cant de autores primero, puesto que vamos a concatenar:
            resultado = f"cantidad de autores:{diccionario['count']}, "

            #Tomamos el primer elemento de results que es una lista de diccionarios:
            listDeDicts = diccionario['results']  

            #Filtramos listDeDict para extraer los campos deseados de cada uno de los diccionarios que contienen los datos del autor:
            listaFiltrada = [{"id": d["id"], "nombre": d["nombre"], "apellido": d["apellido"], "nacimiento": d["nacimiento"], "muerte": d["muerte"]} for d in listDeDicts]

            #Extraemos los pares clave-valor de la lista de diccionarios y los concatenamos en resultado:
            for diccionario in listaFiltrada:
                for clave, valor in diccionario.items():
                    resultado += f"{clave}: {valor}, "

            # 4. Por último depositamos el string en el atributo value del control:
            txt_resultado.value = resultado
        
        finally:
            # 5. Claro, finalmente actualizamos la pag para ver los resultados:
            pagina.update()

    txt_resultado = ft.Text()
    btn_cargar = ft.Button("Cargar Datos", on_click=botonClickeado)

    def borrar_texto(e):
        txt_resultado.value = ""  # O texto.value = None
        pagina.update()

    pagina.add(btn_cargar, txt_resultado, ft.Button("Borrar", on_click=borrar_texto))

ft.run(principal)