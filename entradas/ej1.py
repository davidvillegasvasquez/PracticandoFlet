import flet as ft

def principal(pagina: ft.Page):

    pagina.title = "ej1"
    fila_ej = ft.Row(
        controls=[
            ft.Container(content=ft.Text("Hola1"), bgcolor="blue", padding=10),
            ft.Container(content=ft.Text("Hola2"), bgcolor="yellow", padding=10),
            ft.Container(content=ft.Text("Hola3"), bgcolor="black", padding=20),
        ]
    )

    columna_ej = ft.Column(
        controls=[
            ft.Container(content=ft.Text("Hola1"), bgcolor="blue", padding=10),
            ft.Container(content=ft.Text("Hola2"), bgcolor="yellow", padding=10),
            ft.Container(content=ft.Text("Hola3"), bgcolor="black", padding=20),
        ]
    )

    pagina.add(fila_ej, columna_ej)

ft.run(principal)