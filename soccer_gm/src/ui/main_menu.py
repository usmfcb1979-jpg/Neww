from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel

class MainMenuScreen(MDScreen):
    def __init__(self, app, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        self.app = app  # Store a reference to the main app
        self.name = 'main_menu'

        layout = MDBoxLayout(
            orientation='vertical',
            spacing='15dp',
            padding='15dp',
            adaptive_size=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        title = MDLabel(
            text="Soccer GM",
            font_style="H2",
            halign="center",
            size_hint_y=None,
            height=self.height
        )

        new_career_button = MDRaisedButton(
            text="New Career",
            size_hint=(1, None),
            height="48dp",
            on_press=self.start_new_career
        )

        load_game_button = MDRaisedButton(
            text="Load Game",
            size_hint=(1, None),
            height="48dp",
            on_press=self.load_game
        )

        settings_button = MDRaisedButton(
            text="Settings",
            size_hint=(1, None),
            height="48dp",
            on_press=self.open_settings
        )

        layout.add_widget(title)
        layout.add_widget(new_career_button)
        layout.add_widget(load_game_button)
        layout.add_widget(settings_button)

        self.add_widget(layout)

    def start_new_career(self, instance):
        """Calls the main app's method to start a new game."""
        self.app.start_new_game()

    def load_game(self, instance):
        print("Loading a saved game...")
        # Logic to load game will be added here

    def open_settings(self, instance):
        print("Opening settings...")
        # Logic to open settings screen will be added here