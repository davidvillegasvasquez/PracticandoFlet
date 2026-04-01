#botonPersonalizado.py
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

veces = 0
def principal(pagina: f.Page):
    pagina.tittle="Boton Personalizado"

    def imprimirEnConsola(evento):
        global veces
        veces+=1
        print(f'Haz pulsado el botón {veces} veces.')
        
    boton=BotonPersonalizado(
        texto="click aquí",
        icono=None,
        funcionPasada=imprimirEnConsola
    )

    pagina.add(boton)

f.run(principal)