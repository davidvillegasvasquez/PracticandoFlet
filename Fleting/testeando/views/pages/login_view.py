import flet as ft
from views.layouts.main_layout import MainLayout
from controllers.login_controller import LoginController

class LoginView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.controller = LoginController()

    def render(self):
        content = ft.Column(
            controls=[
                ft.Text(self.controller.get_title(), size=24),
                ft.TextField(label="Email", value=self.controller.get_email()),
                ft.TextField(label="Contraseña"),
                ft.Text(color=ft.Colors.RED),
                ft.Button("Entrar", on_click=""),
            ],
            spacing=16,
        )

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
