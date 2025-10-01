from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.separator import MDSeparator
from kivymd.uix.topappbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

class HomeDashboardScreen(MDScreen):
    def __init__(self, **kwargs):
        super(HomeDashboardScreen, self).__init__(**kwargs)
        self.name = 'home_dashboard'

        layout = MDBoxLayout(orientation='vertical')

        # Top App Bar
        self.toolbar = MDTopAppBar(title="Soccer GM")
        layout.add_widget(self.toolbar)

        # Bottom Navigation
        bottom_nav = MDBottomNavigation()

        # --- Dashboard Tab ---
        dashboard_tab = MDBottomNavigationItem(name='dashboard_tab', text='Dashboard', icon='view-dashboard')
        dashboard_tab.add_widget(self.create_dashboard_content())

        # --- Squad Tab ---
        squad_tab = MDBottomNavigationItem(name='squad_tab', text='Squad', icon='account-group')
        squad_tab.add_widget(MDLabel(text="Squad Management (Placeholder)", halign="center"))

        # --- Transfers Tab ---
        transfers_tab = MDBottomNavigationItem(name='transfers_tab', text='Transfers', icon='swap-horizontal')
        transfers_tab.add_widget(MDLabel(text="Transfers (Placeholder)", halign="center"))

        bottom_nav.add_widget(dashboard_tab)
        bottom_nav.add_widget(squad_tab)
        bottom_nav.add_widget(transfers_tab)

        layout.add_widget(bottom_nav)
        self.add_widget(layout)

    def create_dashboard_content(self):
        """Creates the content widget for the dashboard tab."""
        content_layout = MDBoxLayout(orientation='vertical', padding='20dp', spacing='20dp')

        # Info Card
        self.info_card = MDCard(
            orientation='vertical',
            padding="20dp",
            spacing="10dp",
            size_hint=(1, None),
            height="150dp",
            elevation=2,
            pos_hint={'center_x': 0.5}
        )
        self.welcome_label = MDLabel(
            text="Welcome!",
            halign="center",
            font_style="H5"
        )
        self.league_info_label = MDLabel(
            text="", # Will be populated on screen enter
            halign="center",
            font_style="Body1",
            theme_text_color="Secondary"
        )
        self.info_card.add_widget(self.welcome_label)
        self.info_card.add_widget(MDSeparator())
        self.info_card.add_widget(self.league_info_label)

        content_layout.add_widget(self.info_card)
        return content_layout

    def on_enter(self):
        """Called when the screen is entered. Updates the display with game data."""
        app = MDApp.get_running_app()
        if app and app.league:
            league = app.league
            self.toolbar.title = league.name
            self.welcome_label.text = f"Welcome, Manager!"
            self.league_info_label.text = f"You are competing in the '{league.name}'.\n" \
                                          f"There are {len(league.teams)} teams total."
        else:
            self.welcome_label.text = "Error"
            self.league_info_label.text = "No league data found."