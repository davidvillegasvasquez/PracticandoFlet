import flet as ft
import asyncio
import httpx

API_URL_libros = "http://127.0.0.1:8000/catalogo/apirest/libros/"
API_URL_generos = "http://127.0.0.1:8000/catalogo/apirest/generos/"
#API_URL_libro = "http://127.0.0.1:8000/catalogo/apirest/libros/<int:pk>/"

class PatchLibro(ft.Column):
    def __init__(self, pagina, sesion):
        super().__init__()
        self.pag = pagina
        self.sesion = sesion
        #En un modelo asíncrono, los controles que deben ser precargados con datos de los endpoints al navegar a su vista, en nuestro caso
#menuAutores, menuGenero y menuLenguajes, debes inicializarlos primero aquí en el
#constructor y no en el método build. Esto para poder habilitar la acción de previsualización de sus dropdown en main con el atributo de vista, on_will_mount cuando se cargue la vista al navegar hacia ella:
        self.menuLibros = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Libros",
            options=[],
            on_select=self.rellenarCamposLibroSelec
            )
        #Creamos el atributo generos, una lista de diccionarios para tener todos los generos al cargar que mostraremos como checkboxs, y expresamos los de un libro en particular como checkboxs marcados (value=True):
        self.generos = []
        self.idLibroSeleccionado = None
    
    def build(self):
        #Dibujo de los controles que deben mostrarse precarcados al ir a la vista:
        self.menuGeneros=ft.ListView(controls=[], expand=True)
        #self.titulo_input = ft.TextField(label="Título")
        self.autor_input = ft.TextField(label="Autor", disabled=True)
        #Configuración de un TextField para textos largos. Comienza con 3 lineas visible, a la 6ta para comenzar hacer scroll:
        self.descripcion_input = ft.TextField(label="Descripción", multiline=True, min_lines=3, max_lines=5)
        self.isbn_input = ft.TextField(label="Isbn")
        #Ver como se puede hacer un dropdown que muestre el lenguaje actual como seleccionado:
        self.lenguaje_input = ft.TextField(label="Lenguaje", disabled=True)

        self.resultado_texto = ft.Text()

        self.controls = [
            self.menuLibros,
            self.autor_input,
            self.descripcion_input,
            self.isbn_input,
            ft.Container(
                height=250, # Define el área visible para forzar scroll
                width=250,
                padding=10,
                border=ft.Border.all(1, ft.Colors.BLACK),
                border_radius=ft.BorderRadius.all(value=5),
                content=self.menuGeneros,
            ),
            self.lenguaje_input,
            ft.Button("Actualizar", on_click=self.actualizar),
            self.resultado_texto,
        ]

    #Método para ser ejecutado asíncronamente desde main con el atributo método de los objetos ft.View, on_will_mount (vista.on_will_mount) para poder precargar los controles que lo requieren:
    async def laVista_se_montara(self):
        await self.cargarLibros()
      
    async def cargarLibros(self):
        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                respuestaLibros = await client.get(API_URL_libros) 
                #Obtenemos aquí la lista de todos los generos para no cargar tanto el método rellenarCamposLibroSelec, además que es una sola lista de valores fijo, como la de Libros:  
                respuestaGeneros = await client.get(API_URL_generos)

            #Rellenamos con lo valores consultados:
            diccionarioLibros = respuestaLibros.json()
            diccionarioGeneros = respuestaGeneros.json()
            
            self.listDeDictsLibros = diccionarioLibros['results']
            self.generos = diccionarioGeneros['results']

        except Exception as error:
            
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Ocurrió un error..."),
                content=ft.Text(f'Error: {error}'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))

        else: 
            dropdown_options_libros = [
                ft.dropdown.Option(
                    key=libro["id"], 
                    text=libro['titulo'] 
                )
            for libro in self.listDeDictsLibros
            ]
            self.menuLibros.options = dropdown_options_libros

    
    async def rellenarCamposLibroSelec(self, e):
        """
        El método asociado al evento de seleccionar un libro en el dropdown de libros. Toma los datos actuales del libro seleccionado y los coloca en controles que pueden ser editados, listos para accionar el botón de actualizar y tomar los nuevos valores en los campos editables (descripción, isbn, generos y lenguaje).
        """
   

        self.idLibroSeleccionado = int(e.control.value) #Tenemos que llevar a entero porque los control.value retornan cadenas, y el id en listaFiltrada está expresada como tipo entero.
        
        # Extraemos el diccionario que expresa el registro del libro seleccionado entre todos los registros-diccionarios contenidos en self.listDeDictsLibros:
