import os
import sys
import random
import math
import sqlite3
import json

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.separator import MDSeparator
from kivymd.uix.topappbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.button import MDRaisedButton, MDIconButton

# ==============================================================================
# ===== MODELS (from models.py)
# ==============================================================================

class Contract:
    """Represents a player's contract."""
    def __init__(self, wage, bonuses, length, release_clause=None):
        self.wage = wage
        self.bonuses = bonuses
        self.length = length
        self.release_clause = release_clause

class Player:
    """Represents a single player with detailed attributes."""
    def __init__(self, name, nationality, age, preferred_foot, positions, contract):
        self.name = name
        self.nationality = nationality
        self.age = age
        self.preferred_foot = preferred_foot
        self.positions = positions
        self.contract = contract
        self.physical = {'pace': random.randint(40, 95), 'acceleration': random.randint(40, 95), 'stamina': random.randint(40, 95), 'strength': random.randint(40, 95), 'balance': random.randint(40, 95), 'jumping': random.randint(40, 95), 'agility': random.randint(40, 95)}
        self.technical = {'finishing': random.randint(30, 95), 'long_shots': random.randint(30, 95), 'heading': random.randint(30, 95), 'first_touch': random.randint(30, 95), 'dribbling': random.randint(30, 95), 'passing': random.randint(30, 95), 'crossing': random.randint(30, 95), 'technique': random.randint(30, 95), 'set_pieces': random.randint(30, 95)}
        self.tactical = {'off_ball': random.randint(30, 95), 'vision': random.randint(30, 95), 'decision_making': random.randint(30, 95), 'composure': random.randint(30, 95), 'anticipation': random.randint(30, 95), 'positioning': random.randint(30, 95)}
        self.defensive = {'tackling': random.randint(30, 95), 'interceptions': random.randint(30, 95), 'marking': random.randint(30, 95), 'aggression': random.randint(30, 95)}
        self.goalkeeping = {'shot_stopping': random.randint(20, 95), 'reflexes': random.randint(20, 95), 'handling': random.randint(20, 95), 'distribution': random.randint(20, 95)}
        self.hidden = {'potential': random.randint(50, 100), 'consistency': random.randint(1, 20), 'injury_proneness': random.randint(1, 20)}
        self.morale = 'Content'
        self.fatigue = 0
        self.sharpness = 100

    def get_overall_rating(self):
        all_ratings = {**self.physical, **self.technical, **self.tactical, **self.defensive}
        return sum(all_ratings.values()) / len(all_ratings)

    def __repr__(self):
        return f"Player({self.name}, OVR: {self.get_overall_rating():.2f})"

class Tactics:
    """Represents team tactics."""
    def __init__(self):
        self.formation = '4-4-2'
        self.instructions = {'pressing_intensity': 'normal', 'line_height': 'standard', 'width': 'balanced', 'tempo': 'normal'}

class Team:
    """Represents a soccer team with a roster of players and tactics."""
    def __init__(self, name):
        self.name = name
        self.roster = []
        self.tactics = Tactics()
        self.finances = {'transfer_budget': random.randint(1000000, 50000000), 'wage_budget': random.randint(200000, 2000000)}
        self.facilities = {'training': 10, 'youth': 10}

    def add_player(self, player):
        self.roster.append(player)

    def get_team_strength(self):
        if not self.roster: return 0
        return sum(p.get_overall_rating() for p in self.roster) / len(self.roster)

    def __repr__(self):
        return f"Team({self.name}, Strength: {self.get_team_strength():.2f})"

class League:
    """Manages the league, including teams, schedule, and standings."""
    def __init__(self, name):
        self.name = name
        self.teams = []
        self.schedule = []
        self.standings = {}

    def add_team(self, team):
        self.teams.append(team)
        self.standings[team.name] = {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0, 'gf': 0, 'ga': 0, 'gd': 0, 'points': 0}

    def create_schedule(self):
        self.schedule = []
        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                self.schedule.append((self.teams[i], self.teams[j]))
        random.shuffle(self.schedule)

    def update_standings(self, home_team, away_team, home_goals, away_goals):
        self.standings[home_team.name]['played'] += 1; self.standings[away_team.name]['played'] += 1
        self.standings[home_team.name]['gf'] += home_goals; self.standings[home_team.name]['ga'] += away_goals
        self.standings[away_team.name]['gf'] += away_goals; self.standings[away_team.name]['ga'] += home_goals
        self.standings[home_team.name]['gd'] = self.standings[home_team.name]['gf'] - self.standings[home_team.name]['ga']
        self.standings[away_team.name]['gd'] = self.standings[away_team.name]['gf'] - self.standings[away_team.name]['ga']
        if home_goals > away_goals:
            self.standings[home_team.name]['wins'] += 1; self.standings[home_team.name]['points'] += 3; self.standings[away_team.name]['losses'] += 1
        elif home_goals < away_goals:
            self.standings[away_team.name]['wins'] += 1; self.standings[away_team.name]['points'] += 3; self.standings[home_team.name]['losses'] += 1
        else:
            self.standings[home_team.name]['draws'] += 1; self.standings[away_team.name]['draws'] += 1; self.standings[home_team.name]['points'] += 1; self.standings[away_team.name]['points'] += 1

