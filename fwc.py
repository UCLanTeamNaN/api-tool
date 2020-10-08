# Four Week CLI
# A CLI tool for the UCLan computing challenge API

print("👋 Welcome to FourWeekCLI - provided by Team NaN.")

import requests
import fire
import os

baseUrl = "http://challenge.uclan.ac.uk:8080/preston"
docsUrl = "https://github.com/UCLanTeamNaN/api-docs/blob/master/docs"

# Convert weird CSV into object
def csvToObject(response):
    # Takes response data and returns an object.
    data = response.split("\n")
    status_code, status_desc = data[0].split(",")[0], data[0].split(",")[1]

    return {
        "status": {"code": status_code.strip('"'), "description": status_desc.strip('"')},
        "data": data[1:]
    }

def fetch(endpoint, parameters=""):
    url = f"{baseUrl}/{endpoint}{parameters}"
    print(f"📞 Calling: {url}")

    r = requests.get(url)
    print(f"⏰ Response time: {r.elapsed}")
    data = csvToObject(r.text)

    if data['status']['code'] != "OK": 
        print(f"\n\n😭 Failed to get data:\nError: {data['status']['code']}\nMessage: {data['status']['description']}")
        return exit()
    
    return data

def getToken():
    # Returns the currently active token, checks if the file exists or prompts the user
    if os.path.exists(".sessiontoken"):
        # Read file from
        with open(".sessiontoken", "r+") as f:
            print("🔑 Read session token from disk.")
            return f.read()
    else:
        print("🔑 This command requires a token, if you have one please enter it now:")
        return input("🔑: ")

class Maps:
    """
    Subcommands for interacting with the maps API"""
    def list(self):
        """
        Get list of available maps"""

        print(f"📕 Documentation: {docsUrl}/maps.md#get-all-maps")

        data = fetch("getMaps")
        
        for MapInstance in data['data']:
            MapInstance = MapInstance.split(",")
            name = MapInstance[0].strip('"')
            
            print(f"\n---\n🗺 Map Name: {name}\n🎲 Available Rounds: ")
            for rounds in MapInstance[1:]:
                rounds = rounds.strip('"')
                print(f" - {rounds}")

class Game:
    """
    Subcommands for interacting with game instances (or creating new ones)"""

    def create(self, playerName, mapName, numRounds):
        """
        Create a new game, requires playerName, mapName and numRounds (see maps list)"""
        print(f"📕 Documentation: {docsUrl}/games.md#create-game")

        print("‼ This command creates a new PUBLIC game on the PUBLIC API, do not abuse this!")
        if input("❓ Really create a new game? [y/N] ").lower() != "y": return print("❌ Aborted.")

        data = fetch("createGame", 
        f"?playerName={playerName}&mapName={mapName}&numRounds={numRounds}&appID=8A-TestCLI")
        result = data['data'][0].split(",")
        sessionToken = result[0].strip('"')
        joinCode = result[1].strip('"')
        print("🎉 Created new game!")
        print(f"🔑 User session token: {sessionToken}")
        print(f"🏓 Game join code: {joinCode}")

        print("❗ fwcli can save this token and use it with commands that require tokens later.")
        if input("❓ Save token to local machine? [Y/n] ").lower() == "n": return print("✅ All done.")

        with open(".sessiontoken", "w+") as f:
            f.write(sessionToken)
        
        print("✅ Written .sessiontoken to disk.")

    def state(self):
        """
        Get the state of the user's current game"""
        print(f"📕 Documentation: {docsUrl}/games.md#get-game-state")

        data = fetch(f"/getGameState;jsessionid={getToken()}")
        result = data['data'][0].split(",")
        state = result[0].strip('"')
        roundNo = result[1].strip('"')
        if len(result) == 3: message = result[2].strip('"')
        else: message = "No message."

        print(f"\n🕹 Game State: {state}\n🎲 Round number: {roundNo}\n💬 Message: {message}")

    def start(self, gameID):
        """
        Start an existing game, requires a session."""
        print(f"📕 Documentation: {docsUrl}/games.md#start-game")

        data = fetch(f"/startGame;jsessionid={getToken()}?gameID={gameID}")

        print("\n👍 Lobby closed & Game started! 🎉🎉🎉")

    def join(self, gameID, playerName):
        """
        Join an existing game, state must be OPEN!"""
        print(f"📕 Documentation: {docsUrl}/games.md#join-game")
        
        data = fetch(f"/joinGame?playerName={playerName}&gameID={gameID}&appID=8A-TestCLI")

        sessionId = data['data'][0].strip('"')
        print(f"\n🎉 {playerName} has joined the game!")
        print(f"🔑 Session token: {sessionId}")

        print("❗ fwcli can save this token and use it with commands that require tokens later.")
        if input("❓ Save token to local machine? [Y/n] ").lower() == "n": return print("✅ All done.")

        with open(".sessiontoken", "w+") as f:
            f.write(sessionId)
        
        print("✅ Written .sessiontoken to disk.")

    def players(self, gameId):
        """
        Get all players in game game"""
        print(f"📕 Documentation: {docsUrl}/games.md#get-players-in-current-game")

        data = fetch(f"/getPlayers?gameID={gameId}")

        if len(data['data']) == 0: return print("\n❌ Invalid game or no players in session.")

        for player in data['data']:
            name = player.split(",")[0].strip('"')
            colour = player.split(",")[1].strip('"')

            print(f"\n---\n🤺 Player Name: {name}\n🔴 Player Colour: {colour}")


class Player:
    """
    Subcommands for getting/controlling players in games"""

    def move(self, destination, ticket):
        """
        Move your player to a new destination and use a colour of ticket"""
        print(f"📕 Documentation: {docsUrl}/players.md#make-move")

        if ticket not in ["yellow", "red", "green"]: return print("❗ Ticket must be yellow/red/green!")

        data = fetch(f"/makeMove;jsessionid={getToken()}?destination={destination}&ticket={ticket}")

        print("✅ Moved.")

    def position(self):
        """
        Get your player's current position"""
        print(f"📕 Documentation: {docsUrl}/players.md#get-position")

        data = fetch(f"/getPosition;jsessionid={getToken()}")
        location = data['data'][0].strip('"')

        print(f"\n📍 Location: {location}")


def leaderboard():
    """
    Get the current leaderboard"""
    data = fetch(f"/getLeaderboard")
    topScore = 0
    topScoreTeam = ""
    
    scores = []

    for team in data['data']:
        name, points = team.split(",")
        
        name = name.strip('"')
        points = float(points.strip('"'))

        scores.append((name, points))

    scores.sort(key=lambda x:x[1])
    scores.reverse()

    for team in scores:
        name, points = team[0], team[1]

        if name == "NoName8A":
            print(f"🤼 ❗ {name} - {points}")
        else:
            print(f"🤼 {name} - {points}")

        if float(points) > topScore:
            topScore = float(points)
            topScoreTeam = name

    print("\n❗* - Team 8A - Developers of api-tool.")

    print(f"\n--------\n🎉Top Scoring Team 🎉\n{topScoreTeam}\nScore: {topScore} points.")

# Setup CLI
if __name__ == "__main__":
    fire.Fire({
        "map": Maps,
        "leaderboard": leaderboard,
        "game": Game,
        "player": Player
    })