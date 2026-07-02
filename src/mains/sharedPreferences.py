#sharedPreferences.py
import flet as ft

async def main(page: ft.Page):
    async def fijar_valor():
        
        await ft.SharedPreferences().set(clave_in.value, valor_in.value)
        obtener_clave.value = clave_in.value
        obtener_valor.value = valor_in.value 
        page.show_dialog(ft.SnackBar(f'Valor {obtener_valor.value} guardado en SharedPreferences con clave "{obtener_clave.value}"'))
        clave_in.value = ""
        valor_in.value = ""

    async def obtener_valor():
        contenido = await ft.SharedPreferences().get(obtener_clave.value)
        page.add(ft.Text(f"SharedPreferences contenido de esa clave: {contenido}"))

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    clave_in := ft.TextField(label="Clave"),
                                    valor_in := ft.TextField(label="Valor"),
                                    ft.Button("Fijar", on_click=fijar_valor),
                                ]
                            ),
                            ft.Row(
                                [
                                    obtener_clave := ft.TextField(label="Clave"),
                                    ft.Button("Obtener", on_click=obtener_valor),
                                ]
                            ),
                        ],
                    )
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)