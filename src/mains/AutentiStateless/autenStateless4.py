#autenStateless4.py
import flet as ft
import requests

API_AUTH = "http://localhost:8000/apiauth/auth"

async def main(page: ft.Page):
    page.title = "Login con JWT"
    
    # Controladores para los campos de texto
    username_field = ft.TextField(label="Usuario", width=300)
    password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300)
    error_text = ft.Text(value="", color="red")
    
    async def handle_login(e):
        # 1. Instancia el servicio de preferencias
        prefs = ft.SharedPreferences()
        # 2. Enviar datos a tu backend con SimpleJWT
        login_url = f"{API_AUTH}/login/" # Cambia esto por tu URL
        payload = {
            "email": username_field.value,
            "password": password_field.value
        }
        
        try:
            response = requests.post(login_url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                access_token = data.get("access")
                refresh_token = data.get("refresh")
                
                # 2. Guardar el token de forma segura
                await prefs.set("jwt_access_token", access_token)
                await prefs.set("jwt_refresh_token", refresh_token)
                
                error_text.value = "¡Inicio de sesión exitoso!"
                error_text.color = "green"
                
                # Redirigir a la vista principal o actualizar la app
                # page.go("/dashboard")
                
            else:
                error_text.value = "Usuario o contraseña incorrectos."
                error_text.color = "red"
        except Exception as err:
            error_text.value = f"Error de conexión: {err}"
            error_text.color = "red"
        
        page.update()

    # Vista del login
    page.add(
        ft.Column(
            [
                ft.Text("Iniciar Sesión", size=30, weight=ft.FontWeight.BOLD),
                username_field,
                password_field,
                ft.Button("Entrar", on_click=handle_login),
                error_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

ft.run(main)