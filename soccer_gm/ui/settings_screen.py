from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.name = 'settings'

        label = MDLabel(
            text="Settings (Placeholder)",
            halign="center",
            font_style="H4"
        )
        self.add_widget(label)