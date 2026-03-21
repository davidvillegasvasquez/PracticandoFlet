import flet as f
from dataclasses import field
from typing import Callable

@f.control
class Tarea(f.Column):
    tarea_nombre: str = ""
    on_task_delete: Callable[["Tarea"], None] = field(default=lambda tareax: None)

    def init(self):
        self.mostrar_tarea = f.Checkbox(value=False, label=self.tarea_nombre)
        self.editar_nombre = f.TextField(expand=1)

        self.mostrar_vista = f.Row(
            alignment=f.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=f.CrossAxisAlignment.CENTER,
            controls=[
                self.mostrar_tarea,
                f.Row(
                    spacing=0,
                    controls=[
                        f.IconButton(
                            icon=f.Icons.CREATE_OUTLINED,
                            tooltip="Editar",
                            on_click=self.editar_clickeado,
                        ),
                        f.IconButton(
                            icon=f.Icons.DELETE_OUTLINE,
                            tooltip="Borrar",
                            on_click=self.borrar_clickeado,
                        ),
                    ],
                ),
            ],
        )

        self.editar_vista = f.Row(
            visible=False,
            alignment=f.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=f.CrossAxisAlignment.CENTER,
            controls=[
                self.editar_nombre,
                f.IconButton(
                    icon=f.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=f.Colors.GREEN,
                    tooltip="Actualizar",
                    on_click=self.guardar_clickeado,
                ),
            ],
        )
        self.controls = [self.mostrar_vista, self.editar_vista]

    def editar_clickeado(self, e):
        self.editar_nombre.value = self.mostrar_tarea.label
        self.mostrar_vista.visible = False
        self.editar_vista.visible = True
        self.update()

    def guardar_clickeado(self, e):
        self.mostrar_tarea.label = self.editar_nombre.value
        self.mostrar_vista.visible = True
        self.editar_vista.visible = False
        self.update()

    def borrar_clickeado(self, e):
        self.on_task_delete(self)