# ==============================================================================
# ===== DATABASE (from database.py)
# ==============================================================================

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file); return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    try:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, transfer_budget INTEGER, wage_budget INTEGER, training_facilities INTEGER, youth_facilities INTEGER, formation TEXT, instructions TEXT);")
        c.execute("CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY AUTOINCREMENT, team_id INTEGER, name TEXT NOT NULL, nationality TEXT, age INTEGER, preferred_foot TEXT, positions TEXT, morale TEXT, fatigue INTEGER, sharpness INTEGER, physical_attrs TEXT, technical_attrs TEXT, tactical_attrs TEXT, defensive_attrs TEXT, goalkeeping_attrs TEXT, hidden_attrs TEXT, FOREIGN KEY (team_id) REFERENCES teams (id));")
        c.execute("CREATE TABLE IF NOT EXISTS contracts (player_id INTEGER PRIMARY KEY, wage INTEGER, length INTEGER, release_clause INTEGER, bonuses TEXT, FOREIGN KEY (player_id) REFERENCES players (id));")
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def save_league(conn, league):
    c = conn.cursor()
    c.execute("DELETE FROM contracts;"); c.execute("DELETE FROM players;"); c.execute("DELETE FROM teams;")
    for team in league.teams:
        c.execute("INSERT INTO teams (name, transfer_budget, wage_budget, training_facilities, youth_facilities, formation, instructions) VALUES (?, ?, ?, ?, ?, ?, ?)", (team.name, team.finances['transfer_budget'], team.finances['wage_budget'], team.facilities['training'], team.facilities['youth'], team.tactics.formation, json.dumps(team.tactics.instructions)))
        team_id = c.lastrowid
        for player in team.roster:
            c.execute("INSERT INTO players (team_id, name, nationality, age, preferred_foot, positions, morale, fatigue, sharpness, physical_attrs, technical_attrs, tactical_attrs, defensive_attrs, goalkeeping_attrs, hidden_attrs) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (team_id, player.name, player.nationality, player.age, player.preferred_foot, json.dumps(player.positions), player.morale, player.fatigue, player.sharpness, json.dumps(player.physical), json.dumps(player.technical), json.dumps(player.tactical), json.dumps(player.defensive), json.dumps(player.goalkeeping), json.dumps(player.hidden)))
            player_id = c.lastrowid
            c.execute("INSERT INTO contracts (player_id, wage, length, release_clause, bonuses) VALUES (?, ?, ?, ?, ?)", (player_id, player.contract.wage, player.contract.length, player.contract.release_clause, json.dumps(player.contract.bonuses)))
    conn.commit()

# ==============================================================================
# ===== SIMULATION (from simulation.py)
# ==============================================================================

def create_random_player(position):
    contract = Contract(wage=random.randint(500, 50000), bonuses={}, length=random.randint(1, 5))
    return Player(name=f"Player {random.randint(100, 999)}", nationality="International", age=random.randint(18, 34), preferred_foot='Right', positions=[position], contract=contract)

def setup_sample_league():
    league = League(name="Sample Premier League")
    team_names = ["Red Lions", "Blue Jays", "Green Giants", "Yellow Hornets"]
    for name in team_names:
        team = Team(name=name)
        for _ in range(16):
            team.add_player(create_random_player("Midfielder"))
        league.add_team(team)
    return league

# ==============================================================================
# ===== UI SCREENS (from ui files)
# ==============================================================================

class LoadGameScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoadGameScreen, self).__init__(**kwargs)
        self.name = 'load_game'
        self.add_widget(MDLabel(text="Load Game (Placeholder)", halign="center", font_style="H4"))

class SettingsScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.name = 'settings'
        self.add_widget(MDLabel(text="Settings (Placeholder)", halign="center", font_style="H4"))

class MainMenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        self.name = 'main_menu'
        main_layout = MDBoxLayout(orientation='vertical', spacing='20dp', padding='20dp', adaptive_size=True, pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing='10dp', pos_hint={'center_x': 0.5})
        icon = MDIconButton(icon='soccer', theme_icon_color="Custom")
        title = MDLabel(text="Soccer GM", font_style="H2", halign="center", adaptive_height=True)
        title_layout.add_widget(icon); title_layout.add_widget(title)
        menu_card = MDCard(orientation='vertical', padding="20dp", spacing="10dp", size_hint=(1, None), height="200dp", elevation=2)
        new_career_button = MDRaisedButton(text="New Career", on_press=self.start_new_career, size_hint_x=1)
        load_game_button = MDRaisedButton(text="Load Game", on_press=self.load_game, size_hint_x=1)
        settings_button = MDRaisedButton(text="Settings", on_press=self.open_settings, size_hint_x=1)
        menu_card.add_widget(new_career_button); menu_card.add_widget(load_game_button); menu_card.add_widget(settings_button)
        main_layout.add_widget(title_layout); main_layout.add_widget(menu_card)
        self.add_widget(main_layout)

    def start_new_career(self, instance):
        MDApp.get_running_app().start_new_game()
    def load_game(self, instance):
        self.manager.current = 'load_game'
    def open_settings(self, instance):
        self.manager.current = 'settings'

class HomeDashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super(HomeDashboardScreen, self).__init__(**kwargs)
        self.name = 'home_dashboard'
        layout = MDBoxLayout(orientation='vertical')
        self.toolbar = MDTopAppBar(title="Soccer GM")
        layout.add_widget(self.toolbar)
        bottom_nav = MDBottomNavigation()
        dashboard_tab = MDBottomNavigationItem(name='dashboard_tab', text='Dashboard', icon='view-dashboard')
        dashboard_tab.add_widget(self.create_dashboard_content())
        squad_tab = MDBottomNavigationItem(name='squad_tab', text='Squad', icon='account-group')
        squad_tab.add_widget(MDLabel(text="Squad Management (Placeholder)", halign="center"))
        transfers_tab = MDBottomNavigationItem(name='transfers_tab', text='Transfers', icon='swap-horizontal')
        transfers_tab.add_widget(MDLabel(text="Transfers (Placeholder)", halign="center"))
        bottom_nav.add_widget(dashboard_tab); bottom_nav.add_widget(squad_tab); bottom_nav.add_widget(transfers_tab)
        layout.add_widget(bottom_nav)
        self.add_widget(layout)

    def create_dashboard_content(self):
        content_layout = MDBoxLayout(orientation='vertical', padding='20dp', spacing='20dp')
        self.info_card = MDCard(orientation='vertical', padding="20dp", spacing="10dp", size_hint=(1, None), height="150dp", elevation=2, pos_hint={'center_x': 0.5})
        self.welcome_label = MDLabel(text="Welcome!", halign="center", font_style="H5")
        self.league_info_label = MDLabel(text="", halign="center", font_style="Body1", theme_text_color="Secondary")
        self.info_card.add_widget(self.welcome_label); self.info_card.add_widget(MDSeparator()); self.info_card.add_widget(self.league_info_label)
        content_layout.add_widget(self.info_card)
        return content_layout

    def on_enter(self):
        app = MDApp.get_running_app()
        if app and app.league:
            league = app.league
            self.toolbar.title = league.name; self.welcome_label.text = f"Welcome, Manager!"
            self.league_info_label.text = f"You are competing in the '{league.name}'.\nThere are {len(league.teams)} teams total."
        else:
            self.welcome_label.text = "Error"; self.league_info_label.text = "No league data found."

# ==============================================================================
# ===== MAIN APP (from main.py)
# ==============================================================================

class SoccerGMApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db_conn = None
        self.league = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Dark"
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(MainMenuScreen(name='main_menu'))
        self.screen_manager.add_widget(HomeDashboardScreen(name='home_dashboard'))
        self.screen_manager.add_widget(LoadGameScreen(name='load_game'))
        self.screen_manager.add_widget(SettingsScreen(name='settings'))
        self.screen_manager.current = 'main_menu'
        return self.screen_manager

    def on_start(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        db_file = os.path.join(data_dir, 'soccer_gm.db')
        self.db_conn = create_connection(db_file)
        if self.db_conn:
            create_tables(self.db_conn)
        else:
            print("Error! Cannot create the database connection.")

    def start_new_game(self):
        if not self.db_conn: return
        self.league = setup_sample_league()
        save_league(self.db_conn, self.league)
        self.screen_manager.current = 'home_dashboard'

    def on_stop(self):
        if self.db_conn:
            self.db_conn.close()

if __name__ == "__main__":
    SoccerGMApp().run()