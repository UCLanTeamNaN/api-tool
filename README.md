# FourWeekCLI

A Python CLI tool for the UCLan four week challenge API.

![demo](https://awo.oooooooooooooo.ooo/i/5bl6.png 'demo image')

## Install

> Requires Python 3.7+

Install dependencies

`pip3 install -r requirements.txt`

## Run

The tool has built in help for every command. It is split up similarly to the API documentation.

For example, python3 fwc.py game create [args] will create a new game.

Example usage:

```
fwc map list - List available maps
fwc game create testUser Mini_Map 5 - Create a new game on the Mini_Map map with TestUser as a username
fwc game join 53 testUser - Join a gain as testUser
fwc game start - Exit lobby & start game
fwc player move 5 yellow - Move your player to position 5 using a yellow ticket
fwc game players 53 - Get players in the game 
fwc player position - Get your player's position
fwc leaderboard - Get current leaderboard
```

## Token

Some commands require a token, this can be created automatically by the tool, or you can manually create a file
named `.sessiontoken` in the same directory as the script with your token in it.

If no `.sessiontoken` file exists on the system, you'll be prompted to enter a token everytime you run the script.