#Atributos propiedad del control Page.
import flet as f

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

    pagina.add(boton)

f.run(principal)