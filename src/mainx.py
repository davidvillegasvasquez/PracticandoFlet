#datatable1.py
import flet as ft

def main(page: ft.Page):
    inventory_items = [{'url': 'http://127.0.0.1:8000/catalogo/api-todosLoslibros/4/', 'id': 4, 'titulo': 'Canaima', 'autor': 'http://127.0.0.1:8000/catalogo/api-todosLosAutores/2/', 'descripcion': 'En esta obra, la selva del Orinoco es el gran personaje y el motivo que impulsa todas las acciones de sus personajes. La lucha despiadada contra la naturaleza, el terror del caciquismo y el ansia de riquezas, dominio y poder, constituyen el tema principal de esta novela.', 'isbn': '5556322856771'}, {'url': 'http://127.0.0.1:8000/catalogo/api-todosLoslibros/3/', 'id': 3, 'titulo': 'Doña Barbara', 'autor': 'http://127.0.0.1:8000/catalogo/api-todosLosAutores/2/', 'descripcion': 'Doña Bárbara es la novela venezolana más popular: desde su aparición, en 1929, se leyó con avidez quizás porque entre líneas Gallegos expresaba su rebeldía al régimen dictatorial de Juan Vicente Gómez y al atraso que vivía el país. La novela examina el tópico sociológico, de raíz positivista, civilización frente a barbarie en la vida venezolana rural. Entre otros méritos, se destaca la maestría del escritor en cuanto a la creación de personajes, así como también la descripción del paisaje llanero.', 'isbn': '4077862365395'}]

    displayed_items = list(inventory_items)
    selected_item_ids: set[int] = {1, 3, 5}

    sort_key_for_column = {
        0: lambda item: item["id"],
        1: lambda item: item["titulo"].lower(),
        2: lambda item: item["isbn"],
    }

    def build_rows(items: list[dict[str, int | str]]) -> list[ft.DataRow]:
        return [
            ft.DataRow(
                selected=item["id"] in selected_item_ids,
                on_select_change=handle_row_selection_change,
                data=item["id"],
                cells=[
                    ft.DataCell(ft.Text(int(item["id"]))),
                    ft.DataCell(ft.Text(item["titulo"])),
                    ft.DataCell(ft.Text(item["isbn"])),
                ],
            )
            for item in items
        ]

    def refresh_table_rows() -> None:
        table.rows = build_rows(displayed_items)
        table.update()

    def handle_row_selection_change(e: ft.Event[ft.DataRow]) -> None:
        row = e.control
        item_id = row.data
        is_selected = e.data

        if is_selected:
            selected_item_ids.add(item_id)
        else:
            selected_item_ids.discard(item_id)

        row.selected = is_selected
        row.update()

    def handle_select_all(e: ft.Event[ft.DataTable]) -> None:
        if e.data:
            selected_item_ids.update(item["id"] for item in displayed_items)
        else:
            selected_item_ids.clear()

        refresh_table_rows()

    def handle_column_sort(e: ft.DataColumnSortEvent) -> None:
        displayed_items.sort(
            key=sort_key_for_column[e.column_index],
            reverse=not e.ascending,
        )

        table.sort_column_index = e.column_index
        table.sort_ascending = e.ascending
        refresh_table_rows()

    table = ft.DataTable(
        width=700,
        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
        horizontal_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
        sort_column_index=0,
        sort_ascending=True,
        heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        heading_row_height=70,
        data_row_color={
            ft.ControlState.HOVERED: ft.Colors.with_opacity(0.08, ft.Colors.PRIMARY),
            ft.ControlState.SELECTED: ft.Colors.with_opacity(0.14, ft.Colors.PRIMARY),
        },
        show_checkbox_column=True,
        on_select_all=handle_select_all,
        divider_thickness=1,
        column_spacing=50,
        columns=[
            ft.DataColumn(
                label=ft.Text("ID"),
                on_sort=handle_column_sort,
            ),
            ft.DataColumn(
                label=ft.Text("TÍTULO"),
                on_sort=handle_column_sort,
            ),
            ft.DataColumn(
                label=ft.Text("ISBN"),
                tooltip="Numeric quantity",
                numeric=True,
                on_sort=handle_column_sort,
            ),
        ],
        rows=build_rows(displayed_items),
    )

    page.add(
        ft.SafeArea(
            content=table,
        )
    )


if __name__ == "__main__":
    ft.run(main)