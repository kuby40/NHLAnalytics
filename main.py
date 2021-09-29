import requests
import json
from Forward import Forward
from Goalie import Goalie


def write_to_file(player_array, name_of_role):
    """Writes all data to 3 separate files,
    1 for Forwards (`forwards.txt`),
    1 for Defencemen (`defenceman.txt`),
    and 1 for Goalies (`goalies.txt`)"""
    # Sorts the arrays by points before printing to files
    player_array.sort(key=lambda x: x.projected_points, reverse=True)

    f = open(f"{name_of_role}.txt", "w")
    for player in player_array:
        f.write(f"{player.name}\t{player.projected_points}\n")
    f.close()


def get_teams_players():
    """Uses the NHL API to get data for processing.
    Stores all data into global array: `player_array`"""

    print("Getting all teams players...")
    # loops and get all NHL teams roster
    team_dict = {}
    player_array = []
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
    return player_array


def create_players(player_array):
    """Brings in player data and calculates the points for each player. Sends the players out to get written in a file
    for easy reading"""
    forward_array = []
    defence_array = []
    goalie_array = []
    # loops for player data
    for player in player_array:
        response = requests.get(f"https://statsapi.web.nhl.com{player[1]}/stats?stats=statsSingleSeason"
                                f"&season=20202021")
        temp = json.loads(json.dumps(response.json()))
        # Calculates forward and defencemen points
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
                                 temp["stats"][0]["splits"][0]["stat"]["blocked"],
                                 temp["stats"][0]["splits"][0]["stat"]["games"])
                print("Player " + skater.name + " created")
                if player[2] == "Defenseman":
                    defence_array.append(skater)
                else:
                    forward_array.append(skater)
            except IndexError:
                print("Player " + player[0] + " has no relevant data.. SKIPPING")
                continue
        # Calculates goalie points
        else:
            try:
                skater = Goalie(player[0], player[2], temp["stats"][0]["splits"][0]["stat"]["wins"],
                                temp["stats"][0]["splits"][0]["stat"]["goalsAgainst"],
                                temp["stats"][0]["splits"][0]["stat"]["saves"],
                                temp["stats"][0]["splits"][0]["stat"]["shutouts"],
                                temp["stats"][0]["splits"][0]["stat"]["games"])
                print("Player " + skater.name + " created")
                goalie_array.append(skater)
            except IndexError:
                print("Player " + player[0] + " has no relevant data.. SKIPPING")
                continue
    # Writes all arrays into the files
    write_to_file(forward_array, "forwards")
    write_to_file(defence_array, "defenseman")
    write_to_file(goalie_array, "goalies")


def main():
    """Program to find the average points per game an NHL Player would get using the current point structure
     in the league I'm currently in. Point structure can be changed in the Goalie and Forward Classes."""
    create_players(get_teams_players())


if __name__ == '__main__':
    main()
