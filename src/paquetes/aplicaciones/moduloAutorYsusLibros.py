import flet as ft
import asyncio
import httpx
from paquetes.controles.tablas.datatables import DataTable1

#Constantes:
#cabezeras = {"Authorization": f"Bearer {self.sesion.tokenAcceso}"}
url_api = "http://127.0.0.1:8000/catalogo/apirest/autores/"

class AutorYsusLibros(ft.Column):
    def __init__(self, pagina, sesion):
        super().__init__()
        self.pag = pagina
        self.sesion = sesion
        self.listaFiltrada = []
        self.listaTodosLosTitulosYsusCampos = []
        #self.respuesta = None
        self.cabezeras = {"Authorization": f"Bearer {self.sesion.tokenAcceso}"}
    
    def build(self):
        self.menuAutores = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Autores",
            options=[],
            on_select=self.actualizarMenuLibrosDelAutor,
            )

        self.menuLibrosDelAutor = ft.Dropdown(
            editable=False,                            
            width=220,
            label="Libros",
            options=[],
            on_select=self.actTablaLibrosDeAutor,
            )
                      
        self.tablaLibrosDelAutorSelec = DataTable1()
        self.tablaLibrosDelAutorSelec_2 = DataTable1()

        self.btn_cargar = ft.Button("Cargar Datos", on_click=self.botonConectarClickeado)

        #Finalmente agregamos los controles a la columma (recuerde que este objeto es una herencia de ft.Column):
        self.controls = [
            self.btn_cargar,
            ft.Row(controls=[self.menuAutores, self.menuLibrosDelAutor]),
            ft.Button("Borrar", on_click=self.botonBorrarClickeado), 
            self.tablaLibrosDelAutorSelec,
            self.tablaLibrosDelAutorSelec_2,
        ]

    async def botonConectarClickeado(self, e):
        try:
            async with httpx.AsyncClient(headers=self.cabezeras) as client:
                respuesta = await client.get(url_api)     

            diccionario = respuesta.json() #Analiza el cuerpo de la respuesta como JSON y devuelve un diccionario o lista de Python.
            
            #Tomamos el primer elemento de results que es una lista de diccionarios:
            listDeDicts = diccionario['results']

        except Exception as error:
            
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Ocurrió un error..."),
                content=ft.Text(f'Error: {error}'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))

        else: 
            #Filtramos listDeDicts para extraer los campos deseados de cada uno de los diccionarios que contienen los datos del autor:
            self.listaFiltrada = [{"id": d["id"], "nombre": d["nombre"], "apellido": d["apellido"], "libros": d["libros"]} for d in listDeDicts]

            #Así convertimos una lista de diccionarios a una lista de ft.dropdown.Option en su carga inicial y definitiva:
            dropdown_options_autores = [
                ft.dropdown.Option(
                    key=autor["id"],      # El valor que se obtiene al seleccionar
                    text=f"{autor['nombre']} {autor['apellido']}" #Así hacemos un atributo text compuesto. 
                )
            for autor in self.listaFiltrada
            ]

            self.menuAutores.options = dropdown_options_autores   
            self.menuAutores.update() 

    #Método para actualizar el menú de los libros del autor seleccionado:
    async def actualizarMenuLibrosDelAutor(self, e):
        autor_seleccionado = int(e.control.value) #Tenemos que llevar a entero porque los control.value retornan cadenas, y el id en listaFiltrada está expresada como tipo entero.
        
        # Extraemos el diccioanrio que expresa el registro del autor:
        dictAutor = next((autor for autor in self.listaFiltrada if autor['id'] == autor_seleccionado), None)

        #Extraemos la lista de sus libros contenido en el campo 'libros' de dictAutor y que están en forma de hipervínculos:
        susLibros = dictAutor['libros']

        #Para obtener los títulos de los libros a partir de sus hipervínculos:
        listaDeTitulos=[] #Solo el título para el dropdown de los libros (títulos)
        self.listaTodosLosTitulosYsusCampos = [] #Reseteamos para limpiar de la última selección de autor.

        for url in susLibros:
            try:
                async with httpx.AsyncClient(headers=self.cabezeras) as client:
                    urlLibroRequest = await client.get(url)
                  
            except Exception:
                self.pag.show_dialog(ft.AlertDialog(
                    title=ft.Text("Ocurrió un error..."),
                    content=ft.Text(f'Error: {str(urlLibroRequest.status_code)}'),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: pagina.pop_dialog())],
                    modal=True
                ))

            else:
                if urlLibroRequest: #status_code == 200:
                    data = urlLibroRequest.json() #es el diccionario tal como se muestra en el cliente drf.
                    print(f'data={data}')
                    titulo=data['titulo']
                    listaDeTitulos.append(titulo)
                    self.listaTodosLosTitulosYsusCampos.append(data)
                else:
                    self.botonBorrarClickeado(None)
                    self.pag.show_dialog(ft.AlertDialog(
                    title=ft.Text("Ocurrió un error..."),
                    content=ft.Text(f'No hubo conexión. Código: {urlLibroRequest.status_code}. Pulse el botón "cargar datos" para intentar nuevamente.'),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                    modal=True
                ))       
        #Por último rellenamos las opciones de menuLibrosDelAutor por comprensión de listas:
        dropdown_options_librosDelAutor = [
            ft.dropdown.Option(
                key=libro["id"],      # El valor que se obtiene al seleccionar
                text=libro["titulo"], 
            )
            for libro in self.listaTodosLosTitulosYsusCampos
        ]

        self.menuLibrosDelAutor.options = dropdown_options_librosDelAutor
        self.menuLibrosDelAutor.value = None # Resetea el valor seleccionado anterior
        self.tablaLibrosDelAutorSelec_2.rows = []  #Borramos lo que quedó en esta tabla de la selección anterior en menuLibrosDelAutor.
        #Rellenamos la tabla de datos de los libros del autor seleccionado, tomados de listaTodosLosTitulosYsusCampos que contiene esos datos para el autor seleccionado:
        displayed_items = list(self.listaTodosLosTitulosYsusCampos)
   
        #El método build_rows está implementado para tomar 4 campos específicos de cada registro de listaTodosLosTitulosYsusCampos:
        self.tablaLibrosDelAutorSelec.hacerRegistrosApartirDe(displayed_items)
        

    def actTablaLibrosDeAutor(self, e):
        """
        Vamos a meter el libro seleccionado (una sola fila o registro) en el dropdown menuLibrosDelAutor
        """
        libro_seleccionado = int(e.control.value)
        dictDelLibroSelec = next((libro for libro in self.listaTodosLosTitulosYsusCampos if libro['id'] == libro_seleccionado), None)

        #El argumento que acepta el atributo método hacerRegistrosApartirDe() en nuestra clase personalizada, DataTable1(), son listas de diccionarios.
        #Así que tenemos que hacer una lista de un sólo elemento, cuyo elemento es el libro seleccionado en menuLibrosDelAutor, dictLibro:
        lista = [dictDelLibroSelec,]
        self.tablaLibrosDelAutorSelec_2.hacerRegistrosApartirDe(lista)


    def botonBorrarClickeado(self, e):
        self.menuAutores.options = []
        self.menuLibrosDelAutor.options = []
        self.tablaLibrosDelAutorSelec.rows = []
        self.tablaLibrosDelAutorSelec_2.rows = []
        self.pag.update()
