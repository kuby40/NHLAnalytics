import requests
import json
from Forward import Forward
from Goalie import Goalie

# CONSTANTS FOR POINTS
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

# ARRAYS
team_dict = {}
player_array = []
stats_array = []
forward_array = []
defence_array = []
goalie_array = []


def write_to_file():
    forward_array.sort(key=lambda x: x.projected_points, reverse=True)
    defence_array.sort(key=lambda x: x.projected_points, reverse=True)
    goalie_array.sort(key=lambda x: x.projected_points, reverse=True)

    f = open("forwards.txt", "w")
    for player in forward_array:
        f.write(f"{player.name}\t{player.projected_points}\n")
    f.close()
    f = open("defence.txt", "w")
    for player in defence_array:
        f.write(f"{player.name}\t{player.projected_points}\n")
    f.close()
    f = open("goalie.txt", "w")
    for player in goalie_array:
        f.write(f"{player.name}\t{player.projected_points}\n")
    f.close()


def get_teams_players():
    print("Getting all teams players...")
    for i in range(1, 70):
        response = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{i}?expand=team.roster")
        team_dict[i] = json.loads(json.dumps(response.json()))
    for i in range(1, 50):
        try:
            for x in range(0, 50):
                player = (team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["fullName"],
                          team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["link"],
                          team_dict[i]["teams"][0]["roster"]["roster"][x]["position"]["type"])
                player_array.append(player)
        except (KeyError, IndexError):
            continue


def create_players():
    for player in player_array:
        response = requests.get(f"https://statsapi.web.nhl.com{player[1]}/stats?stats=statsSingleSeason"
                                f"&season=20202021")
        temp = json.loads(json.dumps(response.json()))
        if player[2] != "Goalie":
            try:
                skater = Forward(player[0], player[2], temp["stats"][0]["splits"][0]["stat"]["goals"],
                                 temp["stats"][0]["splits"][0]["stat"]["assists"],
                                 temp["stats"][0]["splits"][0]["stat"]["plusMinus"],
                                 temp["stats"][0]["splits"][0]["stat"]["powerPlayPoints"],
                                 temp["stats"][0]["splits"][0]["stat"]["shortHandedPoints"],
                                 temp["stats"][0]["splits"][0]["stat"]["gameWinningGoals"],
                                 temp["stats"][0]["splits"][0]["stat"]["shots"],
                                 temp["stats"][0]["splits"][0]["stat"]["hits"],
                                 temp["stats"][0]["splits"][0]["stat"]["blocked"])
                print("Player " + skater.name + " created")
                if player[2] == "Defenseman":
                    defence_array.append(skater)
                else:
                    forward_array.append(skater)
            except IndexError:
                print("Player " + player[0] + " has no relevant data.. SKIPPING")
                continue
        else:
            try:
                skater = Goalie(player[0], player[2], temp["stats"][0]["splits"][0]["stat"]["wins"],
                                temp["stats"][0]["splits"][0]["stat"]["goalsAgainst"],
                                temp["stats"][0]["splits"][0]["stat"]["saves"],
                                temp["stats"][0]["splits"][0]["stat"]["shutouts"])
                print("Player " + skater.name + " created")
                goalie_array.append(skater)
            except IndexError:
                print("Player " + player[0] + " has no relevant data.. SKIPPING")
                continue


def main():
    get_teams_players()
    create_players()
    write_to_file()


if __name__ == '__main__':
    main()
