import requests
import json
import sys

team_dict = {}
player_dict = []


def get_teams_players():
    for i in range(1, 70):
        response = requests.get(f"https://statsapi.web.nhl.com/api/v1/teams/{i}?expand=team.roster")
        team_dict[i] = json.loads(json.dumps(response.json()))
    return True


def main():
    get_teams_players()
    for i in range(1, 50):
        try:
            print("*" * 50)
            print(team_dict[i]["teams"][0]["name"])
            print("*" * 50)
        except (KeyError, IndexError):
            continue
        try:
            for x in range(0, 50):
                print(team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["fullName"], "->",
                      team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["link"], sep=" ")
                player_dict.append((team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["fullName"],
                                    team_dict[i]["teams"][0]["roster"]["roster"][x]["person"]["link"]))
        except (KeyError, IndexError):
            print("TEAM DONE")
            continue
    # print(team_dict[1]["teams"][0]["active"])
    for key, value in player_dict:
        print(key, value)


if __name__ == '__main__':
    main()

# id, jerseyNumber
