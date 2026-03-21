import flet as flt

def myapp(page: flt.Page):
    page.theme_mode = flt.ThemeMode.LIGHT
    page.window_height = 400
    page.window_width = 500

    text = flt.TextField(
        label="Introductory Text",
        value="This App is made using Flet"
    )

    page.add(text)
    page.title = 'GeeksApp using Flet'
    page.update()

flt.run(myapp)