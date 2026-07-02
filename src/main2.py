#autenStateless2.py
import asyncio
import flet as ft
import httpx
from paquetes.aplicaciones.clasesFlet import DropdownAutorYsusLibros, widget_ejemplo

API_AUTH = "http://localhost:8000/apiauth/auth"

# Estado global del cliente (mejor mantenido en una clase o variable global)
auth_state = {
    "access_token": None,
    "refresh_token": None,
    "expires_at": 0, # Timestamp de expiración
}

async def main(page: ft.Page):
    page.title = "App Stateless con DRF y Flet"
    monitoreo_encendido = True
    # --- 1. Formularios y Pantallas ---
    
    def go_to_login():
        nonlocal monitoreo_encendido
        print(f"Ver monitoreo_encendido desde go_to_login: {monitoreo_encendido}")
        monitoreo_encendido = False
        error_text.value = ""
        page.clean()
        page.add(login_view)

    def go_to_main_app():
        #page.clean()
        #pagina = DropdownAutorYsusLibros(page, auth_state["access_token"])
        #cuadtex = widget_ejemplo(page)
        page.add(
            DropdownAutorYsusLibros(),
            ft.Button("Cerrar Sesión", on_click=lambda e:go_to_login()),
        )
        # Iniciar la tarea en segundo plano para el monitoreo del token
        page.update()
        nonlocal monitoreo_encendido
        monitoreo_encendido = True
        page.run_task(monitor_token_expiry)

    # Vista de Login
    email_field = ft.TextField(label="Email")
    password_field = ft.TextField(label="Contraseña")
    error_text = ft.Text(color=ft.Colors.RED)

    async def handle_login(e):
        # 1. Enviar datos a tu backend con SimpleJWT
        try:
            # Consumo de tu endpoint de DRF
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_AUTH}/login/",
                    json={"email": email_field.value, "password": password_field.value}
                )
            
            if response.status_code == 200:
                data = response.json()
                auth_state["access_token"] = data["access"]
                auth_state["refresh_token"] = data["refresh"]
                # Ajusta esto según el tiempo de vida de tu JWT (ej: 300 segundos)
                #page.shared_preferences.set_async("jwt_access_token", auth_state["access_token"])
                #page.shared_preferences.set_async("jwt_refresh_token", auth_state["refresh_token"])

                auth_state["expires_at"] = asyncio.get_event_loop().time() + 10 
                go_to_main_app()
                page.update()
            else:
                error_text.value = "Credenciales inválidas"
                page.update()
        except Exception as ex:
            error_text.value = f"Error de conexión: {ex}"
            page.update()

    login_view = ft.Column([
        ft.Text("Iniciar Sesión", size=30),
        email_field,
        password_field,
        ft.Button("Entrar", on_click=handle_login),
        error_text
    ], alignment=ft.MainAxisAlignment.CENTER)

    # --- 2. Cuadro Modal de Advertencia ---
    
    async def renew_token(e):
        try:
            # Consumo de tu endpoint de DRF
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_AUTH}/token/refresh/",
                    json={"refresh": auth_state["refresh_token"]}
            )

            if response.status_code == 200:
                data = response.json()
                auth_state["access_token"] = data["access"]
                auth_state["expires_at"] = asyncio.get_event_loop().time() + 10
                page.run_task(monitor_token_expiry)
                page.pop_dialog()
                page.update()
            else:
                # Si el refresh token también expiró, forzar cierre de sesión
                page.pop_dialog()
                go_to_login()
        except Exception:
            page.pop_dialog()
            go_to_login()

    warning_dialog = ft.AlertDialog(
        title=ft.Text("Sesión a punto de expirar"),
        content=ft.Text("Tu sesión caducará en 5 segundos. ¿Deseas prorrogarla por 10 seg más ?"),
        actions=[
            ft.Button("Renovar sesión", on_click=renew_token),
        ],
    )

    # --- 3. Monitoreo Asíncrono del Token ---
    
    async def monitor_token_expiry():  
        warning_dialog_shown = False
        while monitoreo_encendido:
            await asyncio.sleep(1) # Revisa el estado cada 1 segundos
            
            if not auth_state["access_token"]:
                break # Si el usuario cerró sesión, detener monitoreo

            current_time = asyncio.get_event_loop().time()
            time_left = auth_state["expires_at"] - current_time
            
            # Mostrar modal faltando 10 segundos (y si no está ya abierto)
            if time_left <= 5 and not warning_dialog_shown:
                page.show_dialog(warning_dialog)
                page.update()
                warning_dialog_shown = True
            
            # Al expirar el tiempo, retornar al login
            elif time_left <= 0:
                break
                
        page.pop_dialog()
        print(f"Ver monitoreo_encendido desde monitor_token_expiry <= 0: {monitoreo_encendido}")
        go_to_login()
    # Inicializar en pantalla de login
    page.pop_dialog()
    page.update() #
    go_to_login()

ft.run(main)