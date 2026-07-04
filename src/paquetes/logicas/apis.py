#autenStateless1.py
import asyncio
import flet as ft
import httpx

API_URL = "http://localhost:8000/apiauth/auth"

class SesionJWT():
    """
    Lleva la administración de una sesión sin estado que consume una api de autenticación propia basada en simple jwt.
    """
    def __init__(self, usuario, password, pag):
        self.usuario = usuario
        self.password = password
        self.pagina = pag
        self.tokenAcceso = None
        self.tokenRefres = None
        self.monitoreo_encendido = False
        self.error_text = None 
        self.expira_a = 0
        self.warning_dialog = ft.AlertDialog(
            title=ft.Text("Sesión a punto de expirar"),
            content=ft.Text("Tu sesión caducará en 5 segundos. ¿Deseas prorrogarla por 10 seg más ?"),
            actions=[
                ft.Button("Renovar sesión", on_click=self.renew_token),
            ],
        )

    async def handle_login(self):
        try:
            # Consumo de tu endpoint de DRF
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/login/",
                    json={"email": self.usuario, "password": self.password}
                )
            
            if response.status_code == 200:
                data = response.json()
                self.tokenAcceso = data["access"]
                self.tokenRefres = data["refresh"]
                self.monitoreo_encendido = True
                # Ajusta esto según el tiempo de vida de tu JWT (ej: 300 segundos)
                self.expira_a = asyncio.get_event_loop().time() + 10 
                self.pagina.push_route("/todo")
            else:
                self.error_text = "Credenciales inválidas"
                self.pagina.update()
        except Exception as ex:
            self.error_text = f"Error de conexión: {ex}"
            self.pagina.update()

    # --- 2. Cuadro Modal de Advertencia ---
    
    async def renew_token(self, e):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{API_URL}/token/refresh/",
                    json={"refresh": self.tokenRefres}
                )
            if response.status_code == 200:
                data = response.json()
                self.tokenAcceso = data["access"]
                self.expira_a = asyncio.get_event_loop().time() + 10
                self.pagina.run_task(self.monitor_token_expiry)
                self.pagina.pop_dialog()
                self.pagina.update()
            else:
                # Si el refresh token también expiró, forzar cierre de sesión
                self.pagina.pop_dialog()
                self.pagina.push_route("/")
        except Exception:
            self.pagina.pop_dialog()
            self.pagina.push_route("/")

    # --- 3. Monitoreo Asíncrono del Token ---
    
    async def monitor_token_expiry(self):  
        warning_dialog_shown = False
        while self.monitoreo_encendido:
            await asyncio.sleep(1) # Revisa el estado cada 1 segundos
            
            if not self.tokenAcceso:
                break # Si el usuario cerró sesión, detener monitoreo

            current_time = asyncio.get_event_loop().time()
            time_left = self.expira_a - current_time
            
            # Mostrar modal faltando 10 segundos (y si no está ya abierto)
            if time_left <= 5 and not warning_dialog_shown:
                self.pagina.show_dialog(self.warning_dialog)
                self.pagina.update()
                warning_dialog_shown = True
            
            # Al expirar el tiempo, retornar al login
            elif time_left <= 0:
                break
                
        self.pagina.pop_dialog()
        self.pagina.update()
        self.pagina.push_route("/")
