import random

class Contract:
    """Represents a player's contract."""
    def __init__(self, wage, bonuses, length, release_clause=None):
        self.wage = wage
        self.bonuses = bonuses
        self.length = length  # in years
        self.release_clause = release_clause

class Player:
    """Represents a single player with detailed attributes."""
    def __init__(self, name, nationality, age, preferred_foot, positions, contract):
        self.name = name
        self.nationality = nationality
        self.age = age
        self.preferred_foot = preferred_foot
        self.positions = positions  # e.g., ['ST', 'LW']
        self.contract = contract

        # Core Attributes
        self.physical = {
            'pace': random.randint(40, 95), 'acceleration': random.randint(40, 95),
            'stamina': random.randint(40, 95), 'strength': random.randint(40, 95),
            'balance': random.randint(40, 95), 'jumping': random.randint(40, 95),
            'agility': random.randint(40, 95)
        }
        self.technical = {
            'finishing': random.randint(30, 95), 'long_shots': random.randint(30, 95),
            'heading': random.randint(30, 95), 'first_touch': random.randint(30, 95),
            'dribbling': random.randint(30, 95), 'passing': random.randint(30, 95),
            'crossing': random.randint(30, 95), 'technique': random.randint(30, 95),
            'set_pieces': random.randint(30, 95)
        }
        self.tactical = {
            'off_ball': random.randint(30, 95), 'vision': random.randint(30, 95),
            'decision_making': random.randint(30, 95), 'composure': random.randint(30, 95),
            'anticipation': random.randint(30, 95), 'positioning': random.randint(30, 95)
        }
        self.defensive = {
            'tackling': random.randint(30, 95), 'interceptions': random.randint(30, 95),
            'marking': random.randint(30, 95), 'aggression': random.randint(30, 95)
        }
        self.goalkeeping = {
            'shot_stopping': random.randint(20, 95), 'reflexes': random.randint(20, 95),
            'handling': random.randint(20, 95), 'distribution': random.randint(20, 95)
        }

        # Hidden Attributes
        self.hidden = {
            'potential': random.randint(50, 100), 'consistency': random.randint(1, 20),
            'injury_proneness': random.randint(1, 20)
        }

        # Game State
        self.morale = 'Content'
        self.fatigue = 0
        self.sharpness = 100

    def get_overall_rating(self):
        """Calculates a simple overall rating based on primary position."""
        # This is a placeholder; a more sophisticated calculation will be needed
        all_ratings = {**self.physical, **self.technical, **self.tactical, **self.defensive}
        return sum(all_ratings.values()) / len(all_ratings)

    def __repr__(self):
        return f"Player({self.name}, OVR: {self.get_overall_rating():.2f})"

class Tactics:
    """Represents team tactics."""
    def __init__(self):
        self.formation = '4-4-2'
        self.instructions = {
            'pressing_intensity': 'normal',
            'line_height': 'standard',
            'width': 'balanced',
            'tempo': 'normal'
        }

class Team:
    """Represents a soccer team with a roster of players and tactics."""
    def __init__(self, name):
        self.name = name
        self.roster = []
        self.tactics = Tactics()
        self.finances = {
            'transfer_budget': random.randint(1_000_000, 50_000_000),
            'wage_budget': random.randint(200_000, 2_000_000)
        }
        self.facilities = {
            'training': 10, 'youth': 10 # Scale of 1-20
        }

    def add_player(self, player):
        self.roster.append(player)

    def get_team_strength(self):
        """Calculates the team's overall strength from its players."""
        if not self.roster:
            return 0
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
        self.standings[home_team.name]['played'] += 1
        self.standings[away_team.name]['played'] += 1
        self.standings[home_team.name]['gf'] += home_goals
        self.standings[home_team.name]['ga'] += away_goals
        self.standings[away_team.name]['gf'] += away_goals
        self.standings[away_team.name]['ga'] += home_goals
        self.standings[home_team.name]['gd'] = self.standings[home_team.name]['gf'] - self.standings[home_team.name]['ga']
        self.standings[away_team.name]['gd'] = self.standings[away_team.name]['gf'] - self.standings[away_team.name]['ga']
        if home_goals > away_goals:
            self.standings[home_team.name]['wins'] += 1
            self.standings[home_team.name]['points'] += 3
            self.standings[away_team.name]['losses'] += 1
        elif home_goals < away_goals:
            self.standings[away_team.name]['wins'] += 1
            self.standings[away_team.name]['points'] += 3
            self.standings[home_team.name]['losses'] += 1
        else:
            self.standings[home_team.name]['draws'] += 1
            self.standings[away_team.name]['draws'] += 1
            self.standings[home_team.name]['points'] += 1
            self.standings[away_team.name]['points'] += 1

    def __repr__(self):
        return f"League({self.name}, Teams: {len(self.teams)})"