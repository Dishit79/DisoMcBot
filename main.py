import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

prefix = os.getenv('PREFIX')

client = commands.Bot(case_insensitive=True,command_prefix=prefix)

@client.event
async def on_ready():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

    activity = discord.Game(name="Checking server", type=3)
    await client.change_presence(activity=activity)
    print('We have logged in as {0.user}'.format(client))

client.run(os.getenv('BOT_KEY'))
