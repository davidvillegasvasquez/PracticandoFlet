#Atributos propiedad del control Page.
import flet as f
#from paquetes.controles.barras.barras import barraAppBar, barraBottomAppBar

@f.control
class BotonPersonalizado(f.Button):
    def __init__(self, texto: str, icono=None, funcionPasada=None):
        super().__init__()
        self.content=texto
        self.icon=icono if icono else f.Icons.ADD
        self.on_click=funcionPasada #funcionPasada
        self.color="black"
    
    def build(self):
        self.bgcolor="green"

def principal(pagina: f.Page):
    pagina.tittle="Atributos de Page"

    def imprimirEnConsola(evento):
        print(f'pagina.client_ip = {pagina.client_ip}')
        print(f'pagina.client_user_agent = {pagina.client_user_agent}')
        print(f'pagina.platform = {pagina.platform}')
        print(f'pagina.platform_brightness = {pagina.platform_brightness}')
        print(f'pagina.route = {pagina.route}')
        print('================================')

    
    boton=BotonPersonalizado(
        texto="click aquí",
        icono=None,
        funcionPasada=imprimirEnConsola
    )
    
    pagina.appbar = f.AppBar(
        leading=f.Icon(f.Icons.MENU),
        title=f.Text("App de comer moco"),
        bgcolor=f.Colors.SURFACE_CONTAINER,
        actions=[
            f.IconButton(f.Icons.SEARCH),
            f.IconButton(f.Icons.MORE_VERT),
        ],
    )

    pagina.bottom_appbar = f.BottomAppBar(
        bgcolor=f.Colors.SURFACE_CONTAINER_LOW,
        content=f.Row(
            alignment=f.MainAxisAlignment.SPACE_AROUND,
            controls=[
                f.IconButton(f.Icons.MENU),
                f.IconButton(f.Icons.SEARCH),
                f.IconButton(f.Icons.SETTINGS),
            ],
        ),
    )
    #Así se importan controles sencillos desde paquetes para asignarlos a los atributos de la página. Claro, se supone que el control importado a asignar sea del tipo del atributo: Esto arroja error al rato. Debe ser funciones o clases.
    #pagina.appbar = barraAppBar
    #pagina.bottom_appbar = barraBottomAppBar

    #pagina.add(barraAppBar, boton, barraBottomAppBar)
    pagina.add(boton)

f.run(principal)