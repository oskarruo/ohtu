class PlayerStats:
    def __init__(self, reader):
        self.stats = reader.players
    
    def top_scorers_by_nationality(self, nat):
        players_by_nationality = filter(lambda player: player.nationality == nat, self.stats)
        sorted_players = sorted(players_by_nationality, key=sort_by_points, reverse=True)
        return sorted_players

def sort_by_points(player):
    return player.goals + player.assists