#Menú desplegable (dropdown) de autores y sus libros.
import flet as ft
import requests

def principal(pagina: ft.Page):
    pagina.title = "Menú desplegable autor y sus libros"
    #Variables creadas en botonConectarClickeado y enlazadas (nonlocal) al ámbito (scope) de principal(pagina: ft.Page) porque serán usadas en el resto de las funciónes de este ámbito.
    listaFiltrada = []
    listaTodosLosTitulosYsusCampos = []
    
    def botonConectarClickeado(e):
        # 1. Consumir la API.  
        nonlocal listaFiltrada #Hacemos el enlace de listaFiltrada a la capa exterior inmediata, principal(pagina: ft.Page).

        try:
            respuestaGet = requests.get("http://127.0.0.1:8000/catalogo/api-todosLosAutores/") #respuestaGet es un objeto Response.

            diccionario = respuestaGet.json() #Analiza el cuerpo de la respuesta como JSON y devuelve un diccionario o lista de Python.
            
            #Tomamos el primer elemento de results que es una lista de diccionarios:
            listDeDicts = diccionario['results']

        except:
            pagina.show_dialog(ft.AlertDialog(
                title=ft.Text("Hubo un error en la conexión."),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: pagina.pop_dialog())],
                modal=True
            ))

        else: 
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
    def actualizarMenuLibrosDelAutor(e):
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
        tablaLibrosDelAutorSelec_2.rows = []  #Borramos lo que quedó en esta tabla de la selección anterior en menuLibrosDelAutor.
        #Rellenamos la tabla de datos de los libros del autor seleccionado, tomados de listaTodosLosTitulosYsusCampos que contiene esos datos para el autor seleccionado:
        displayed_items = list(listaTodosLosTitulosYsusCampos)
   
        #El método build_rows está implementado para tomar 4 campos específicos de cada registro de listaTodosLosTitulosYsusCampos:
        tablaLibrosDelAutorSelec.hacerRegistrosApartirDe(displayed_items)
    
    def actTablaLibrosDeAutor(e):
        """
        Vamos a meter el libro seleccionado (una sola fila o registro) en el dropdown menuLibrosDelAutor
        """
        libro_seleccionado = int(e.control.value)
        dictDelLibroSelec = next((libro for libro in listaTodosLosTitulosYsusCampos if libro['id'] == libro_seleccionado), None)

        #El argumento que acepta el atributo método hacerRegistrosApartirDe() en nuestra clase personalizada, DataTable1(), son listas de diccionarios.
        #Así que tenemos que hacer una lista de un sólo elemento, cuyo elemento es el libro seleccionado en menuLibrosDelAutor, dictLibro:
        lista = [dictDelLibroSelec,]
        tablaLibrosDelAutorSelec_2.hacerRegistrosApartirDe(lista)

    #Declaración de los menú desplegables:
    menuAutores = ft.Dropdown(
                        editable=True,                            
                        width=220,
                        label="Autores",
                        options=[],
                        on_select=actualizarMenuLibrosDelAutor,
                    )

    menuLibrosDelAutor = ft.Dropdown(
                        editable=False,                            
                        width=220,
                        label="Libros",
                        options=[],
                        on_select=actTablaLibrosDeAutor,
                    )
    
    from paquetes.controles.tablas.datatables import DataTable1
    #Hacemos la tabla que lista todos los libros del autor seleccionad:
    tablaLibrosDelAutorSelec = DataTable1()

    #Tabla de datos (DataTable) de una sola fila o registro que mostrara los datos del libro seleccioando en el menú desplegable menuLibrosDelAutor:
    tablaLibrosDelAutorSelec_2 = DataTable1()

    btn_cargar = ft.Button("Cargar Datos", on_click=botonConectarClickeado)

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