#Será uno así: {'url': 'http://127.0.0.1:8000/catalogo/apirest/libros/4/', 'id': 4, 'titulo': 'Canaima', 'autor': 'http://127.0.0.1:8000/catalogo/apirest/autores/2/', 'descripcion': 'Canaima es una novela ...', 'isbn': '9798886451740', 'genero': ['http://127.0.0.1:8000/catalogo/apirest/generos/1/'], 'lenguaje': 'http://127.0.0.1:8000/catalogo/apirest/lenguajes/1/'}

        dictLibroSelec = next((libro for libro in self.listDeDictsLibros if libro['id'] == self.idLibroSeleccionado), None)

        #Primero extraémos los campos del diccionario-registro que son hipervínculos (autor, lenguaje y generos):

        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                respuestaAutor = await client.get(dictLibroSelec['autor']) 
                respuestaLenguaje = await client.get(dictLibroSelec['lenguaje'])
                #dictLibroSelec['genero'] es una lista de urls, por lo cual debemos iterar sobre ellas y extraer los dict que devuelven esas urls:
                listaIdsGenerosSelec = []
                for url in dictLibroSelec['genero']:
                    respuestaGeneros = await client.get(url)
                    #Recuerde que respuestaGeneros.json() es el diccionario del genero devuelto en la solicitud (una lista), de modo que extraemos sus ids para almacenaro en
#atributo data del checkbox correspondiente para darle value=True en la lista de de checkbox generos en el listview self.menuGeneros:
                    listaIdsGenerosSelec.append(respuestaGeneros.json()['id'])

            dictAutorSelec = respuestaAutor.json() 
            dictLenguajeSelec = respuestaLenguaje.json()

        except Exception as error:
            
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Ocurrió un error..."),
                content=ft.Text(f'Error: {error}'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))

        else: 
            #La lista de generos:
            self.menuGeneros.controls = [
                ft.Checkbox(
                    label=genero["nombre"],
                    value=True if genero["id"] in listaIdsGenerosSelec else False,
                    #Adjuntamos el id, en el atributo para uso del usuario, data:
                    data=genero["id"],
                ) 
            for genero in self.generos
            ]
            
            self.autor_input.value = f"{dictAutorSelec['nombre']} {dictAutorSelec['apellido']}"
            self.descripcion_input.value = dictLibroSelec['descripcion']
            self.isbn_input.value = dictLibroSelec['isbn']
            self.lenguaje_input.value = dictLenguajeSelec['nombre']
            #Finalmente actualizamos para hacer visible los cambios:
            self.pag.update()

        
    async def actualizar(self, e):
        self.resultado_texto.value = "Enviando datos..."
        self.pag.update()

        #Nuevamente, validamos que el usuario no deje vacío los campos:

        #Por comprensión de listas creamos la lista de ids de los generos seleccionados que fue guardado en su atributo data:
        gen_selec_ids=[
            checkbox.data for checkbox in self.menuGeneros.controls if checkbox.value
        ]
       

        if gen_selec_ids: #Lista no vacía, el usuario seleccionó al menos un genero.
            #Ahora, tenemos que crear la lista de urls de generos seleccionados, porque las solicitudes patch para campos de listas con relaciones ManyToMany así lo exige:
            urls_gen_selec = [
                dictGen['url'] for dictGen in self.generos if dictGen['id'] in gen_selec_ids
            ]
        else:
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Error de ingreso"),
                content=ft.Text('Debe seleccionar al menos un genero.'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))
            return

        if self.isbn_input.value is not None:
            pass
        else:
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Error de ingreso"),
                content=ft.Text('Debe aportar un isbn.'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))
            return

        if self.descripcion_input.value is not None:
            pass
        else:
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Error de ingreso"),
                content=ft.Text('Debe aportar un descripción.'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))
            return
        """
        if self.menuLenguajes.value is not None:
            val_select_len = int(self.menuLenguajes.value)
        else:
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Error de ingreso"),
                content=ft.Text('Debe seleccionar un lenguaje.'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))
            return
        """
   
        #Procedemos a contruir la payload o cuerpo (body) de la petición o solicitud:
        datos = {
            "descripcion": self.descripcion_input.value,
            "isbn": self.isbn_input.value,
            "genero": urls_gen_selec
            #"lenguaje_id": val_select_len
        }

        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                #Reucerde que API_URL_libros tiene un / al final. Si colocamos / se producirá un error como: PATCH /catalogo/apirest/libros//31/ HTTP/1.1" 404
                response = await client.patch(f"{API_URL_libros}{self.idLibroSeleccionado}/", json=datos, timeout=10.0)
                
                if response.status_code == 200:
                    #Aqui se debe meter un modal y redirigir a home:
                    self.resultado_texto.value = "Libro actualizado exitosamente."
                    self.resultado_texto.color = "green"
                    return response.json()
                else:
                    self.resultado_texto.value = f"Error {response.status_code}: {response.text}"
                    self.resultado_texto.color = "red" 

        except Exception as ex:
            self.resultado_texto.value = f"Error de conexión: {str(ex)}"
            self.resultado_texto.color = "red"
