import discord
from discord.ext import commands
import asyncio
import os
import yaml
from dotenv import load_dotenv
load_dotenv()

ip = os.getenv('IP')

with open("cogs/data/rules.yml", 'r', encoding="utf8") as stream:
    try:
        Data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


class Server(commands.Cog):
    def __init__(self, client):
        self.client=client

    @commands.command(breif="Server rules")
    async def rules(self,ctx):
        embed = discord.Embed(title="Minecraft Server Rules", description='Common sense is the most important rule :)', color=0x78b159)
        for data in Data['rules']:
            embed.add_field(name=data["name"], value=data['value'], inline=False)
        await ctx.reply(embed=embed)
    @commands.command(breif="Server ip")
    async def ip(self,ctx):
        await ctx.reply(f'**Server IP**: __{ip}__')


def setup(client):
    client.add_cog(Server(client))
