#ej1.py
import flet as ft

def principal(pagina: ft.Page):

    pagina.title = "ej1"
    fila_ej = ft.Row(
        controls=[
            ft.Container(content=ft.Text("Hola1"), bgcolor="blue", padding=10),
            ft.Container(content=ft.Text("Hola2"), bgcolor="yellow", padding=10),
            ft.Container(content=ft.Text("Hola3", color="white"), bgcolor="black", padding=10),
        ]
    )

    columna_ej = ft.Column(
        controls=[
            ft.Container(content=ft.Text("Hola1"), bgcolor="blue", padding=10),
            ft.Container(content=ft.Text("Hola2"), bgcolor="yellow", padding=10),
            ft.Container(content=ft.Text("Hola3",color="white"), bgcolor="black", padding=5),
        ]
    )

    pagina.add(fila_ej, columna_ej)

ft.run(principal)