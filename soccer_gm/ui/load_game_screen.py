from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

class LoadGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoadGameScreen, self).__init__(**kwargs)
        self.name = 'load_game'

        label = MDLabel(
            text="Load Game (Placeholder)",
            halign="center",
            font_style="H4"
        )
        self.add_widget(label)