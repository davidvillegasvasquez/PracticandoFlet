import flet as ft
import asyncio
import httpx

API_URL_libros = "http://127.0.0.1:8000/catalogo/apirest/libros/"
API_URL_libro = "http://127.0.0.1:8000/catalogo/apirest/libros/<int:pk>/"

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
    
    def build(self):
        #Dibujo de los controles que deben mostrarse precarcados al ir a la vista:
        self.menuGeneros=ft.ListView(controls=[], expand=True)
        self.titulo_input = ft.TextField(label="Título")
        self.autor_input = ft.TextField(label="Autor")
        #Configuración de un TextField para textos largos. Comienza con 3 lineas visible, a la 6ta para comenzar hacer scroll:
        self.descripcion_input = ft.TextField(label="Descripción", multiline=True, min_lines=3, max_lines=5)
        self.isbn_input = ft.TextField(label="Isbn")
        self.lenguaje_input = ft.TextField(label="Lenguaje")

        self.resultado_texto = ft.Text()

        self.controls = [
            self.menuLibros,
            self.titulo_input,
            self.autor_input,
            self.descripcion_input,
            self.isbn_input,
            ft.Container(
                height=100, # Define el área visible para forzar scroll
                width=250,
                padding=10,
                border=ft.Border.all(1, ft.Colors.BLACK),
                border_radius=ft.BorderRadius.all(value=5),
                content=self.menuGeneros,
            ),
            self.lenguaje_input,
            ft.Button("Actualizar", on_click=""),
            self.resultado_texto,
        ]

    #Método para ser ejecutado asíncronamente desde main con el atributo método de los objetos ft.View, on_will_mount (vista.on_will_mount) para poder precargar los controles que lo requieren:
    async def laVista_se_montara(self):
        await self.cargarLibros()
      
    async def cargarLibros(self):
        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                respuestaLibros = await client.get(API_URL_libros)     

            diccionarioLibros = respuestaLibros.json()
            self.listDeDictsLibros = diccionarioLibros['results']

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
        libro_seleccionado = int(e.control.value) #Tenemos que llevar a entero porque los control.value retornan cadenas, y el id en listaFiltrada está expresada como tipo entero.
        
        # Extraemos el diccionario que expresa el registro del libro seleccionado entre todos los registros-diccionarios contenidos en self.listDeDictsLibros:
#Será uno así: {'url': 'http://127.0.0.1:8000/catalogo/apirest/libros/4/', 'id': 4, 'titulo': 'Canaima', 'autor': 'http://127.0.0.1:8000/catalogo/apirest/autores/2/', 'descripcion': 'Canaima es una novela ...', 'isbn': '9798886451740', 'genero': ['http://127.0.0.1:8000/catalogo/apirest/generos/1/'], 'lenguaje': 'http://127.0.0.1:8000/catalogo/apirest/lenguajes/1/'}

        dictLibroSelec = next((libro for libro in self.listDeDictsLibros if libro['id'] == libro_seleccionado), None)

        #Primero extraémos los campos del diccionario-registro que son hipervínculos (autor, lenguaje y generos):

        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                respuestaAutor = await client.get(dictLibroSelec['autor']) 
                respuestaLenguaje = await client.get(dictLibroSelec['lenguaje'])
                #dictLibroSelec ['genero'] es una lista de urls, por lo cual debemos iterar sobre ellas y extraer los dict que devuelven esas urls:
                listaDictsGenerosSelec = []
                for url in dictLibroSelec ['genero']:
                    respuestaGeneros = await client.get(url)
                    listaDictsGenerosSelec.append(respuestaGeneros.json())

            dictAutorSelec = respuestaAutor.json() 
            dictLenguajeSelec = respuestaLenguaje.json()

            print('======================================')
            print(f"dictAutorSelec = {dictAutorSelec}")
            print('--------------------------------------')
            print(f"dictLenguajeSelec = {dictLenguajeSelec}")
            print('--------------------------------------')
            print(f"listaDictsGenerosSelec = {listaDictsGenerosSelec}")

        except Exception as error:
            
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Ocurrió un error..."),
                content=ft.Text(f'Error: {error}'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))

        else: 
            self.pag.update()
            #Filtramos

        #Extraemos el resto de campos del diccionario que expresa el registro del libro seleccionado que no son hipervinculos, y se lo asignamos directamente a los controles de la vista:
        #self.titulo_input.value = dictLibroSelec['titulo']


        
        
    async def botonPatchLibro(self, e):
        self.resultado_texto.value = "Enviando datos..."
        self.pag.update()

        #Nuevamente, validamos que el usuario no deje vacío los campos:
        """
        if self.menuAutores.value is not None:
            val_select_autor = int(self.menuAutores.value)
        else:
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Error de ingreso"),
                content=ft.Text('Debe seleccionar un autor.'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))
            return #Forzamos la finalización del método.

        #Por comprensión de listas creamos la lista de ids de los generos seleccionados que fue guardado en su atributo data:
        gen_selec=[
            checkbox.data for checkbox in self.menuGeneros.controls if checkbox.value
        ]
        if gen_selec: #Lista no vacía, el usuario seleccionó al menos un genero.
            pass
        else:
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Error de ingreso"),
                content=ft.Text('Debe seleccionar al menos un genero.'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))
            return
      
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

        
        Aquí no necesitamos obtener el valor literal de los campos porque estamos usando un serializador hipervinculado, lo cual requiere el número del índice del item para construir a partir de este la url necesaria, y no un str. En vistas basadas en serializadores normales si necesitaríamos ese valor literal directamente.
        # Iteramos sobre las opciones para extraer el texto
        autor_selec = next((opt.text for opt in self.menuAutores.options if opt.key == val_select_autor), None)
        
        genero_selec = next((opt.text for...
        
        #Procedemos a contruir la payload o cuerpo (body) de la petición o solicitud:
        datos = {
            "titulo": self.titulo_input.value,
            #Debemos usar el patron modelo_id para referenciar los campos con relaciones foreingkey del lado uno, porque vamos a construir urls con serializadores hipervinculados:
            "autor_id": val_select_autor,
            "descripcion": self.descripcion_input.value,
            "isbn": self.isbn_input.value,
            #Aunque genero tiene muchos libros, es una relación ManyToMany con Libro, por ello no se referencia con genero_id:
            "genero": gen_selec,
            "lenguaje_id": val_select_len
        }

        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                response = await client.post(API_URL_libros, json=datos, timeout=10.0)
                
                if response.status_code == 201:
                    #Aqui se debe meter un modal y redirigir a home:
                    self.resultado_texto.value = "Libro creado exitosamente."
                    self.resultado_texto.color = "green"
                    #self.pag.push_route("/")
                else:
                    self.resultado_texto.value = f"Error {response.status_code}: {response.text}"
                    self.resultado_texto.color = "red" 

        except Exception as ex:
            self.resultado_texto.value = f"Error de conexión: {str(ex)}"
            self.resultado_texto.color = "red"

        """