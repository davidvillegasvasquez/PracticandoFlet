
import flet as ft
from core.state import AppState as AS
from core.i18n import I18n
from configs.routes import ROUTES

class MainLayout(ft.Column):
    def __init__(self, page, content, router):
        super().__init__(expand=True)
        self._page = page
        self.router = router
        self.content = content

        self._build()

    def _build(self):
        self.controls.clear()

        # TOP BAR
        self.controls.append(self._top_bar())

        self.usuario = ft.Text(AS.usuario)
        self.controls.append(self.usuario)

        self.boton_salir = ft.Button("logout", on_click=self.salir, visible=False)
        self.controls.append(self.boton_salir)

        # CONTENT
        self.controls.append(
            ft.Container(
                content=self.content,
                expand=True,
                padding=0,
            )
        )

        # BOTTOM BAR (mobile / tablet)
        if AS.device != "desktop":
            self.controls.append(self._bottom_bar())

    def salir(self, e):
        AS.usuario = None
        self.boton_salir.visible = False
        self._page.update()

    # ---------- TOP BAR ----------
    def _top_bar(self):
        items = []

        for r in ROUTES:
            if not r.get("show_in_top"):
                continue

            items.append(
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(r["icon"]),
                            ft.Text(
                                I18n.t(r["label"]) if "." in r["label"] else r["label"],
                                size=12,                            
                            ),
                        ],
                        spacing=10,
                    ),
                    on_click=lambda e, p=r["path"]: self.router.navigate(p),
                )
            )

        return ft.AppBar(
            title=ft.Text(I18n.t("app.name")),
            actions=[
                ft.PopupMenuButton(
                    icon=ft.Icons.MENU,
                    items=items,
                )
            ],
        )

    # ---------- BOTTOM BAR ----------
    def _bottom_bar(self):
        destinations = []
        paths = []

        for r in ROUTES:
            if r.get("show_in_bottom"): # and (r.get("label") != "Perfilusuario"):
                destinations.append(
                    ft.NavigationBarDestination(
                        icon=r["icon"],
                        label=I18n.t(r["label"]),
                    )
                )
                paths.append(r["path"])

        def on_change(e):
            self.router.navigate(paths[e.control.selected_index])

        return ft.NavigationBar(
            destinations=destinations,
            selected_index=paths.index(AS.current_route)
            if AS.current_route in paths else 0,
            on_change=on_change,
        )
#MainLayout sin el menú hamburguesa: Para ello reescribimos el atributo método _top_bar. Note como configuramos los constructores para las clases padres:
class MainLayout2(MainLayout):
    def __init__(self, *args, **kwargs):
        # **kwargs catches 'page' and prevents the TypeError
        super().__init__(*args, **kwargs)

    def _top_bar(self):
        return ft.AppBar(
            title=ft.Text(I18n.t("app.name"))
        )
