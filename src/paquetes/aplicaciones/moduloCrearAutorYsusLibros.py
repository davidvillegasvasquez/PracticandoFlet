import flet as ft
import asyncio
import httpx

API_URL_autores = "http://127.0.0.1:8000/catalogo/apirest/autores/"
API_URL_libros = "http://127.0.0.1:8000/catalogo/apirest/libros/"
API_URL_generos = "http://127.0.0.1:8000/catalogo/apirest/generos/"
API_URL_lenguajes = "http://127.0.0.1:8000/catalogo/apirest/lenguajes/"

class CrearAutor(ft.Column):
    def __init__(self, pagina, sesion):
        super().__init__()
        self.pag = pagina
        self.sesion = sesion
    
    def build(self):
        self.nombre_input = ft.TextField(label="Nombre")
        self.apellido_input = ft.TextField(label="Apellido")
        self.nacimiento_input = ft.TextField(label="Nacimiento")
        self.muerte_input = ft.TextField(label="Muerte")
        self.resultado_texto = ft.Text()

        self.controls = [
            self.nombre_input,
            self.apellido_input,
            self.nacimiento_input,
            self.muerte_input,
            ft.Button("Crear", on_click=self.botonCrearAutor),
            self.resultado_texto
        ]

    async def botonCrearAutor(self, e):
        self.resultado_texto.value = "Enviando datos..."
        self.pag.update()
        
        datos = {
            "nombre": self.nombre_input.value,
            "apellido": self.apellido_input.value,
            "nacimiento": self.nacimiento_input.value,
            "muerte": self.muerte_input.value
        }

        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                response = await client.post(API_URL_autores, json=datos, timeout=10.0)
                
                if response.status_code == 201:
                    self.resultado_texto.value = "Autor creado exitosamente."
                    self.resultado_texto.color = "green"
                else:
                    self.resultado_texto.value = f"Error {response.status_code}: {response.text}"
                    self.resultado_texto.color = "red" 

        except Exception as ex:
            self.resultado_texto.value = f"Error de conexión: {str(ex)}"
            self.resultado_texto.color = "red"

class CrearLibro(ft.Column):
    def __init__(self, pagina, sesion):
        super().__init__()
        self.pag = pagina
        self.sesion = sesion
        #En un modelo asíncrono, si quieres ver los controles precargados con datos de los endpoints al navegar a la vista, debes inicializarlos primero en el constructor:
        self.menuAutores = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Autores",
            options=[],
            on_select="",
            )
        self.menuGeneros = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Genero",
            options=[],
            on_select="",
            )
        self.menuLenguajes = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Lenguaje",
            options=[],
            on_select="",
            )
    
    
    def build(self):
        self.menuAutores
        self.menuGeneros 
        self.menuLenguajes

        self.titulo_input = ft.TextField(label="Nombre")
        #Configuración de un TextField para textos largos. Comienza con 3 lineas visible, a la 6 para comenzar hacer scroll:
        self.descripcion_input = ft.TextField(label="Descripción", multiline=True, min_lines=3, max_lines=5)
        self.isbn_input = ft.TextField(label="Isbn")
        self.resultado_texto = ft.Text()

        self.controls = [
            self.titulo_input,
            self.menuAutores,
            self.descripcion_input,
            self.isbn_input,
            self.menuGeneros,
            self.menuLenguajes,
            ft.Button("Crear", on_click=""), #self.cargarAutoresGenerosYlenguajes), #self.botonCrearLibro),
            self.resultado_texto,
        ]

    async def view_will_mount(self):
        await self.cargarAutoresGenerosYlenguajes()
      
    async def cargarAutoresGenerosYlenguajes(self):
        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                respuestaAutores = await client.get(API_URL_autores)     
                respuestaGeneros = await client.get(API_URL_generos)
                respuestaLenguajes = await client.get(API_URL_lenguajes)

            diccionarioAutores = respuestaAutores.json() #Analiza el cuerpo de la respuesta como JSON y devuelve un diccionario o lista de Python.
            diccionarioGeneros = respuestaGeneros.json()
            diccionarioLenguajes = respuestaLenguajes.json()
            #Tomamos el primer elemento de results que es una lista de diccionarios:
            listDeDictsAutores = diccionarioAutores['results']
            listDeDictsGeneros = diccionarioGeneros['results']
            listDeDictsLenguajes = diccionarioLenguajes['results']

        except Exception as error:
            
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Ocurrió un error..."),
                content=ft.Text(f'Error: {error}'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))

        else: 
            #Filtramos listDeDictsAutores para extraer los campos deseados de cada uno de los diccionarios que contienen los datos del autor. Los otros dos no se necesitan ser filtrados:
            listDeDictFiltAutores = [{"id": d["id"], "nombre": d["nombre"], "apellido": d["apellido"]} for d in listDeDictsAutores]

            dropdown_options_autores = [
                ft.dropdown.Option(
                    key=autor["id"],# El valor que se obtiene al seleccionar
                    text=f"{autor['nombre']} {autor['apellido']}" #Así hacemos un atributo text compuesto. 
                )
            for autor in listDeDictFiltAutores
            ]
            self.menuAutores.options = dropdown_options_autores   

            dropdown_options_generos = [
                ft.dropdown.Option(
                    key=genero["id"],      # El valor que se obtiene al seleccionar
                    text=f"{genero['nombre']}" #Así hacemos un atributo text compuesto. 
                )
            for genero in listDeDictsGeneros
            ]
            self.menuGeneros.options = dropdown_options_generos
            
            dropdown_options_lenguajes = [
                ft.dropdown.Option(
                    key=lenguaje["id"],      # El valor que se obtiene al seleccionar
                    text=f"{lenguaje['nombre']}" #Así hacemos un atributo text compuesto. 
                )
            for lenguaje in listDeDictsLenguajes
            ]
            self.menuLenguajes.options = dropdown_options_lenguajes
            #No actualizamos aquí porque no se han conformado aún los dropdown por la asíncronía que implica el view_will_mount que lo 
#ejecutaremos desde el main con el atributo de View flet, on_will_mount. Todo esto porque no se puede ejecutar métodos asíncronos desde el constructor:

            #self.menuAutores.update()
            #self.menuGeneros.update()
            #self.menuLenguajes.update()
        
"""
    async def botonCrearLibro(self, e):
        self.resultado_texto.value = "Enviando datos..."
        self.pag.update()
        
        datos = {
            "nombre": self.nombre_input.value,
            "apellido": self.apellido_input.value,
            "nacimiento": self.nacimiento_input.value,
            "muerte": self.muerte_input.value
        }

        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                response = await client.post(API_URL_autores, json=datos, timeout=10.0)
                
                if response.status_code == 201:
                    self.resultado_texto.value = "Autor creado exitosamente."
                    self.resultado_texto.color = "green"
                else:
                    self.resultado_texto.value = f"Error {response.status_code}: {response.text}"
                    self.resultado_texto.color = "red" 

        except Exception as ex:
            self.resultado_texto.value = f"Error de conexión: {str(ex)}"
            self.resultado_texto.color = "red"
"""