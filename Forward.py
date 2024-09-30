# Points per:
GOALS = 6
ASSISTS = 4
PLUS_MINUS = 2
POWER_PLAY_POINTS = 2
SHORT_HANDED_POINTS = 2
# GAME_WINNING_GOALS = 2
SHOTS = 0.5
HITS = 0.5
BLOCKS = 0.5


class Forward:

    def __init__(self, name, position, goals, assists, plus_minus, power_play_points, shorthanded_points,
                 shots_on_goal, hits, blocks, games_played,
                 #game_winning_goals
                 ):
        self.name = name
        self.position = position
        self.goals = goals
        self.assists = assists
        self.plus_minus = plus_minus
        self.power_play_points = power_play_points
        self.shorthanded_points = shorthanded_points
        #self.game_winning_goals = game_winning_goals
        self.shots_on_goal = shots_on_goal
        self.hits = hits
        self.blocks = blocks
        self.games_played = games_played
        self.projected_points = 0
        get_projected_points(self)


def get_projected_points(self):
    self.projected_points += (self.goals * GOALS)
    self.projected_points += (self.assists * ASSISTS)
    self.projected_points += (self.plus_minus * PLUS_MINUS)
    self.projected_points += (self.power_play_points * POWER_PLAY_POINTS)
    self.projected_points += (self.shorthanded_points * SHORT_HANDED_POINTS)
    #self.projected_points += (self.game_winning_goals * GAME_WINNING_GOALS)
    self.projected_points += (self.shots_on_goal * SHOTS)
    self.projected_points += (self.hits * HITS)
    self.projected_points += (self.blocks * BLOCKS)
    self.projected_points = self.projected_points / self.games_played
