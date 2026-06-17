import flet as ft

#Así hacemos una barra personalizada para ser utilizada por un cliente que la importe:

@ft.control
class BarraAppBar(ft.AppBar):
    def __init__(self, titulo):
        super().__init__()      
        self.leading=ft.Icon(ft.Icons.MENU),
        self.title=ft.Text(titulo)
        self.bgcolor=ft.Colors.SURFACE_CONTAINER,
        self.actions=[
                ft.IconButton(ft.Icons.SEARCH),
                ft.IconButton(ft.Icons.MORE_VERT),
            ]

@ft.control
class BarraBottomAppBar(ft.BottomAppBar):
    def __init__(self):
        super().__init__()
        self.bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        self.content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.IconButton(ft.Icons.MENU),
                ft.IconButton(ft.Icons.SEARCH),
                ft.IconButton(ft.Icons.SETTINGS),
            ],
        )
