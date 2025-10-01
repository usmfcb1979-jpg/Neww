import random
import math
from models import Player, Team, League, Contract

def create_random_player(position):
    """Factory function to create a random player with detailed attributes."""
    contract = Contract(
        wage=random.randint(500, 50000),
        bonuses={},
        length=random.randint(1, 5)
    )
    return Player(
        name=f"Player {random.randint(100, 999)}",
        nationality="International",
        age=random.randint(18, 34),
        preferred_foot='Right',
        positions=[position],
        contract=contract
    )

def setup_sample_league():
    """Sets up a sample league with teams and players."""
    league = League(name="Sample Premier League")
    team_names = ["Red Lions", "Blue Jays", "Green Giants", "Yellow Hornets"]

    for name in team_names:
        team = Team(name=name)
        for _ in range(16): # 16 players per team
            team.add_player(create_random_player("Midfielder"))
        league.add_team(team)

    return league

def simulate_match(league, home_team, away_team):
    """
    Simulates a single match using a simple, event-driven engine.
    The match is simulated as a series of attacks.
    """
    home_strength = home_team.get_team_strength()
    away_strength = away_team.get_team_strength()

    # Normalize strength to a 0-1 scale for probability calculations
    total_strength = home_strength + away_strength
    home_advantage_prob = home_strength / total_strength

    home_goals = 0
    away_goals = 0

    # Let's model the game as ~150 key attacks/possessions
    num_attacks = 150

    for _ in range(num_attacks):
        # Determine which team is attacking based on their relative strength
        if random.random() < home_advantage_prob:
            attacker = home_team
            defender = away_team
        else:
            attacker = away_team
            defender = home_team

        # --- Simple Event Logic ---
        # Does the attack result in a shot?
        # Let's say a team's chance to turn an attack into a shot is related to its strength.
        # A team with 100 strength has a high chance, a team with 50 has a lower chance.
        # We'll model this as a probability. A 65-strength team might have a ~32.5% chance.
        shot_chance_prob = (attacker.get_team_strength() / 200)

        if random.random() < shot_chance_prob:
            # It's a shot! Is it a goal?
            # This depends on the attacker's finishing vs. the defender's strength.
            # A simple model: goal_prob = attacker_strength / (attacker_strength + defender_strength*2)
            # The *2 gives the defense a slight advantage, making goals rarer.
            goal_prob = attacker.get_team_strength() / (attacker.get_team_strength() + (defender.get_team_strength() * 2))

            if random.random() < goal_prob:
                # Goal scored!
                if attacker == home_team:
                    home_goals += 1
                else:
                    away_goals += 1

    # After all attacks are simulated, update the league standings
    league.update_standings(home_team, away_team, home_goals, away_goals)
    return home_goals, away_goals

def simulate_season(league):
    """Simulates a full season based on the league's schedule."""
    if not league.schedule:
        league.create_schedule()

    for home_team, away_team in league.schedule:
        simulate_match(league, home_team, away_team)

    return league.standings