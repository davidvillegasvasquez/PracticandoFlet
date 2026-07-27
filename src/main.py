#navigationDrawerLogin.py
import asyncio
import flet as ft
from paquetes.aplicaciones.agenda_tareas import TodoApp
from paquetes.aplicaciones.calculadora import AppCalculadora
from paquetes.logicas.apis import SesionJWT
from paquetes.aplicaciones.moduloLeerAutorYsusLibros import ConsultarAutorYsusLibros
from paquetes.aplicaciones.moduloCrearAutorYsusLibros import CrearAutor, CrearLibro
from paquetes.aplicaciones.moduloRetrieveUpdateDestroyLibro import PatchLibro

sesion = None

async def main(pagina: ft.Page):
    pagina.title = "Cajón de navegación"

    async def view_will_mount():
        await fetch_data_and_draw()

    async def manejar_cambio(e):
        if e.control.selected_index == 0:
            await pagina.push_route("/")

        elif e.control.selected_index == 1:
            await pagina.push_route("/todo")

        elif e.control.selected_index == 2:
            await pagina.push_route("/read_crud")

        elif e.control.selected_index == 3:
            await pagina.push_route("/create_crud_autor")

        elif e.control.selected_index == 4:
            await pagina.push_route("/create_crud_libro")

        elif e.control.selected_index == 5:
            await pagina.push_route("/patch_crud_libro")

        elif e.control.selected_index == 6:
            await pagina.push_route("/calculadora")

    def crear_cajonNav(indice_seleccionado=0):
        return ft.NavigationDrawer(
            selected_index=indice_seleccionado,
            on_change=manejar_cambio,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Ingresar",
                    icon=ft.Icons.HOME_OUTLINED, 
                    visible = True, #if auth_state["access_token"] is not None else False,
                    selected_icon=ft.Icon(ft.Icons.HOME),
                    disabled=False if (sesion is None or sesion.tokenAcceso is None) else True
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="To-do",
                    icon=ft.Icon(ft.Icons.STORE_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.STORE),
                    disabled=True if (sesion is None or sesion.tokenAcceso is  None) else False
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Operación read/crud, consultar autor y sus libros",
                    icon=ft.Icon(ft.Icons.STORE_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.STORE),
                    disabled=True if (sesion is None or sesion.tokenAcceso is None) else False
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Operación create/crud, crear autor",
                    icon=ft.Icon(ft.Icons.STORE_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.STORE),
                    disabled=True if (sesion is None or sesion.tokenAcceso is None) else False
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Operación create/crud, crear libro",
                    icon=ft.Icon(ft.Icons.STORE_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.STORE),
                    disabled=True if (sesion is None or sesion.tokenAcceso is None) else False
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Operación patch/crud, modificar(update) libro",
                    icon=ft.Icon(ft.Icons.STORE_OUTLINED),
                    selected_icon=ft.Icon(ft.Icons.STORE),
                    disabled=True if (sesion is None or sesion.tokenAcceso is None) else False
                ),
                ft.Divider(thickness=2),
                ft.NavigationDrawerDestination(
                    label="Calculadora",
                    icon=ft.Icon(ft.Icons.PHONE_OUTLINED),
                    selected_icon=ft.Icons.PHONE,
                    disabled=True if (sesion is None or sesion.tokenAcceso is None) else False
                ),
            ],
        )

    async def mostrar_cajonNav():
        await pagina.show_drawer()

    async def logeo(e):
        global sesion
        error_text.value =""
        sesion = SesionJWT(email.value, password.value, pagina)
        await sesion.handle_login()
        error_text.value = sesion.error_text
        email.value = ""
        password.value = ""
        pagina.update()

    def logout(e):
        #Por definir.
        pass
    
    #Definimos los controles que se usaran a nivel del main para poder funcionar:
    error_text = ft.Text(color=ft.Colors.RED)
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Contraseña")
    botonEnviar = ft.Button("Entrar", on_click=logeo)

    async def cambio_ruta(route):
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
                                                f'usuario:{sesion.usuario}',
                                                visible=True if sesion.tokenAcceso is not None else False
                                            )
                                        ]
                                    ),
                                    TodoApp(),
                                    ft.Button(
                                        "Ir a autor y sus libros",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/read_crud")
                                        ),
                                    ),
                                ]
                            )
                        )
                    ],
                    drawer=crear_cajonNav(indice_seleccionado=1),
                )
            )

        if pagina.route == "/read_crud":
            consultaAutorYsusLibros=ConsultarAutorYsusLibros(pagina, sesion)
            vista=ft.View(
                    route="/create_crud_libro",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column(
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("Operación r/crud read o retrieve autor y sus libros", expand=True),
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                        leading=ft.IconButton(
                                            ft.Icons.MENU, on_click=mostrar_cajonNav
                                        ),
                                        automatically_imply_leading=False,
                                        actions=[
                                            ft.Text(
                                                f'usuario:{sesion.usuario}',
                                                visible=True if sesion.tokenAcceso is not None else False
                                            )
                                        ]
                                    ),
                                    consultaAutorYsusLibros,
                                    ft.Button(
                                        "Ir a crear autor",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/create_crud_autor")
                                            )
                                    ), 
                                    #Botón comodín invisibilizado que simula su pulsación con vista.on_will_mount al cargar esta vista. 
