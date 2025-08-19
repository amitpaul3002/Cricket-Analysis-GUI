# data_store.py

team_data = {
    "team1": {"name": "", "runs": 0, "overs": 0.0, "total_overs":0.0, "wickets": 0},
    "team2": {"name": "", "runs": 0, "overs": 0.0, "total_overs": 0.0, "wickets": 0, "game_over": False}
}

team_players = {
    "team1": {"batsmen": [], "bowlers": []},
    "team2": {"batsmen": [], "bowlers": []}
}

def reset_team_data():
    """Resets all team data to their initial state."""
    team_data.clear()
    team_data.update({
        "team1": {"name": "", "runs": 0, "overs": 0.0, "total_overs": 0.0, "wickets": 0},
        "team2": {"name": "", "runs": 0, "overs": 0.0, "total_overs": 0.0, "wickets": 0, "game_over": False}
    })
    
def reset_team_players():
    """Resets all player data to their initial state."""
    team_players.clear()
    team_players.update({
        "team1": {"batsmen": [], "bowlers": []},
        "team2": {"batsmen": [], "bowlers": []}
    })
    
    
