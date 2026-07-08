import flet as ft
import asyncio
import httpx

url_api = "http://127.0.0.1:8000/catalogo/apirest/autores/"

class CrearAutor(ft.Column):
    def __init__(self, pagina, sesion):
        super().__init__()
        self.pag = pagina
        self.sesion = sesion
    
    def build(self):
        self.nombre_input = ft.TextField(label="Nombre")
        self.apellido_input = ft.TextField(label="Apellido")
        self.nacimiento_input = ft.TextField(label="Nacimiento")
        self.muerte_input = ft.TextField(label="Muerte")
        self.btn_crear = ft.Button("Crear", on_click=self.botonCrearAutor)
        self.resultado_texto = ft.Text()

        self.controls = [
            self.nombre_input,
            self.apellido_input,
            self.nacimiento_input,
            self.muerte_input,
            ft.Button("Crear", on_click=self.botonCrearAutor),
            self.resultado_texto
        ]

    async def botonCrearAutor(self, e):
        self.resultado_texto.value = "Enviando datos..."
        self.pag.update()
        
        datos = {
            "nombre": self.nombre_input.value,
            "apellido": self.apellido_input.value,
            "nacimiento": self.nacimiento_input.value,
            "muerte": self.muerte_input.value
        }
"""
        try:
            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {self.sesion.tokenAcceso}"}) as client:
                response = await client.post(API_URL, json=datos, timeout=10.0)
                
                if response.status_code == 201:
                    resultado_texto.value = "¡Instancia creada exitosamente en Django!"
                    resultado_texto.color = "green"
                else:
                    resultado_texto.value = f"Error {response.status_code}: {response.text}"
                    resultado_texto.color = "red" 

        except Exception as error:
            self.pag.show_dialog(ft.AlertDialog(
                title=ft.Text("Ocurrió un error..."),
                content=ft.Text(f'Error: {error}'),
                actions=[ft.TextButton("Cerrar", on_click=lambda e: self.pag.pop_dialog())],
                modal=True
            ))

        else: 
            pass
"""