import sqlite3
import json
import os
from models import League, Team, Player, Contract, Tactics

def create_connection(db_file):
    """Create a database connection to the SQLite database."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_tables(conn):
    """Create the necessary tables for the game state."""
    try:
        c = conn.cursor()
        # Team Table
        c.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                transfer_budget INTEGER,
                wage_budget INTEGER,
                training_facilities INTEGER,
                youth_facilities INTEGER,
                formation TEXT,
                instructions TEXT
            );
        """)
        # Player Table
        c.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER,
                name TEXT NOT NULL,
                nationality TEXT,
                age INTEGER,
                preferred_foot TEXT,
                positions TEXT,
                morale TEXT,
                fatigue INTEGER,
                sharpness INTEGER,
                physical_attrs TEXT,
                technical_attrs TEXT,
                tactical_attrs TEXT,
                defensive_attrs TEXT,
                goalkeeping_attrs TEXT,
                hidden_attrs TEXT,
                FOREIGN KEY (team_id) REFERENCES teams (id)
            );
        """)
        # Contract Table
        c.execute("""
            CREATE TABLE IF NOT EXISTS contracts (
                player_id INTEGER PRIMARY KEY,
                wage INTEGER,
                length INTEGER,
                release_clause INTEGER,
                bonuses TEXT,
                FOREIGN KEY (player_id) REFERENCES players (id)
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def save_league(conn, league):
    """Saves the entire league state to the database."""
    c = conn.cursor()
    # Clear existing data to prevent duplicates on re-save
    c.execute("DELETE FROM contracts;")
    c.execute("DELETE FROM players;")
    c.execute("DELETE FROM teams;")

    for team in league.teams:
        # Save team
        c.execute("""
            INSERT INTO teams (name, transfer_budget, wage_budget, training_facilities, youth_facilities, formation, instructions)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            team.name, team.finances['transfer_budget'], team.finances['wage_budget'],
            team.facilities['training'], team.facilities['youth'], team.tactics.formation,
            json.dumps(team.tactics.instructions)
        ))
        team_id = c.lastrowid

        for player in team.roster:
            # Save player
            c.execute("""
                INSERT INTO players (team_id, name, nationality, age, preferred_foot, positions, morale, fatigue, sharpness,
                                     physical_attrs, technical_attrs, tactical_attrs, defensive_attrs, goalkeeping_attrs, hidden_attrs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                team_id, player.name, player.nationality, player.age, player.preferred_foot, json.dumps(player.positions),
                player.morale, player.fatigue, player.sharpness, json.dumps(player.physical), json.dumps(player.technical),
                json.dumps(player.tactical), json.dumps(player.defensive), json.dumps(player.goalkeeping), json.dumps(player.hidden)
            ))
            player_id = c.lastrowid

            # Save contract
            c.execute("""
                INSERT INTO contracts (player_id, wage, length, release_clause, bonuses)
                VALUES (?, ?, ?, ?, ?)
            """, (
                player_id, player.contract.wage, player.contract.length,
                player.contract.release_clause, json.dumps(player.contract.bonuses)
            ))
    conn.commit()

def load_league(conn, league_name):
    """Loads a league state from the database."""
    c = conn.cursor()
    league = League(name=league_name)

    # Load teams
    c.execute("SELECT * FROM teams")
    teams_data = c.fetchall()

    team_map = {} # To map team_id to Team object

    for team_data in teams_data:
        team = Team(name=team_data[1])
        team.finances['transfer_budget'] = team_data[2]
        team.finances['wage_budget'] = team_data[3]
        team.facilities['training'] = team_data[4]
        team.facilities['youth'] = team_data[5]
        team.tactics.formation = team_data[6]
        team.tactics.instructions = json.loads(team_data[7])

        league.add_team(team)
        team_map[team_data[0]] = team

    # Load players and contracts
    c.execute("""
        SELECT p.*, c.wage, c.length, c.release_clause, c.bonuses
        FROM players p
        JOIN contracts c ON p.id = c.player_id
    """)
    players_data = c.fetchall()

    for player_data in players_data:
        contract = Contract(
            wage=player_data[16],
            length=player_data[17],
            release_clause=player_data[18],
            bonuses=json.loads(player_data[19])
        )
        player = Player(
            name=player_data[2],
            nationality=player_data[3],
            age=player_data[4],
            preferred_foot=player_data[5],
            positions=json.loads(player_data[6]),
            contract=contract
        )
        player.morale = player_data[7]
        player.fatigue = player_data[8]
        player.sharpness = player_data[9]
        player.physical = json.loads(player_data[10])
        player.technical = json.loads(player_data[11])
        player.tactical = json.loads(player_data[12])
        player.defensive = json.loads(player_data[13])
        player.goalkeeping = json.loads(player_data[14])
        player.hidden = json.loads(player_data[15])

        team_id = player_data[1]
        team_map[team_id].add_player(player)

    return league
