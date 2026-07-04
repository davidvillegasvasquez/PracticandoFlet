
import flet as ft

@ft.control
class Formulario_login(ft.Column):
    #monitoreo_encendido: bool = True
    # --- 1. Formularios y Pantallas ---

    def init(self):
    # Vista de Login
        self.email_field = ft.TextField(label="Email")
        self.password_field = ft.TextField(label="Contraseña")

        self.controls = [
            self.email_field, 
            self.password_field,
        ]
    """
    def obtener_datos(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()
    """
