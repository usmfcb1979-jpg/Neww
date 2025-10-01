import os
import sys
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

# Backend Imports
from models import League
from database import create_connection, create_tables, save_league, load_league
from simulation import setup_sample_league

# UI Imports
from ui.main_menu import MainMenuScreen
from ui.home_dashboard import HomeDashboardScreen
from ui.load_game_screen import LoadGameScreen
from ui.settings_screen import SettingsScreen

class SoccerGMApp(MDApp):
    """Main application class for Soccer GM."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_conn = None
        self.league = None

    def build(self):
        """Builds the KivyMD application UI."""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"

        self.screen_manager = ScreenManager()

        # Add all the screens
        self.screen_manager.add_widget(MainMenuScreen(name='main_menu'))
        self.screen_manager.add_widget(HomeDashboardScreen(name='home_dashboard'))
        self.screen_manager.add_widget(LoadGameScreen(name='load_game'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))

        self.screen_manager.current = 'main_menu'
        return self.screen_manager

    def on_start(self):
        """Lifecycle method that is called when the app starts."""
        # --- Database Setup ---
        # With the new flat structure, the path is simpler.
        script_dir = os.path.dirname(os.path.abspath(__file__))
        db_file = os.path.join(script_dir, 'data', 'soccer_gm.db')

        self.db_conn = create_connection(db_file)
        if self.db_conn:
            create_tables(self.db_conn)
        else:
            print("Error! Cannot create the database connection.")

    def start_new_game(self):
        """Creates a new game, saves it, and transitions to the dashboard."""
        print("Starting new game...")
        if not self.db_conn:
            print("Database connection not available.")
            return

        # 1. Create a new league using the backend logic
        self.league = setup_sample_league()
        print(f"League '{self.league.name}' created with {len(self.league.teams)} teams.")

        # 2. Save the new league to the database
        save_league(self.db_conn, self.league)
        print("New league saved to database.")

        # 3. Transition to the home dashboard
        self.screen_manager.current = 'home_dashboard'

    def on_stop(self):
        """Lifecycle method that is called when the app is closed."""
        if self.db_conn:
            self.db_conn.close()

if __name__ == "__main__":
    SoccerGMApp().run()