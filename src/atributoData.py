#atributoData.py
"""
En Flet , cada componente de la interfaz de usuario (incluido ft.Checkbox) hereda de la clase BaseControl, que cuenta con un data atributo universal diseñado para almacenar datos arbitrarios. Esto resulta increíblemente útil para adjuntar identificadores de base de datos, objetos de modelo o metadatos adicionales directamente a una casilla de verificación, que se pueden recuperar fácilmente dentro de un controlador de eventos cuando el usuario la marca o desmarca.


import flet as ft

def main(page: ft.Page):
    def checkbox_changed(e):
        # Retrieve the extra data assigned to the checkbox
        item_id = e.control.data
        status = "checked" if e.control.value else "unchecked"
        print(f"Item ID {item_id} is now {status}")

    # Pass any data type (int, str, dict, object) into the data attribute
    cb = ft.Checkbox(
        label="Accept Terms", 
        value=False, 
        data=42,  # <-- Storing custom data here
        on_change=checkbox_changed
    )

    page.add(cb)

ft.run(main)

Implementación práctica: Gestión de una lista de tareas pendientes. Al generar listas de forma dinámica (como en los carritos de compra o los sistemas de gestión de tareas), puede utilizar este data atributo para realizar un seguimiento sencillo de qué fila de datos del sistema pertenece a cada casilla de verificación:
"""

import flet as ft

def main(page: ft.Page):
    page.title = "Flet Checkbox Data Attribute Demo"
    
    # Mock data from a database
    tasks_from_db = [
        {"id": 101, "title": "Buy groceries"},
        {"id": 102, "title": "Finish Flet project"},
        {"id": 103, "title": "Call the bank"}
    ]
    
    def on_task_toggle(e):
        # Extract metadata easily via e.control.data
        task_id = e.control.data["db_id"]
        task_title = e.control.data["name"]
        is_checked = e.control.value
        
        status_text.value = f"Task ID {task_id} ('{task_title}') completed status: {is_checked}"
        page.update()

    status_text = ft.Text("Toggle a task to see its attached data.", size=16, color="blue")
    
    # Build checkboxes dynamically using list comprehension
    checkboxes = [
        ft.Checkbox(
            label=task["title"],
            value=False,
            # Attaching a full dictionary to the data attribute
            data={"db_id": task["id"], "name": task["title"]},
            on_change=on_task_toggle
        ) 
        for task in tasks_from_db
    ]
    
    page.add(
        ft.Text("Task List", size=20, weight=ft.FontWeight.BOLD),
        ft.Column(controls=checkboxes),
        ft.Divider(),
        status_text
    )

ft.run(main)
"""
Conclusiones clave
Flexibilidad de datos: Esta data propiedad acepta cualquier objeto de Python, incluidos números enteros, cadenas, tuplas, diccionarios o instancias de clases personalizadas.
Gestión de eventos limpia: en lugar de mantener un mapeador de índices paralelo complejo o analizar la label cadena de la interfaz de usuario, accede directamente a los metadatos e.control.data dentro de sus funciones de eventos.
Estado vs. Datos: No confundir value con data. La value propiedad maneja el estado de verificación booleano ( True, False, o None), mientras que data actúa como un depósito de almacenamiento definido por el desarrollador.
"""