import discord
from discord.ext import commands, tasks
import asyncio
import paramiko
from aiohttp import ClientSession
import datetime
import pytz
import os
from dotenv import load_dotenv
load_dotenv()

ip = os.getenv('IP')
server_ip = os.getenv('SERVER_IP')
user = os.getenv('SERVER_USER')
pas = os.getenv('SERVER_PAS')

class ServerControl(commands.Cog):
    def __init__(self, client):
        self.client=client


    @commands.command(breif="Server rules")
    @commands.has_permissions(administrator=True)
    async def start(self,ctx):

        session = ClientSession()
        rawonline = await session.get(f'https://mcapi.xdefcon.com/server/{ip}/full/json')
        online = await rawonline.json()
        await session.close()

        print(online['serverStatus'])
        if online['serverStatus'] == 'online':
            await ctx.send("Server is already online")
        else:
            mess = await ctx.reply("Connecting <a:loading:858371469934198785>")
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(server_ip, username=user, password=pas)
            except:
                await asyncio.sleep(5)
                return await mess.edit(content="Failed to connect. :x:")

            await asyncio.sleep(2)
            await mess.edit(content="Connected ✔")
            await asyncio.sleep(2)
            await mess.edit(content="Starting server <a:loading:858371469934198785>")
            try:
                stdin, stdout, stderr = client.exec_command('systemctl start minecraft')
                print([t for t in stdout])
            except:
                await asyncio.sleep(2)
                return await mess.edit(content="Failed to start server. :x:")
            await asyncio.sleep(2)
            await mess.edit(content=":white_check_mark: Server started!")


def setup(client):
    client.add_cog(ServerControl(client))
