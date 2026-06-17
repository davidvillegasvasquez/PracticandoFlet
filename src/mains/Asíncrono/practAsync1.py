#practAsync1.py
import asyncio
import flet as ft

def cuerpo(pagina: ft.Page):
    async def button_click(e):
        await asyncio.sleep(5)
        texto.value = "Hola con retraso de 5 segundos!"
        botonImprimir.disabled = True

    def borrar(e):
        texto.value=""
        botonImprimir.disabled = False

    texto = ft.Text()
    botonBorrar = ft.Button("Borrar", on_click=borrar)
    botonImprimir = ft.Button("Hola luego de 5 seg", on_click=button_click)

    pagina.add(
        texto,
        botonImprimir,
        botonBorrar,
    )

ft.run(cuerpo)