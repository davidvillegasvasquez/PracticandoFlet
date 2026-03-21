from paquetes.controles.botones import * #CalcButton, DigitButton, ActionButton, ExtraActionButton
import flet as f

@f.control
class AppCalculadora(f.Container):
    def init(self):
        self.width = 350
        self.bgcolor = f.Colors.BLACK
        self.border_radius = f.BorderRadius.all(20)
        self.padding = 20
        self.result = f.Text(value="0", color=f.Colors.WHITE, size=20)
        self.content = f.Column(
            controls=[
                f.Row(
                    controls=[self.result],
                    alignment=f.MainAxisAlignment.END,
                ),
                f.Row(
                    controls=[
                        ExtraActionButton(content="AC"),
                        ExtraActionButton(content="+/-"),
                        ExtraActionButton(content="%"),
                        ActionButton(content="/"),
                    ]
                ),
                f.Row(
                    controls=[
                        DigitButton(content="7"),
                        DigitButton(content="8"),
                        DigitButton(content="9"),
                        ActionButton(content="*"),
                    ]
                ),
                f.Row(
                    controls=[
                        DigitButton(content="4"),
                        DigitButton(content="5"),
                        DigitButton(content="6"),
                        ActionButton(content="-"),
                    ]
                ),
                f.Row(
                    controls=[
                        DigitButton(content="1"),
                        DigitButton(content="2"),
                        DigitButton(content="3"),
                        ActionButton(content="+"),
                    ]
                ),
                f.Row(
                    controls=[
                        DigitButton(content="0", expand=2),
                        DigitButton(content="."),
                        ActionButton(content="="),
                    ]
                ),
            ]
        )
