#Menú desplegable (dropdown) de autores y sus libros.
import flet as ft
import requests

def principal(pagina: ft.Page):
    pagina.title = "Menú desplegable autor y sus libros"

    def botonClickeado(e):
        # 1. Consumir la API.  Algunos de los atributos y métodos más utilizados del objeto `request` incluyen:
        try:
            respuestaGet = requests.get("http://127.0.0.1:8000/catalogo/api-todosLosAutores/") #respuestaGet es un objeto Response.
            
        except:
            pagina.show_dialog(ft.AlertDialog(
                title=ft.Text("Hubo un error en la conexión."),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: pagina.pop_dialog())],
                modal=True
            ))
        else:

            diccionario = respuestaGet.json() #Analiza el cuerpo de la respuesta como JSON y devuelve un diccionario o lista de Python.
            
            #Tomamos el primer elemento de results que es una lista de diccionarios:
            listDeDicts = diccionario['results'] 
   
            #Filtramos listDeDicts para extraer los campos deseados de cada uno de los diccionarios que contienen los datos del autor:
            listaFiltrada = [{"id": d["id"], "nombre": d["nombre"], "apellido": d["apellido"], "libros": d["libros"]} for d in listDeDicts]

            #Así convertimos una lista de diccionarios a una lista de ft.dropdown.Option:
            dropdown_options_autores = [
                ft.dropdown.Option(
                    key=autor["id"],      # El valor que se obtiene al seleccionar
                    text=f"{autor['nombre']} {autor['apellido']}" #Así hacemos un atributo text compuesto. 
                )
            for autor in listaFiltrada
            ]
            menuAutores.options = dropdown_options_autores

            #Y para sus libros:
            dropdown_options_libros = [
                ft.dropdown.Option(
                    key=libro["id"],      # El valor que se obtiene al seleccionar
                    text=libro["libros"]
                )
            for libro in listaFiltrada
            ]
            menuLibros.options = dropdown_options_libros

        finally:
            #Claro, finalmente actualizamos la pag para ver los resultados:
            pagina.update()          

    menuAutores = ft.Dropdown(
                        editable=True,                            
                        width=220,
                        label="Autores",
                        options=[],
                        #on_select=handle_dropdown_select_autor,
                    )

    menuLibros = ft.Dropdown(
                        editable=False,                            
                        width=220,
                        label="Libros",
                        options=[],
                    )
    """
    def handle_dropdown_select_autor(e: ft.Event[ft.Dropdown]):
        e.control.autor = e.control.value
    """
    btn_cargar = ft.Button("Cargar Datos", on_click=botonClickeado)

    def botonBorrarClickeado(e):
        menuAutores.options=[]
        menuLibros.options=[]
        pagina.update() 

    pagina.add(btn_cargar, ft.Row(controls=[menuAutores, menuLibros]), ft.Button("Borrar", on_click=botonBorrarClickeado))

ft.run(principal)
