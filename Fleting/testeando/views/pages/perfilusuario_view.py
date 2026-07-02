import flet as ft
from views.layouts.main_layout import MainLayout, MainLayout2
from controllers.perfilusuario_controller import PerfilusuarioController

class PerfilusuarioView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
        self.controller = PerfilusuarioController()

    def render(self):
        content = ft.Column(
            controls=[
                ft.Text(self.controller.get_title(), size=12),
            ],
            spacing=16,
        )
        print(f'self.page.multi_views = {self.page.multi_views}')

        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
