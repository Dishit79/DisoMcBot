import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from aiohttp import ClientSession
from mcstatus import JavaServer
import time
import os
from dotenv import load_dotenv
load_dotenv()

ip = os.getenv('IP')
#imgur credintials
client_id = os.getenv('CLIENT_ID')
api_key = os.getenv('API_KEY')
url = os.getenv('URL')
version_number = "2.0"

class Status(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.server = JavaServer.lookup(ip)
        self.img_cache = None
        self.change_status.start()

    async def fetchData(self):
        try:
            query = await self.server.async_status()
            return {'status':'online','data':query}
        except ConnectionRefusedError:
            return {'status':'offline','data': None}
        except asyncio.TimeoutError:
            print ('e')
            return await fetchData()
        except Exception as e:
            print (e.message, e.args)
            print('ew')
            server = MinecraftServer.lookup(ip)
            return {'status':'nothing','data': None}

    async def fetchImage(self,image):
        if self.img_cache:
            return self.img_cache
        session = ClientSession()
        submit = await session.post(
            f'{url}/upload.json',
            headers = {"Authorization": f"Client-ID {client_id}"},
            data = {
                'key': api_key,
                'image': image,
                'type': 'base64',
                'name': '1.jpg',
                'title': 'Picture no. 1'
            }
        )
        data = await submit.json()
        await session.close()
        self.img_cache = data['data']['link']
        return data['data']['link'] 
    
    @commands.hybrid_command(brief='Check server status')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def status(self, ctx: discord.Interaction):
        image = 'https://imgur.com/m84S3So.png'
        data = await self.fetchData()
        if data['status']=='online':
            if data['data'].favicon:
                image = await self.fetchImage(data['data'].favicon[22:] or None)
            print(data['data'].description)
            embed = discord.Embed(title="Minecraft Server Status", description=data['data'].description, color=0x78b159)
            embed.set_footer(text=f'{ip} | Server Status v{version_number}')
            embed.set_thumbnail(url=image)
            embed.add_field(name='Server Status: ', value=':green_circle: **| Online**', inline=False)
            embed.add_field(name='Minecraft Version: ', value=data['data'].version.name, inline=False)
            embed.add_field(name='Players Online: ', value=(f'{data["data"].players.online}/{data["data"].players.max}'), inline=True)
            if 10 > data['data'].players.online > 0 :
                embed.add_field(name='Players Playing : ', value=''.join(f"`{d.name}` " for d in data['data'].players.sample), inline=True)
            await ctx.reply(embed=embed)
        elif data['status']=='offline':
            embed = discord.Embed(title="Minecraft Server Status", color=0xdd2e44)
            embed.set_footer(text=f'{ip} | Server Status v{version_number}')
            embed.set_thumbnail(url=image)
            embed.add_field(name='Server Status: ', value=':red_circle: **| Offline**', inline=False)
            await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(title=":x: **| Server not reachable**", color=0xE10600)
            embed.set_footer(text=f'{ip} | Server Status v{version_number}')
            await ctx.send(embed=embed)

    @status.error
    async def logging_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Please try again in {str(error.retry_after)[:4]} seconds")
        else:
            print(error)
            await ctx.reply("Something went wrong")

    @commands.group(brief="View settings")
    @commands.has_permissions(manage_messages=True)
    async def settings(self, ctx):
        await ctx.send(f"Img: {self.img_cache} \n Ip: {ip}")

    @settings.command(brief="Reset server image")
    async def reset(self, ctx):
        self.img_cache= None
        await ctx.send(':white_check_mark: Image cache reset')

    @settings.command(brief="Change server ip")
    async def ip_change(self, ctx, newip=ip):
        ip = newip
        await ctx.send(f':white_check_mark: Set ip to {newip}')

    @settings.command(brief="Reset bot status")
    async def reset_status(self, ctx, newip=ip):
        try:
            self.change_status.start()
            await ctx.send(":white_check_mark: Status reset")
        except:
            await ctx.send(":x: Failed to reset status")

    @settings.error
    async def logging_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.reply("Sorry you can not use that command")
        else:
            print(error)
            await ctx.reply("Something went wrong")

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
    await client.add_cog(Status(client))
