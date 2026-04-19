#tareas.py
import flet as f
from paquetes.aplicaciones.agenda_tareas import TodoApp
from paquetes.aplicaciones.calculadora import AppCalculadora

def entrada(pagina: f.Page):
    pagina.title = "AppDeTareas"
    pagina.horizontal_alignment = f.CrossAxisAlignment.CENTER
    pagina.scroll = f.ScrollMode.AUTO
    pagina.update()
    # create application instance
    #app = TodoApp()
    # add application's root control to the pagina
    pagina.add(TodoApp(), AppCalculadora())

f.run(entrada)