from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

class HomeDashboardScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(HomeDashboardScreen, self).__init__(**kwargs)
        self.app = app
        self.name = 'home_dashboard'

        self.layout = MDBoxLayout(orientation='vertical', padding='20dp', spacing='10dp')
        self.title_label = MDLabel(
            text="Home Dashboard",
            halign="center",
            font_style="H4"
        )
        self.league_info_label = MDLabel(
            text="", # Will be populated on screen enter
            halign="center",
            font_style="Body1"
        )

        self.layout.add_widget(self.title_label)
        self.layout.add_widget(self.league_info_label)
        self.add_widget(self.layout)

    def on_enter(self):
        """Called when the screen is entered. Updates the display with game data."""
        if self.app.league:
            league = self.app.league
            self.league_info_label.text = f"Welcome to the '{league.name}'!\n" \
                                          f"There are {len(league.teams)} teams competing."
        else:
            self.league_info_label.text = "Error: No league data found."