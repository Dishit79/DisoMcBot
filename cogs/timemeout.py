import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import time
import json
import os
from dotenv import load_dotenv
load_dotenv()

ip = os.getenv('CHANNEL_ID')

class TimeMeOut(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.hybrid_command(brief='Temp ban yourself')
    async def timeout(self, ctx: discord.Interaction, hours: int):
        member = ctx.author


        jsonFile = open("/home/nawaf/Documents/GitHub/DisoMcBot/cogs/data/data.json", "r") # Open the JSON file for reading
        data = json.load(jsonFile) # Read the JSON into the buffer
        jsonFile.close() # Close the JSON file

        for u in data["users"]:
            print(u)
            if u['id'] == member.id:
                username = u['name']
                
                
        for ban in data["bantime"]:
            if ban['id'] == member.id:
                return await ctx.send("Already in timeout")

        t = {"id":member.id, "username": username, "unbantime": time.time() + (3600 * hours)} 
        
        data["bantime"].append(t)

        # Save our changes to JSON
        jsonFile = open("/home/nawaf/Documents/GitHub/DisoMcBot/cogs/data/data.json", "w+")
        jsonFile.write(json.dumps(data))
        jsonFile.close()

    @tasks.loop(seconds=60)
    async def change_status(self):
        try:
            data = await self.fetchData()
        except:
            data = {'status':'failed'}
        if data['status']=='online':
            activity = discord.Game(f"with {data['data'].players.online} friends | Online")
            await self.client.change_presence(activity=activity)
        elif data['status']=='offline':
            activity = discord.Game(f"Offline | Last checked {time.strftime('%H:%M:%S', time.localtime())}")
            await self.client.change_presence(status=discord.Status.dnd, activity=activity)
        else:
            activity = discord.Game(f"Failed")
            await self.client.change_presence(status=discord.Status.dnd, activity=activity)

    
        

async def setup(client):
    await client.add_cog(TimeMeOut(client))
