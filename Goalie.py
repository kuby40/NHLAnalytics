GOALS = 1
ASSISTS = 1
PLUS_MINUS = 0.1
POWER_PLAY_POINTS = 1
SHORT_HANDED_POINTS = 1
GAME_WINNING_GOALS = 2
SHOTS = 0.1
HITS = 0.1
BLOCKS = 0.1
WINS = 2
GOALS_AGAINST = -3
SAVES = 0.1
SHUTOUTS = 5


class Goalie:
    def __init__(self, name, position, wins, goals_against, saves, shutouts):
        self.name = name
        self.position = position
        self.wins = wins
        self.goals_against = goals_against
        self.saves = saves
        self.shutouts = shutouts
        self.projected_points = 0
        get_projected_points(self)


def get_projected_points(self):
    self.projected_points += (self.wins * WINS)
    self.projected_points += (self.goals_against * GOALS_AGAINST)
    self.projected_points += (self.saves * SAVES)
    self.projected_points += (self.shutouts * SHUTOUTS)
