#navigationDrawer.py

import asyncio

import flet as ft

def main(pagina: ft.Page):
    pagina.title = "Drawer navigation"

    async def manejar_cambio(e):
        if e.control.selected_index == 0:
            await pagina.push_route("/")
        elif e.control.selected_index == 1:
            await pagina.push_route("/store")
        elif e.control.selected_index == 2:
            await pagina.push_route("/about")

    def crear_cajonNav(indice_seleccionado=0):
        return ft.NavigationDrawer(
            selected_index=indice_seleccionado,
            on_change=manejar_cambio,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Home",
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.HOME),
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Store",
                    icon=ft.Icon(ft.Icons.STORE_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.STORE),
                ),
                ft.NavigationDrawerDestination(
                    label="About",
                    icon=ft.Icon(ft.Icons.PHONE_OUTLINED),
                    selected_icon=ft.Icons.PHONE,
                ),
            ],
        )

    async def mostrar_cajonNav():
        await pagina.show_drawer()

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
                                    title=ft.Text("Home", expand=True),
                                    bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                    leading=ft.IconButton(
                                        ft.Icons.MENU, on_click=mostrar_cajonNav
                                    ),
                                ),
                                ft.Text("Welcome to Home Page"),
                            ]
                        )
                    )
                ],
                drawer=crear_cajonNav(indice_seleccionado=0) if pagina.route == "/" else None,
            )
        )

        if pagina.route == "/store":
            pagina.views.append(
                ft.View(
                    route="/store",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column(
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("Store", expand=True),
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                        leading=ft.IconButton(
                                            ft.Icons.MENU, on_click=mostrar_cajonNav
                                        ),
                                        automatically_imply_leading=False,
                                    ),
                                    ft.Text("Welcome to Store Page"),
                                    ft.Button(
                                        "Go About",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/about")
                                        ),
                                    ),
                                ]
                            )
                        )
                    ],
                    drawer=crear_cajonNav(indice_seleccionado=1),
                )
            )

        if pagina.route == "/about":
            pagina.views.append(
                ft.View(
                    route="/about",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column(
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("About", expand=True),
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                        leading=ft.IconButton(
                                            ft.Icons.MENU, on_click=mostrar_cajonNav
                                        ),
                                        automatically_imply_leading=False,
                                    ),
                                    ft.Text("Welcome to About Page"),
                                    ft.Button(
                                        "Go Store",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/store")
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