#Menú desplegable (dropdown) de autores y sus libros.
import flet as ft
import requests

def principal(pagina: ft.Page):
    pagina.title = "Menú desplegable autor y sus libros"
    listaFiltrada = []
    listaTodosLosTitulosYsusCampos = []
    
    def botonClickeado(e):
        # 1. Consumir la API.  
        nonlocal listaFiltrada #Hacemos el enlace de listaFiltrada a la capa exterior inmediata, porque usaremos esta lista en varias funciones dentro de dicha capa, es decir la función principal(pagina: ft.Page)

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

            #Así convertimos una lista de diccionarios a una lista de ft.dropdown.Option en su carga inicial y definitiva:
            dropdown_options_autores = [
                ft.dropdown.Option(
                    key=autor["id"],      # El valor que se obtiene al seleccionar
                    text=f"{autor['nombre']} {autor['apellido']}" #Así hacemos un atributo text compuesto. 
                )
            for autor in listaFiltrada
            ]
            menuAutores.options = dropdown_options_autores   

        finally:
            pass  

    #Funcion para actualizar el menú de los libros del autor seleccionado:
    def actualizarAutor(e):
        autor_seleccionado = int(e.control.value) #Tenemos que llevar a entero porque los control.value retornan cadenas, y el id en listaFiltrada está expresada como tipo entero.
        
        # Extraemos el diccioanrio que expresa el registro del autor:
        dictAutor = next((autor for autor in listaFiltrada if autor['id'] == autor_seleccionado), None)

        #Extraemos la lista de sus libros contenido en el campo 'libros' de dictAutor y que están en forma de hipervínculos:
        susLibros = dictAutor['libros']

        #Para obtener los títulos de los libros a partir de sus hipervínculos:
        listaDeTitulos=[] #Solo el título para el dropdown de los libros (títulos)
        nonlocal listaTodosLosTitulosYsusCampos #Lista de diccionarios-registro de los libros del autor seleccionado:

        listaTodosLosTitulosYsusCampos = [] #Reseteamos para limpiar de la última selección de autor.
        for url in susLibros:
            urlLibro = requests.get(url)
            urlLibro.raise_for_status() # Lanza error si no es 200
            data = urlLibro.json() #es el diccionario tal como se muestra en el cliente drf.
            titulo=data['titulo']
            listaDeTitulos.append(titulo)
            listaTodosLosTitulosYsusCampos.append(data)
        
        #Por último rellenamos las opciones de menuLibrosDelAutor por comprensión de listas:
        dropdown_options_librosDelAutor = [
            ft.dropdown.Option(
                key=libro["id"],      # El valor que se obtiene al seleccionar
                text=libro["titulo"], 
            )
            for libro in listaTodosLosTitulosYsusCampos
        ]

        menuLibrosDelAutor.options = dropdown_options_librosDelAutor
        menuLibrosDelAutor.value = None # Resetea el valor seleccionado anterior
        tablaLibrosDelAutorSelec_2.rows = []  #Borramos lo que quedó en esta tabla.
        #Rellenamos la tabla de datos de los libros del autor seleccionado, tomados de listaTodosLosTitulosYsusCampos que contiene esos datos para el autor seleccionado:
        displayed_items = list(listaTodosLosTitulosYsusCampos)
   
        #El método build_rows está implementado para tomar 4 campos específicos de cada registro de listaTodosLosTitulosYsusCampos:
        tablaLibrosDelAutorSelec.hacerRegistrosApartirDe(displayed_items)
    
    def actTablaLibrosDeAutor(e):
        libro_seleccionado = int(e.control.value)
        dictLibro = next((libro for libro in listaTodosLosTitulosYsusCampos if libro['id'] == libro_seleccionado), None)
        
        #displayed_items = list(dictLibro)
        #print(displayed_items)
        tablaLibrosDelAutorSelec_2.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(dictLibro["id"])),
                        ft.DataCell(ft.Text(dictLibro["titulo"])),
                        ft.DataCell(ft.Text(dictLibro["isbn"])),
                        ft.DataCell(ft.Text(dictLibro["url"])),
                    ],
                )
        ]
    

    #Declaración de los menú desplegables:
    menuAutores = ft.Dropdown(
                        editable=True,                            
                        width=220,
                        label="Autores",
                        options=[],
                        on_select=actualizarAutor,
                    )

    menuLibrosDelAutor = ft.Dropdown(
                        editable=False,                            
                        width=220,
                        label="Libros",
                        options=[],
                        on_select=actTablaLibrosDeAutor,
                    )
    
    from paquetes.controles.tablas.datatables import DataTable1

    tablaLibrosDelAutorSelec = DataTable1()

    tablaLibrosDelAutorSelec_2 = DataTable1()

    btn_cargar = ft.Button("Cargar Datos", on_click=botonClickeado)

    def botonBorrarClickeado(e):
        menuAutores.options=[]
        menuLibrosDelAutor.options=[]
        pagina.update() 

    pagina.add(
        btn_cargar, 
        ft.Row(controls=[menuAutores, menuLibrosDelAutor]), 
        ft.Button("Borrar", on_click=botonBorrarClickeado),
        tablaLibrosDelAutorSelec,
        tablaLibrosDelAutorSelec_2,
        )

ft.run(principal)
