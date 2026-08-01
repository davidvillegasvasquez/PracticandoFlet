import flet as ft
import asyncio
import httpx

#Estas direcciones hay que importarlas dese un módulo de constantes:
API_URL_libros = "http://127.0.0.1:8000/catalogo/apirest/libros/"
API_URL_generos = "http://127.0.0.1:8000/catalogo/apirest/generos/"
API_URL_lenguajes = "http://127.0.0.1:8000/catalogo/apirest/lenguajes/"

class PatchLibro(ft.Column):
    def __init__(self, pagina, sesion):
        super().__init__()
        self.pag = pagina
        self.sesion = sesion
        #Definimos menuLibros y menuLenguajes aquí en el constructor porque lo necesitamos precargado al abrir esta vista y menuLenguajes estará en on_will_mount:
        self.menuLibros = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Libros",
            options=[],
            on_select=self.rellenarCamposLibroSelec
            )
        #Dropdown que muestra el lenguaje actual como seleccionado:
        self.menuLenguajes = ft.Dropdown(
            editable=True,                            
            width=220,
            label="Lenguaje",
            options=[],
            )
        #Creamos el atributo generos y lenguajes, que son listas de diccionarios para tener todos los generos y lenguajes al cargar, que mostraremos como checkboxs en generos, y expresamos los de un libro en particular como checkboxs marcados (value=True):
        self.generos = []
        #self.lenguajes = []
        #Necesitamos este id como atributo propiedad de la clase porque lo usamos tanto en el método rellenarCamposLibroSelec como en el de actualizar, 
