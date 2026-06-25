import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.login_controller import LoginController
from core.state import AppState as AS

class LoginView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.control = LoginController()

    def render(self):
        self.email_user = ft.TextField(label="Email", width=80, height=20)
        self.password = ft.TextField(label="pass", width=80, height=20)
        self.respuesta = ft.Text(color=ft.Colors.RED)
        self.boton_ingresar = ft.Button("Entrar", on_click=self.ingresar)
        
        content = ft.Column(
            controls=[
                ft.Text(self.control.get_title(), size=12),
                self.email_user,
                self.password,
                self.respuesta,
                self.boton_ingresar,
            ],
            spacing=10,
        )

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )

    def ingresar(self, e):
        self.control.set_email(self.email_user.value)
        self.control.set_pass(self.password.value)
        AS.usuario = self.control.get_email()
