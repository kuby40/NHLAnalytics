# Points per:
WINS = 2
GOALS_AGAINST = -3
SAVES = 0.1
SHUTOUTS = 5


class Goalie:
    def __init__(self, name, position, wins, goals_against, saves, shutouts, games_played):
        self.name = name
        self.position = position
        self.wins = wins
        self.goals_against = goals_against
        self.saves = saves
        self.shutouts = shutouts
        self.games_played = games_played
        self.projected_points = 0
        get_projected_points(self)


def get_projected_points(self):
    self.projected_points += (self.wins * WINS)
    self.projected_points += (self.goals_against * GOALS_AGAINST)
    self.projected_points += (self.saves * SAVES)
    self.projected_points += (self.shutouts * SHUTOUTS)
    self.projected_points = self.projected_points / self.games_played
