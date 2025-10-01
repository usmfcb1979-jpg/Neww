from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard

class MainMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        self.name = 'main_menu'

        # Main layout container
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing='20dp',
            padding='20dp',
            adaptive_size=True,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )

        # App Title with an icon
        title_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing='10dp', pos_hint={'center_x': 0.5})
        icon = MDIconButton(icon='soccer', theme_icon_color="Custom", icon_color=MDApp.get_running_app().theme_cls.primary_color)
        title = MDLabel(text="Soccer GM", font_style="H2", halign="center", adaptive_height=True)
        title_layout.add_widget(icon)
        title_layout.add_widget(title)

        # Card to hold the menu buttons
        menu_card = MDCard(
            orientation='vertical',
            padding="20dp",
            spacing="10dp",
            size_hint=(1, None),
            height="200dp",
            elevation=2
        )

        new_career_button = MDRaisedButton(
            text="New Career",
            on_press=self.start_new_career,
            size_hint_x=1
        )

        load_game_button = MDRaisedButton(
            text="Load Game",
            on_press=self.load_game,
            size_hint_x=1
        )

        settings_button = MDRaisedButton(
            text="Settings",
            on_press=self.open_settings,
            size_hint_x=1
        )

        menu_card.add_widget(new_career_button)
        menu_card.add_widget(load_game_button)
        menu_card.add_widget(settings_button)

        main_layout.add_widget(title_layout)
        main_layout.add_widget(menu_card)

        self.add_widget(main_layout)

    def start_new_career(self, instance):
        """Calls the main app's method to start a new game."""
        app = MDApp.get_running_app()
        app.start_new_game()

    def load_game(self, instance):
        print("Load Game button pressed.")
        self.manager.current = 'load_game'

    def open_settings(self, instance):
        print("Settings button pressed.")
        self.manager.current = 'settings'