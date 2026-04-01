#El control container.
import flet as ft

def principal(pagina: ft.Page):
    pagina.title = "Ejemplo de Contenedores"
    pagina.theme_mode = ft.ThemeMode.LIGHT
    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    pagina.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Text("No clicleable"),
                    margin=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.AMBER,
                    width=150,
                    height=150,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Text("Clicleable sin entintar"),
                    margin=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.GREEN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=lambda e: print("Clickable sin entintar clicleada!"),
                ),
                ft.Container(
                    content=ft.Text("Clicleable con entintada"),
                    margin=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.CYAN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    ink=True, #ink da cambio de color al pasar cursor sobre el.
                    on_click=lambda e: print("Clickable con entintada clicleada!"),
                ),
                ft.Container(
                    content=ft.Text("Clickable transparente con entintada"),
                    margin=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                    width=150,
                    height=150,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Clickable transparente con entintada clicked!"),
                ),
            ],
        ),
    )

    pagina.add(ft.Button(content="Enabled button")) #add diferido.  

    contenedor = ft.Container(
                    content=ft.Button(
                        width=120,
                        height=30,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.FAVORITE, color=ft.Colors.PINK),
                                ft.Icon(ft.Icons.AUDIOTRACK,                color=ft.Colors.GREEN),
                                ft.Icon(ft.Icons.BEACH_ACCESS, color=ft.Colors.BLUE),
                            ],
                        ),
                    ),
                        margin=10,
                        bgcolor=ft.Colors.CYAN_200,
                        padding=10,
                        alignment=ft.Alignment.CENTER,
                        width=200,
                        height=200,
                        border_radius=10,
                        ink=True,
                    )   
    
    pagina.add(contenedor) #add diferido.

ft.run(principal)