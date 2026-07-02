#AppBar.py
import flet as f
from paquetes.controles.barras.barras import BarraAppBar, BarraBottomAppBar
from paquetes.controles.botones.botones import BotonPersonalizado

def principal(pagina: f.Page):
    pagina.tittle="Atributos de Page"

    def imprimirEnConsola(evento):
        print(f'pagina.client_ip = {pagina.client_ip}')
        print(f'pagina.client_user_agent = {pagina.client_user_agent}')
        print(f'pagina.platform = {pagina.platform}')
        print(f'pagina.platform_brightness = {pagina.platform_brightness}')
        print(f'pagina.route = {pagina.route}')
        print('================================')

    def toggleVisibleUser(evento):
        try:
            user = pagina.appbar.actions[2]
            if user.visible:
                user.visible = False
            else:
                user.visible = True
        except:
            pass

    def eliminarUser(evento):
        pagina.appbar.actions.pop(2)

    def agregarUser(evento):
        pagina.appbar.actions.append(f.Text("david"))
        
      
    boton1=BotonPersonalizado(
        texto="click aquí",
        icono=None,
        funcionPasada=imprimirEnConsola
    )

    boton2=BotonPersonalizado(
        texto="toggleVisibleUser",
        icono=None,
        funcionPasada=toggleVisibleUser
    )

    boton3=BotonPersonalizado(
        texto="eliminarUser",
        icono=None,
        funcionPasada = lambda xcosa: pagina.appbar.actions.pop(2) if (len(pagina.appbar.actions)  >= 3) else ""
    )

    boton4=BotonPersonalizado(
        texto="agregarUser",
        icono=None,
        funcionPasada = lambda sky: pagina.appbar.actions.append(f.Text("david"))
    )
    
    #Así implementamos una barra personalizada importada desde paquetes para asignarlos a los atributos de la página en este caso. Recuerde que esos controles personalizados no pueden ser controles básicos, sino personalizados en forma de una clase:

    pagina.appbar = BarraAppBar("App de comer Mocos")
    pagina.bottom_appbar = BarraBottomAppBar()
    pagina.adaptive = True
    pagina.add(boton1, boton2, boton3, boton4)
    pagina.update()
    
f.run(principal)