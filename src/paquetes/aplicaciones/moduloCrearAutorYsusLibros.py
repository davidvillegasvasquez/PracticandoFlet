import flet as ft
import asyncio
import httpx

API_URL = "http://127.0.0.1:8000/catalogo/apirest/autores/"

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
                response = await client.post(API_URL, json=datos, timeout=10.0)
                
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
    
    def build(self):
        self.menuAutores = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Autores",
            options=["x", "y"],
            on_select="",
            )

        self.menuGeneros = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Genero",
            options=["x", "y"],
            on_select="",
            )

        self.menuLenguajes = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Lenguaje",
            options=["x", "y"],
            on_select="",
            )

        self.titulo_input = ft.TextField(label="Nombre")
        self.descripcion_input = ft.TextField(label="Descripción") #multiline ideal para textos largos.
        self.isbn_input = ft.TextField(label="Isbn")
        self.resultado_texto = ft.Text()

        self.controls = [
            self.titulo_input,
            self.menuAutores,
            self.descripcion_input,
            self.isbn_input,
            #ft.Column(controls=[self.menuGeneros, self.menuLenguajes]),
            self.menuGeneros,
            self.menuLenguajes,
            ft.Button("Crear", on_click=self.cargarAutores),
            self.resultado_texto
        ]

    def cargarAutores(self, e):
        self.pag.update()
"""
    async def cargarAutoresGenerosYlenguajes(self, e):
        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                respuestaAutores = await client.get(API_URL)     

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
            self.listaFiltrada = [{"id": d["id"], "nombre": d["nombre"], "apellido": d["apellido"]} for d in listDeDicts]

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
                response = await client.post(API_URL, json=datos, timeout=10.0)
                
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