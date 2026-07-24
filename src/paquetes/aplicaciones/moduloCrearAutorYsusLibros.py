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

#--------------------------------

class CrearLibro(ft.Column):
    def __init__(self, pagina, sesion):
        super().__init__()
        self.pag = pagina
        self.sesion = sesion
        #En un modelo asíncrono, si quieres ver los controles precargados con datos de los endpoints al navegar a la vista, debes inicializarlos primero en el constructor y no en el método build:
        self.menuAutores = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Autores",
            options=[],
            on_select="",
            )

        self.menuGeneros=ft.ListView(controls=[], expand=True)

        self.menuLenguajes = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Lenguaje",
            options=[],
            on_select="",
            )
    
    def build(self):
        #Declaración de los controles que deben mostrarse precarcados al ir a la vista:
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
            ft.Container(
                height=100, # Define el área visible para forzar scroll
                width=250, # Espacio entre elementos
                padding=10,
                border=ft.Border.all(1, ft.Colors.BLACK),
                border_radius=ft.BorderRadius.all(value=5),
                content=self.menuGeneros,
            ),
            self.menuLenguajes,
            ft.Button("Crear", on_click=self.botonCrearLibro),
            self.resultado_texto,
        ]

    #Método para ejecutar desde main con el atributo método de los objetos ft.View, on_will_mount (vista.on_will_mount):
    async def laVista_se_montara(self):
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
            #Tomamos el primer elemento de results que es una lista de diccionarios con los campos del modelo:
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
            #Filtramos listDeDictsAutores para extraer los campos deseados (id y nombre) de cada uno de los diccionarios que contienen los datos del autor. Los otros dos no necesitan ser filtrados porque sólo tinen id y nombre:
            listDeDictFiltAutores = [{"id": d["id"], "nombre": d["nombre"], "apellido": d["apellido"]} for d in listDeDictsAutores]

            #Hacemos los dropdowns:
            dropdown_options_autores = [
                ft.dropdown.Option(
                    key=autor["id"],# El valor que se obtiene al seleccionar
                    text=f"{autor['nombre']} {autor['apellido']}" #Así hacemos un atributo text compuesto. 
                )
            for autor in listDeDictFiltAutores
            ]
            self.menuAutores.options = dropdown_options_autores 

            #Para genero hacemo una lista de checkboxs porque no existe un dropdown de selección múltiple:          
            self.menuGeneros.controls = [
                ft.Checkbox(
                    label=task["nombre"],
                    value=False,
                    # Attaching a full dictionary to the data attribute
                    data=task["id"],
                    on_change="" #on_task_toggle
                ) 
                for task in listDeDictsGeneros
            ]          

            dropdown_options_lenguajes = [
                ft.dropdown.Option(
                    key=lenguaje["id"], 
                    text=lenguaje['nombre'] 
                )
            for lenguaje in listDeDictsLenguajes
            ]
            self.menuLenguajes.options = dropdown_options_lenguajes
            #No actualizamos los controles aquí porque no se han conformado aún por la asíncronía que implica el view_will_mount que lo 
#ejecutaremos desde su cliente, main, con el atributo de la clase View flet, on_will_mount. Todo esto porque no se puede ejecutar métodos asíncronos desde el constructor:

            #self.menuAutores.update()
            #self.menuGeneros.update()
            #self.menuLenguajes.update()
        
    async def botonCrearLibro(self, e):
        self.resultado_texto.value = "Enviando datos..."
        self.pag.update()

        #Lamentablemente tenemos que hacer el trabajon de ubicar y extraer los valores seleccionados en los menus dropdown y la lista de checkboxs. No existe una forma directa como si fuera una lista o dict:
        
        #Recuerde que self.menuAutores.value es un str que representa el id, y key=autor["id"] en este caso guarda un entero, por lo cual tenemos que convertirlo a entero para poder compararlos en su busqueda posterior. Lo mismo aplica a lenguaje:

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

        #Por comprensión de listas creamos la lista de generos seleccionados:
        gen_selec=[
            cb.data for cb in self.menuGeneros.controls if cb.value
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

        """
        Aquí no necesitamos obtener el valor literal de los campos porque estamos usando un serializador hipervinculado, lo cual requiere el número del índice del item para construir a partir de este la url necesaria, y no un str. En vistas basadas en serializadores normales si necesitaríamos ese valor literal directamente.
        # Iteramos sobre las opciones para extraer el texto
        autor_selec = next((opt.text for opt in self.menuAutores.options if opt.key == val_select_autor), None)
        
        genero_selec = next((opt.text for...
        """
        #Procedemos a contruir la payload o cuerpo (body) de la petición o solicitud:
        datos = {
            "titulo": self.titulo_input.value,
            #Debemos usar el patron modelo_id en los campos con relaciones foreingkey, porque vamos a construir urls con serializadores hipervinculados, y trabajamos en base del campo relacionado para construirlos:
            "autor_id": val_select_autor,
            "descripcion": self.descripcion_input.value,
            "isbn": self.isbn_input.value,
            "genero": gen_selec,
            "lenguaje_id": val_select_len
        }

        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                response = await client.post(API_URL_libros, json=datos, timeout=10.0)
                
                if response.status_code == 201:
                    self.resultado_texto.value = "Libro creado exitosamente."
                    self.resultado_texto.color = "green"
                    #self.pag.push_route("/")
                else:
                    self.resultado_texto.value = f"Error {response.status_code}: {response.text}"
                    self.resultado_texto.color = "red" 

        except Exception as ex:
            self.resultado_texto.value = f"Error de conexión: {str(ex)}"
            self.resultado_texto.color = "red"
