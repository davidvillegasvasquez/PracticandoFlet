
import flet as ft
from views.layouts.main_layout import MainLayout

class HomeView:
    def __init__(self, page, router):
        self.page = page
        self.router = router
    
    def render(self):
        content = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=12,
            controls=[
                ft.Image(
                    src="icon.png",
                    width=48,
                    height=48,
                    fit="contain",
                ),
                ft.Text(
                    "Fleting Framework",
                    size=12,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    "Micro Framework MVC for Flet",
                    size=12,
                    color=ft.Colors.GREY_600,
                ),
                ft.Text(
                    "Build modern applications with a clear architecture, "
                    "Dynamic routing and productive CLI.",
                    size=10,
                    text_align=ft.TextAlign.CENTER,
                    width=480,
                ),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.FilledButton(
                            "Settings",
                            icon=ft.Icons.SETTINGS, #ft.Icons.SETTINGS
                            on_click=lambda e: self.router.navigate("/settings"),
                        ),
                        ft.OutlinedButton(
                            "Create new page",
                            icon=ft.Icons.ADD,
                        ),
                    ],
                ),
            ],
        )

        # LAYOUT
        return MainLayout(
            page=self.page,
            content=content,
            router=self.router,
        )
