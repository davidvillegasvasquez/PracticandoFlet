import flet as f
from paquetes.controles.marcos import Tarea

@f.control
class TodoApp(f.Column):
    # application's root control is a Column containing all other controls
    def init(self):
        self.nueva_tarea = f.TextField(hint_text="Que tareas tienes pendiente y que no haras?", expand=True)
        self.tareas = f.Column()
        self.width = 600
        self.controls = [
            f.Row(
                controls=[
                    self.nueva_tarea,
                    f.FloatingActionButton(
                        icon=f.Icons.ADD, on_click=self.botonAgregarClickeado
                    ),
                ],
            ),
            self.tareas,
        ]

    def botonAgregarClickeado(self, e):
        tarea = Tarea(tarea_nombre=self.nueva_tarea.value, on_task_delete=self.tarea_borrar)
        self.tareas.controls.append(tarea)
        self.nueva_tarea.value = ""
        self.update()

    def tarea_borrar(self, tarea):
        self.tareas.controls.remove(tarea)
        self.update()