#específicamente en la construcción de la url de la solicitud patch (client.patch(f"{API_URL_libros}{self.idLibroSeleccionado}/")):
        self.idLibroSeleccionado = None
        
    
    def build(self):
        #Dibujo de los controles que deben mostrarse precarcados al ir a la vista:
        self.menuGeneros=ft.ListView(controls=[], expand=True)
        self.autor_input = ft.TextField(label="Autor", disabled=True)
        #Configuración de un TextField para textos largos. Comienza con 3 lineas visible, a la 6ta para comenzar hacer scroll:
        self.descripcion_input = ft.TextField(label="Descripción", multiline=True, min_lines=3, max_lines=5)
        self.isbn_input = ft.TextField(label="Isbn")
        self.resultado_texto = ft.Text()

        self.controls = [
            self.menuLibros,
            self.autor_input,
            self.descripcion_input,
            self.isbn_input,
            ft.Container(
                height=250, 
                width=250,
                padding=10,
                border=ft.Border.all(1, ft.Colors.BLACK),
                border_radius=ft.BorderRadius.all(value=5),
                content=self.menuGeneros,
            ),
            self.menuLenguajes,
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
                respuestaLenguajes = await client.get(API_URL_lenguajes)
                #Obtenemos aquí la lista de todos los generos para no cargar tanto el método rellenarCamposLibroSelec, además que es una sola lista de valores
#que se pedirá una sola vez mientas el usuario elige un libro a modificar, en este caso la de Libros:  
                respuestaGeneros = await client.get(API_URL_generos)

            #Rellenamos con lo valores consultados. Recuerde que cada uno de ellos es una lista de dicts, no un sólo dict:
            diccionarioLibros = respuestaLibros.json()
            diccionarioLenguajes = respuestaLenguajes.json()
            diccionarioGeneros = respuestaGeneros.json()
            
            self.listDeDictsLibros = diccionarioLibros['results']
            listDeDictsLenguajes = diccionarioLenguajes['results']
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

            dropdown_options_lenguajes = [
                ft.dropdown.Option(
                    key=lenguaje["id"], 
                    text=lenguaje['nombre'] 
                )
            for lenguaje in listDeDictsLenguajes
            ]
            self.menuLenguajes.options = dropdown_options_lenguajes

            #Por supuesto no actualizamos la página con sus controles aquí, porque será montada con on_will_mount en main.
    
    async def rellenarCamposLibroSelec(self, e):
        """
        El método asociado al evento de seleccionar un libro en el dropdown de libros. Toma los datos actuales del libro seleccionado y los coloca en controles que pueden ser editados, listos para accionar el botón de actualizar y tomar los nuevos valores en dichos campos editables (descripción, isbn, generos y lenguaje).
        """
   
        self.idLibroSeleccionado = int(e.control.value)
        
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
            self.menuLenguajes.value = dictLenguajeSelec['id']
            #Finalmente actualizamos para hacer visible los cambios:
            self.pag.update()

        
    async def actualizar(self, e):
        self.resultado_texto.value = "Enviando datos..."
        self.pag.update()

        #Nuevamente, validamos que el usuario no deje vacío los campos:

        #Por comprensión de listas creamos la lista de ids de los generos seleccionados que fue guardado en su atributo data:
        gens_selecs_ids=[
            checkbox.data for checkbox in self.menuGeneros.controls if checkbox.value
        ]
       
        if gens_selecs_ids: #Lista no vacía, el usuario seleccionó al menos un genero.
            #Ahora, tenemos que crear la lista de urls de generos seleccionados, porque los campos hipervinculados trabajan sólo con urls:
            urls_gens_selecs = [
                dictGen['url'] for dictGen in self.generos if dictGen['id'] in gens_selecs_ids
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
        
        if self.menuLenguajes.value is not None:
            #Tenemos que construir la url, porque en serialización hipervinculada las solicitudes patch no se construyen a partir de enteros, si no en cadenas url.
            #Recuerde que API_URL_lenguajes tiene un / al final. Si colocamos / en la cadena que estamos construyendo, se producirá un error como: PATCH /catalogo/apirest/lenguajes//5/ HTTP/1.1" 404
            url_lenguaje_selec = f"{API_URL_lenguajes}{self.menuLenguajes.value}/"
           
        else:
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Error de ingreso"),
                content=ft.Text('Debe seleccionar un lenguaje.'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))
            return
   
        #Procedemos a contruir la payload o cuerpo (body) de la petición o solicitud:
        datos = {
            "descripcion": self.descripcion_input.value,
            "isbn": self.isbn_input.value,
            "genero": urls_gens_selecs,
            "lenguaje": url_lenguaje_selec
        }

        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
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


class EliminarLibro(PatchLibro):
    
    def build(self):
        # 1. Run original build
        super().build()  

        # 3. Invisibilizamos todos los controles excepto self.menuLibros:
        for control in self.controls:
            if control not in (self.menuLibros, self.resultado_texto):
                control.visible = False    

        
        #Reescribimos el atributo on_select de menuLibros con el nuevo método:
        self.menuLibros.on_select=self.borrarLibro
    

    async def borrarLibro(self, e):
        self.idLibroSeleccionado = int(e.control.value)
        
        # Extraemos el diccionario que expresa el registro del libro seleccionado entre todos los registros-diccionarios contenidos en self.listDeDictsLibros:
#Será uno así: {'url': 'http://127.0.0.1:8000/catalogo/apirest/libros/4/', 'id': 4, 'titulo': 'Canaima', 'autor': 'http://127.0.0.1:8000/catalogo/apirest/autores/2/', 'descripcion': 'Canaima es una novela ...', 'isbn': '9798886451740', 'genero': ['http://127.0.0.1:8000/catalogo/apirest/generos/1/'], 'lenguaje': 'http://127.0.0.1:8000/catalogo/apirest/lenguajes/1/'}

        self.dictLibroSelec = next((libro for libro in self.listDeDictsLibros if libro['id'] == self.idLibroSeleccionado), None)

        #Procedemos a borrar:
        self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Eliminar libro"),
                content=ft.Text(f'Desea eliminar el libro: {self.dictLibroSelec["titulo"]} ?'),
                actions=[ft.TextButton("Eliminar", on_click=self.eliminar), ft.TextButton("Otra opción", on_click=lambda e:salir())],
                modal=True
            ))
        #self.resultado_texto.value = "Enviando datos..."
        self.pag.update()

        def salir():
            self.pag.pop_dialog()
            return

    #Método eliminar:
    async def eliminar(self, e):
            #Borramos el cuadro de dialogo emergente:
            self.pag.pop_dialog()
            self.resultado_texto.value = "Enviando datos..."
            self.pag.update()
            #Procedemos a borrar el libro:
            
            try:
                async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                    respuestaBorrarLibro = await client.delete(f"{API_URL_libros}{self.idLibroSeleccionado}/") 

                    if respuestaBorrarLibro.status_code == 204:
                        #Aqui se debe meter un modal y redirigir a home:
                        self.resultado_texto.value = "Libro eliminado exitosamente."
                        self.resultado_texto.color = "green"
                        #Averiguar como actualizar menuLibros porque esto no lo hace:
                        self.menuLibros.update()
                        self.pag.update()
                        return 
                    else:
                        self.resultado_texto.value = f"Error {respuestaBorrarLibro.status_code}: {respuestaBorrarLibro.text}"
                        self.resultado_texto.color = "red"

            except Exception as error:
                
                self.pag.show_dialog(ft.AlertDialog(
                    title=ft.Text("Ocurrió un error..."),
                    content=ft.Text(f'Error: {error}'),
                    actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                    modal=True
                ))

            else: 
                pass        
