#autenStateless2.py
import asyncio
import flet as ft
import httpx


API_URL = "http://localhost:8000/apiauth/auth"

@ft.control
class Formulario_login(ft.Column):
    monitoreo_encendido: bool = True
    # --- 1. Formularios y Pantallas ---

    def init(self):
    # Vista de Login
        self.email_field = ft.TextField(label="Email")
        self.password_field = ft.TextField(label="Contraseña")
        self.error_text = ft.Text(color=ft.Colors.RED)

        self.controls = [
            self.email_field, 
            self.password_field,
            ft.Button("Entrar", on_click=""), #handle_login),
            self.error_text,
        ]

    """
    async def handle_login(self, e):
        try:
            # Consumo de tu endpoint de DRF
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/login/",
                    json={"email": email_field.value, "password": password_field.value}
                )
            
            if response.status_code == 200:
                data = response.json()
                auth_state["access_token"] = data["access"]
                auth_state["refresh_token"] = data["refresh"]
                # Ajusta esto según el tiempo de vida de tu JWT (ej: 300 segundos)
                auth_state["expires_at"] = asyncio.get_event_loop().time() + 10 
                go_to_main_app()
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
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/token/refresh/",
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
                #page.pop_dialog()
                #print(f"Ver monitoreo_encendido desde elif time_left <= 0: {monitoreo_encendido}")
                #go_to_login()
                #break
        page.pop_dialog()
        print(f"Ver monitoreo_encendido desde monitor_token_expiry <= 0: {monitoreo_encendido}")
        go_to_login()
    # Inicializar en pantalla de login
    page.pop_dialog()
    page.update() #
    go_to_login()

ft.run(main)
    """