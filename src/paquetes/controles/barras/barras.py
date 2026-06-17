import flet as ft

barraAppBar = ft.AppBar(
    leading=ft.Icon(ft.Icons.MENU),
    title=ft.Text("App de comer moco"),
    bgcolor=ft.Colors.SURFACE_CONTAINER,
    actions=[
        ft.IconButton(ft.Icons.SEARCH),
        ft.IconButton(ft.Icons.MORE_VERT),
    ],
)

barraBottomAppBar = ft.BottomAppBar(
    bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
    content=ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            ft.IconButton(ft.Icons.MENU),
            ft.IconButton(ft.Icons.SEARCH),
            ft.IconButton(ft.Icons.SETTINGS),
        ],
    ),
)