DisoMcBot
======

DisoMCBot is a Mineecraft stauts bot for SMP servers. It tells user when server is offline or online and how many players are playing.

## Installation
1. Install all requirements using `pip install -r requirements.txt`
2. Create a `.env` file like the one below.
```
IP="minecraft server ip"
PREFIX="!"

#imgur credintials
CLIENT_ID="imgur client id"
API_KEY="imgur client secret"
URL="https://api.imgur.com/3"

BOT_KEY="discord bot token"
```
3. Run bot!

## Todo:
1. Add error handling
2. Add birdflop's timing analyser
3. Rebase everything into cogs
4. Make a docker
