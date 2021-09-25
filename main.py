import requests
import json
import sys

team_dict = {}
player_array = []
stats_array = []
player_projected_points = []


def get_player_projected_points(player):
    projection = 0
    if "goals" in player[1]["stats"][0]["splits"][0]["stat"]:
        projection += player[1]["stats"][0]["splits"][0]["stat"]["goals"]
        projection += player[1]["stats"][0]["splits"][0]["stat"]["assists"]
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["plusMinus"] * 0.1)
        projection += player[1]["stats"][0]["splits"][0]["stat"]["powerPlayPoints"]
        projection += player[1]["stats"][0]["splits"][0]["stat"]["shortHandedPoints"]
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["gameWinningGoals"] * 2)
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["shots"] * 0.1)
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["hits"] * 0.1)
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["blocked"] * 0.1)
    elif "wins" in player[1]["stats"][0]["splits"][0]["stat"]:
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["wins"] * 5)
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["goalsAgainst"] * -3)
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["saves"] * 0.6)
        projection += (player[1]["stats"][0]["splits"][0]["stat"]["shutouts"] * 5)
    player_projected_points.append([round(projection, 1), player[0]])


def get_teams_players():
    for i in range(1, 70):
        response = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{i}?expand=team.roster")
        team_dict[i] = json.loads(json.dumps(response.json()))
    return True


def main():
    get_teams_players()
    for i in range(1, 50):
        # try:
        #     print("*" * 50)
        #     print(team_dict[i]["teams"][0]["name"])
        #     print("*" * 50)
        # except (KeyError, IndexError):
        #     continue
        try:
            for x in range(0, 50):
                print(team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["fullName"], "->",
                      team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["link"], sep=" ")
                player_array.append((team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["fullName"],
                                     team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["link"]))
        except (KeyError, IndexError):
            print("TEAM DONE")
            continue
    # print(team_dict[1]["teams"][0]["active"])
    for key, value in player_array:
        # print(key, value)
        response = requests.get(f"https://statsapi.web.nhl.com{value}/stats?stats=statsSingleSeason"
                                f"&season=20202021")
        stats_array.append([key, json.loads(json.dumps(response.json()))])
    for player in stats_array:
        try:
            # print(player[0], player[1]["stats"][0]["splits"][0]["stat"], sep=" -> ")
            get_player_projected_points(player)
        except IndexError:
            continue
    for key, value in sorted(player_projected_points, reverse=True):
        print(key, value)


if __name__ == '__main__':
    main()
