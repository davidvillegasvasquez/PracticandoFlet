import flet as ft

@ft.control
class DataTable1(ft.DataTable):
    def __init__(self, columns=None, rows=None, **kwargs):
        super().__init__(
            columns=[
                ft.DataColumn(label=ft.Text("ID"), on_sort=self.handle_column_sort),
                ft.DataColumn(label=ft.Text("TITULO")),
                ft.DataColumn(label=ft.Text("ISBN")),
                ft.DataColumn(label=ft.Text("URL")),
            ],
            #rows=[],
            **kwargs,
            width=300,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=7,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.OUTLINE_VARIANT),
            sort_column_index=0,
            sort_ascending=True,
            heading_row_color=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            heading_row_height=30,
            data_row_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(0.08, ft.Colors.PRIMARY),
                ft.ControlState.SELECTED: ft.Colors.with_opacity(0.14, ft.Colors.PRIMARY),
            },
            show_checkbox_column=True,
            #on_select_all=self.handle_select_all,
            divider_thickness=1,
            column_spacing=80
        )

        self.rows = []
        self.displayed_items = []

        self.selected_item_ids: set[int] = {1, 3, 5}

        self.sort_key_for_column = {
            0: lambda item: item["id"],
            1: lambda item: item["titulo"].lower(),
            #2: lambda item: item["isbn"],
            #3: lambda item: item["url"],
        }
  
    def hacerRegistrosApartirDe(self, items: list[dict[str, int | str]]) -> list[ft.DataRow]:
        self.displayed_items = list(items)
        self.rows = [
                ft.DataRow(
                    selected=item["id"] in self.selected_item_ids,
                    on_select_change=self.handle_row_selection_change,
                    data=item["id"],
                    cells=[
                        ft.DataCell(ft.Text(item["id"])),
                        ft.DataCell(ft.Text(item["titulo"])),
                        ft.DataCell(ft.Text(item["isbn"])),
                        ft.DataCell(ft.Text(item["url"])),
                    ],
                )
                for item in items
        ]    

    def handle_row_selection_change(self, e: ft.Event[ft.DataRow]) -> None:
        row = e.control
        item_id = row.data
        is_selected = e.data

        if is_selected:
            self.selected_item_ids.add(item_id)
        else:
            self.selected_item_ids.discard(item_id)

        row.selected = is_selected
        row.update()

    def handle_column_sort(self, e: ft.DataColumnSortEvent) -> None:
        self.displayed_items.sort(
            key=self.sort_key_for_column[e.column_index],
            reverse=not e.ascending,
        )

        self.sort_column_index = e.column_index
        self.sort_ascending = e.ascending
        self.refresh_table_rows()

    def refresh_table_rows(self) -> None:
        self.rows = self.hacerRegistrosApartirDe(self.displayed_items)
        print(f'self.rows = {self.rows}') #Retorna None. Averiguar por qué.
        self.update()
