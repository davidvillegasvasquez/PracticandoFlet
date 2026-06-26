from dataclasses import field
import flet as ft

#Tarea: hacer una clase botón genérica de enviar
#botonEnviar = ft.Button("Enviar", on_click=send_click)

@ft.control
class CalcButton(ft.Button):
    expand: int = field(default_factory=lambda: 1)

@ft.control
class DigitButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.WHITE_24
    color: ft.Colors = ft.Colors.WHITE

@ft.control
class ActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.ORANGE
    color: ft.Colors = ft.Colors.WHITE

@ft.control
class ExtraActionButton(CalcButton):
    bgcolor: ft.Colors = ft.Colors.BLUE_GREY_100
    color: ft.Colors = ft.Colors.BLACK

@ft.control
class BotonPersonalizado(ft.Button):
    def __init__(self, texto: str, icono=None, funcionPasada=None):
        super().__init__()
        self.content=texto
        self.icon=icono if icono else ft.Icons.ADD
        self.on_click=funcionPasada #funcionPasada
        self.color="black"
    
    def build(self):
        self.bgcolor="green"
