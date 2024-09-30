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
    team_codes = []
    res = requests.get('https://api-web.nhle.com/v1/standings/now')
    for team in res.json()['standings']:
        team_codes.append(team['teamAbbrev']['default'])
    player_array = []
    url = 'https://api-web.nhle.com/v1/roster/{}/current'
    team_codes.remove("ARI")
    team_codes.append("UTA")
    for team in team_codes:
        print("Currently on ", team)
        res = requests.get(url.format(team))
        player_array += [player for position in ['forwards', 'defensemen', 'goalies'] for player in res.json()[position]]
    return player_array


def create_players(player_array):
    """Brings in player data and calculates the points for each player. Sends the players out to get written in a file
    for easy reading"""
    forward_array = []
    defense_array = []
    goalie_array = []
    playerStatsResponse = requests.get(f"https://api.nhle.com/stats/rest/en/skater/realtime?limit=-1&cayenneExp=seasonId=20232024%20and%20gameTypeId=2")
    playerStats = json.loads(json.dumps(playerStatsResponse.json())) 
    goalieStatsResponse = requests.get(f"https://api.nhle.com/stats/rest/en/goalie/summary?limit=-1&cayenneExp=seasonId=20232024")
    goalieStats = json.loads(json.dumps(goalieStatsResponse.json())) 
    # loops for player data
    for player in player_array:
        response = requests.get(f"https://api-web.nhle.com/v1/player/{player["id"]}/landing")
        temp = json.loads(json.dumps(response.json()))
        playerStatsFoundIndex = -1
        
        # Calculates forward and defencemen points
        if player["positionCode"] != "G":
            for index, data in enumerate(playerStats["data"]): 
                if data["playerId"] == player["id"]:
                    playerStatsFoundIndex = index
                    break
            filtered_temp = [d for d in temp["seasonTotals"] if d["season"] == 20232024 and d["leagueAbbrev"] == "NHL" and d["gameTypeId"] == 2]
            try:
                skater = Forward(player["firstName"]["default"] + " " + player["lastName"]["default"], player["positionCode"], filtered_temp[0]["goals"],
                                 filtered_temp[0]["assists"],
                                 filtered_temp[0]["plusMinus"],
                                 filtered_temp[0]["powerPlayPoints"],
                                 filtered_temp[0]["shorthandedPoints"],
                                 filtered_temp[0]["shots"],
                                 playerStats["data"][playerStatsFoundIndex]["hits"],
                                 playerStats["data"][playerStatsFoundIndex]["blockedShots"],
                                 filtered_temp[0]["gamesPlayed"])
                print("Player " + skater.name + " created")
                if player["positionCode"] == "D":
                    defense_array.append(skater)
                else:
                    forward_array.append(skater)
            except IndexError:
                print("Player " + player["firstName"]["default"] + " " + player["lastName"]["default"] + " has no relevant data.. SKIPPING")
                continue
        # Calculates goalie points
        else:
            for index, data in enumerate(goalieStats["data"]): 
                if data["playerId"] == player["id"]:
                    playerStatsFoundIndex = index
                    break
            try:
                skater = Goalie(player["firstName"]["default"] + " " + player["lastName"]["default"], player["positionCode"], goalieStats["data"][playerStatsFoundIndex]["wins"],
                                goalieStats["data"][playerStatsFoundIndex]["goalsAgainst"],
                                goalieStats["data"][playerStatsFoundIndex]["saves"],
                                goalieStats["data"][playerStatsFoundIndex]["shutouts"],
                                goalieStats["data"][playerStatsFoundIndex]["gamesPlayed"])
                print("Player " + skater.name + " created")
                goalie_array.append(skater)
            except IndexError:
                print("Player " + player["firstName"]["default"] + " " + player["lastName"]["default"] + " has no relevant data.. SKIPPING")
                continue
    # Writes all arrays into the files
    write_to_file(forward_array, "forwards")
    write_to_file(defense_array, "defenseman")
    write_to_file(goalie_array, "goalies")


def main():
    """Program to find the average points per game an NHL Player would get using the current point structure
     in the league I'm currently in. Point structure can be changed in the Goalie and Forward Classes."""
    create_players(get_teams_players())


if __name__ == '__main__':
    main()
