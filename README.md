DisoMcBot
======

DisoMCBot is a Minecraft status bot for SMP servers. It provides the server's status and online players. You can add and remove cogs to customize the bots commands. The cogs are added automatically and default cog is `status.py`

## Installation
1. Install all requirements using `pip install -r requirements.txt`
2. Create a `.env` file like the one below.
```
IP="minecraft server ip"
PREFIX="!"

#imgur credentials
CLIENT_ID="imgur client id"
API_KEY="imgur client secret"
URL="https://api.imgur.com/3"

BOT_KEY="discord bot token"

#SSH credentials (this part not needed if you are not using servercontrol cog)
SERVER_IP = "ssh server ip"
SERVER_USER = "dishit"
SERVER_PAS = "password"
```
3. Run bot!


## Preview:
### Online Embed:
![plot](./preview/image1.png)
### Offline Embed:
![plot](./preview/image2.jpg)
### Timings check command:
![plot](./preview/image3.gif)


## Todo:
1. ~~Add error handling~~
2. ~~Add birdflop's timing analyzer~~
3. ~~Rebase everything into cogs~~
4. Make a docker
