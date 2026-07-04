#navigationDrawerLogin.py

import asyncio
import flet as ft
#from paquetes.controles.formularios.formularios import Formulario_login
from paquetes.aplicaciones.agenda_tareas import TodoApp
from paquetes.aplicaciones.calculadora import AppCalculadora
from paquetes.logicas.apis import SesionJWT

sesion = None

def main(pagina: ft.Page):
    pagina.title = "Cajón de navegación"

    async def manejar_cambio(e):
        if e.control.selected_index == 0:
            await pagina.push_route("/")
        elif e.control.selected_index == 1:
            await pagina.push_route("/todo")
        elif e.control.selected_index == 2:
            await pagina.push_route("/calculadora")

    def crear_cajonNav(indice_seleccionado=0):
        return ft.NavigationDrawer(
            selected_index=indice_seleccionado,
            on_change=manejar_cambio,
            #disabled = True,
            #visible = True if auth_state["access_token"] is not None else False,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Ingresar",
                    icon=ft.Icons.HOME_OUTLINED, 
                    visible = True, #if auth_state["access_token"] is not None else False,
                    selected_icon=ft.Icon(ft.Icons.HOME),
                    #disabled=True if auth_state["access_token"] is not None else False
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="To-do",
                    icon=ft.Icon(ft.Icons.STORE_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.STORE),
                    #disabled=True if auth_state["access_token"] is None else False
                ),
                ft.NavigationDrawerDestination(
                    label="Calculadora",
                    icon=ft.Icon(ft.Icons.PHONE_OUTLINED),
                    selected_icon=ft.Icons.PHONE,
                    #disabled=True if auth_state["access_token"] is None else False
                ),
            ],
        )

    async def mostrar_cajonNav():
        await pagina.show_drawer()

    async def logeo(e):
        error_text.value =""
        sesion = SesionJWT(email.value, password.value, pagina)
        await sesion.handle_login()
        error_text.value = sesion.error_text
        email.value = ""
        password.value = ""
        pagina.update()

    def logout(e):
        pass
    
    #Definimos los controles que se usaran a nivel del main para poder funcionar:
    error_text = ft.Text(color=ft.Colors.RED)
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Contraseña")
    botonEnviar = ft.Button("Entrar", on_click=logeo)

    def cambio_ruta(route):
        pagina.views.clear()
        pagina.views.append(
            ft.View(
                route="/",
                controls=[
                    ft.SafeArea(
                        content=ft.Column(
                            controls=[
                                ft.AppBar(
                                    title=ft.Text("Abrir sesión", expand=True),
                                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                    leading=ft.IconButton(
                                        ft.Icons.MENU,
                                        #disabled=True if auth_state["access_token"] is None else False,
                                        on_click=mostrar_cajonNav
                                    ),
                                ),
                                email,
                                password,
                                botonEnviar,
                                error_text,   
                            ]
                        )
                    )
                ],
                drawer=crear_cajonNav(indice_seleccionado=0) if pagina.route == "/" else None,
            )
        )

        if pagina.route == "/todo":
            pagina.views.append(
                ft.View(
                    route="/todo",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column(
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("To-Do", expand=True),
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                        leading=ft.IconButton(
                                            ft.Icons.MENU, on_click=mostrar_cajonNav
                                        ),
                                        automatically_imply_leading=False,
                                        actions=[
                                            ft.Text(
                                                f'usuario:{"david"}',
                                                visible=True if sesion is None else False
                                            )
                                        ]
                                    ),
                                    TodoApp(),
                                    ft.Button(
                                        "Ir a calculadora",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/calculadora")
                                        ),
                                    ),
                                ]
                            )
                        )
                    ],
                    drawer=crear_cajonNav(indice_seleccionado=1),
                )
            )

        if pagina.route == "/calculadora":
            pagina.views.append(
                ft.View(
                    route="/calculadora",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column(
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("Calculadora", expand=True),
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                        leading=ft.IconButton(
                                            ft.Icons.MENU, on_click=mostrar_cajonNav
                                        ),
                                        automatically_imply_leading=False,
                                    ),
                                    AppCalculadora(),
                                    ft.Button(
                                        "Ir a To-Do",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/todo")
                                        ),
                                    ),
                                ]
                            )
                        )
                    ],
                    drawer=crear_cajonNav(indice_seleccionado=2),
                )
            )
        pagina.update()

    async def vista_pop(view):
        pagina.views.pop()
        top_view = pagina.views[-1]
        await pagina.push_route(top_view.route)

    pagina.on_route_change = cambio_ruta
    pagina.on_view_pop = vista_pop
    cambio_ruta(pagina.route)


if __name__ == "__main__":
    ft.run(main)