#Todo esto porque las clases python no aceptan contructores asíncronos:                                    
                                    ft.Button(
                                        "Botón comodín",
                                        on_click=await consultaAutorYsusLibros.cargarAutores(),
                                        visible=False
                                    ),                                                                     
                                ]
                            )
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    drawer=crear_cajonNav(indice_seleccionado=2),
                )

            # Asignamos el evento de ciclo de vida de la vista
            vista.on_will_mount = await consultaAutorYsusLibros.laVista_se_montara()
            #Finalmente es que agregamos a la pila de navegación. Todo por la asíncronía que requiere mostrar controles precargados:
            pagina.views.append(vista)
            pagina.update()        

        if pagina.route == "/create_crud_autor":
            pagina.views.append(
                ft.View(
                    route="/create_crud_autor",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column(
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("Operación c/crud crear autor", expand=True),
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                        leading=ft.IconButton(
                                            ft.Icons.MENU, on_click=mostrar_cajonNav
                                        ),
                                        automatically_imply_leading=False,
                                        actions=[
                                            ft.Text(
                                                f'usuario:{sesion.usuario}',
                                                visible=True if sesion.tokenAcceso is not None else False
                                            )
                                        ]
                                    ),
                                    CrearAutor(pagina, sesion),
                                    ft.Button(
                                        "Ir a crear libro",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/create_crud_libro")
                                        ),
                                    ),
                                ]
                            )
                        )
                    ],
                    drawer=crear_cajonNav(indice_seleccionado=3),
                )
            )

        if pagina.route == "/create_crud_libro":
            #Tenemos que crear una instancia de la clase CrearLibro, porque la usaremos diferidamente con su método personalizado, laVista_se_montara(), en el método de ciclo de vida de la vista, vista.on_will_mount:
            libro_nuevo=CrearLibro(pagina, sesion)

            vista=ft.View(
                    route="/create_crud_libro",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column(
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("Operación c/crud crear libro", expand=True),
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                        leading=ft.IconButton(
                                            ft.Icons.MENU, on_click=mostrar_cajonNav
                                        ),
                                        automatically_imply_leading=False,
                                        actions=[
                                            ft.Text(
                                                f'usuario:{sesion.usuario}',
                                                visible=True if sesion.tokenAcceso is not None else False
                                            )
                                        ]
                                    ),
                                    libro_nuevo,
                                    ft.Button(
                                        "Ir a update libro",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/patch_crud_libro")
                                            )
                                    ), 
                                    #Botón comodín invisibilizado que simula su pulsación con vista.on_will_mount al cargar esta vista. 
#Todo esto porque las clases python no aceptan contructores asíncronos:                                    
                                    ft.Button(
                                        "Botón comodín",
                                        on_click=await libro_nuevo.cargarAutoresGenerosYlenguajes(),
                                        visible=False
                                    ),                                                                     
                                ]
                            )
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    drawer=crear_cajonNav(indice_seleccionado=4),
                )

            # Asignamos el evento de ciclo de vida de la vista
            vista.on_will_mount = await libro_nuevo.laVista_se_montara()
            #Finalmente es que agregamos a la pila de navegación. Todo por la asíncronía que requiere mostrar controles precargados:
            pagina.views.append(vista)
            pagina.update()

        if pagina.route == "/patch_crud_libro":
            #Creamos la instancia con identificador porque la utilizaremos posteriormente en vista.on_will_mount:
            libro_actualizado=PatchLibro(pagina, sesion)
            vista=ft.View(
                    route="/patch_crud_libro",
                    controls=[
                        ft.SafeArea(
                            content=ft.Column(
                                controls=[
                                    ft.AppBar(
                                        title=ft.Text("Operación update/crud, en este caso parchear (patch) libro", expand=True),
                                        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                        leading=ft.IconButton(
                                            ft.Icons.MENU, on_click=mostrar_cajonNav
                                        ),
                                        automatically_imply_leading=False,
                                        actions=[
                                            ft.Text(
                                                f'usuario:{sesion.usuario}',
                                                visible=True if sesion.tokenAcceso is not None else False
                                            )
                                        ]
                                    ),
                                    libro_actualizado,
                                    ft.Button(
                                        "Ir a calculadora",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/calculadora")
                                            )
                                    ),                              
                                    ft.Button(
                                        "Botón comodín",
                                        on_click=await libro_actualizado.cargarLibros(),
                                        visible=False
                                    ),                                                                     
                                ]
                            )
                        )
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    drawer=crear_cajonNav(indice_seleccionado=5),
                )

            # Asignamos el evento de ciclo de vida de la vista
            vista.on_will_mount = await libro_actualizado.laVista_se_montara()
            pagina.views.append(vista)
            pagina.update()      
     
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
                                        actions=[
                                            ft.Text(
                                                f'usuario:{sesion.usuario}',
                                                visible=True if sesion.tokenAcceso is not None else False
                                            )
                                        ]
                                    ),
                                    AppCalculadora(),
                                    ft.Button(
                                        "Ir a crear libro",
                                        on_click=lambda _: asyncio.create_task(
                                            pagina.push_route("/create_crud_libro")
                                        ),
                                    ),
                                ]
                            )
                        )
                    ],
                    drawer=crear_cajonNav(indice_seleccionado=6),
                )
            )
        pagina.update()

    async def vista_pop(view):
        pagina.views.pop()
        top_view = pagina.views[-1]
        await pagina.push_route(top_view.route)

    pagina.on_route_change = cambio_ruta
    pagina.on_view_pop = vista_pop
    await cambio_ruta(pagina.route)

if __name__ == "__main__":
    ft.run(main)
