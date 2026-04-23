from dataclasses import field
import flet as f

#Tarea: hacer una clase botón genérica de enviar
#botonEnviar = f.Button("Enviar", on_click=send_click)

@f.control
class CalcButton(f.Button):
    expand: int = field(default_factory=lambda: 1)

@f.control
class DigitButton(CalcButton):
    bgcolor: f.Colors = f.Colors.WHITE_24
    color: f.Colors = f.Colors.WHITE

@f.control
class ActionButton(CalcButton):
    bgcolor: f.Colors = f.Colors.ORANGE
    color: f.Colors = f.Colors.WHITE

@f.control
class ExtraActionButton(CalcButton):
    bgcolor: f.Colors = f.Colors.BLUE_GREY_100
    color: f.Colors = f.Colors.BLACK