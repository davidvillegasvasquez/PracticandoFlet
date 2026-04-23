import flet as ft

@ft.control
class DataTable1(ft.DataTable):
    def __init__(self, columns=None, rows=None, **kwargs):
        super().__init__(
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("TITULO")),
                ft.DataColumn(label=ft.Text("ISBN")),
                ft.DataColumn(label=ft.Text("URL")),
            ],
            rows=[],
            **kwargs
        )

        self.border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT)
  
    def hacerRegistrosApartirDe(self, items: list[dict[str, int | str]]) -> list[ft.DataRow]:
        self.rows = [
                ft.DataRow(
                    #selected=item["id"] in selected_item_ids,
                    #on_select_change=handle_row_selection_change,
                    #data=item["id"],
                    cells=[
                        ft.DataCell(ft.Text(item["id"])),
                        ft.DataCell(ft.Text(item["titulo"])),
                        ft.DataCell(ft.Text(item["isbn"])),
                        ft.DataCell(ft.Text(item["url"])),
                    ],
                )
                for item in items
        ]    
#---------------------------------------------------------  

@ft.control
class DataTable2(ft.DataTable):
    def init(self):
        self.inventory_items = None
        self.displayed_items = list(inventory_items)
        self.selected_item_ids: set[int] = {1, 3, 5}

        self.sort_key_for_column = {
            0: lambda item: item["id"],
            1: lambda item: item["titulo"].lower(),
            2: lambda item: item["isbn"],
        }

    def build_rows(self, items: list[dict[str, int | str]]) -> list[ft.DataRow]:
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

    def refresh_table_rows(self) -> None:
        table.rows = build_rows(displayed_items)
        table.update()

    def handle_row_selection_change(self, e: ft.Event[ft.DataRow]) -> None:
        row = e.control
        item_id = row.data
        is_selected = e.data

        if is_selected:
            selected_item_ids.add(item_id)
        else:
            selected_item_ids.discard(item_id)

        row.selected = is_selected
        row.update()

    def handle_select_all(self, e: ft.Event[ft.DataTable]) -> None:
        if e.data:
            selected_item_ids.update(item["id"] for item in displayed_items)
        else:
            selected_item_ids.clear()

        refresh_table_rows()

    def handle_column_sort(self, e: ft.DataColumnSortEvent) -> None:
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
