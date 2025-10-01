from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

class SquadPageScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SquadPageScreen, self).__init__(**kwargs)
        self.name = 'squad_page'

        label = MDLabel(
            text="Squad Page",
            halign="center",
            font_style="H4"
        )
        self.add_widget(label)