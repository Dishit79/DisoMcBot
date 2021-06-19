import discord
from discord.ext import commands, tasks
import asyncio
import base64
from aiohttp import ClientSession
from mcstatus import MinecraftServer
import time
import os
from dotenv import load_dotenv
load_dotenv()
ip = os.getenv('IP')
prefix = os.getenv('PREFIX')
#imgur credintials
client_id = os.getenv('CLIENT_ID')
api_key = os.getenv('API_KEY')
url = os.getenv('URL')

client = commands.Bot(case_insensitive=True,command_prefix=prefix)
server = MinecraftServer.lookup(ip)
img_cache = None

async def fetchData():
    global server
    try:
        query = await server.async_status()
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

async def fetchImage(image):
    global img_cache
    if img_cache:
        return img_cache
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
    img_cache = data['data']['link']
    return data['data']['link']

@client.command(brief='This is the brief description')
async def status(ctx):
    image = 'https://imgur.com/m84S3So.png'
    data = await fetchData()
    if data['status']=='online':
        if data['data'].favicon:
            image = await fetchImage(data['data'].favicon[22:] or None)
        print(data['data'].description)
        embed = discord.Embed(title="Minecraft Server Status", description=data['data'].description, color=0x78b159)
        embed.set_footer(text=f'{ip} | Server Status v2.5 by Jhoan')
        embed.set_thumbnail(url=image)
        embed.add_field(name='Server Status: ', value=':green_circle: **| Online**', inline=False)
        embed.add_field(name='Minecraft Version: ', value=data['data'].version.name, inline=False)
        embed.add_field(name='Players Online: ', value=(f'{data["data"].players.online}/{data["data"].players.max}'), inline=True)
        if 10 > data['data'].players.online > 0 :
            embed.add_field(name='Players Playing : ', value=''.join(f"`{d.name}` " for d in data['data'].players.sample), inline=True)
        await ctx.reply(embed=embed)
    elif data['status']=='offline':
        embed = discord.Embed(title="Minecraft Server Status", color=0xdd2e44)
        embed.set_footer(text=f'{ip} | Server Status v2.5 by Jhoan')
        embed.set_thumbnail(url=image)
        embed.add_field(name='Server Status: ', value=':red_circle: **| Offline**', inline=False)
        await ctx.reply(embed=embed)
    else:
        embed = discord.Embed(title=":x: **| Server not reachable**", color=0xE10600)
        embed.set_footer(text=f'{ip} | Server Status v2.5 by Jhoan')
        await ctx.send(embed=embed)

@client.group()
@commands.has_permissions(manage_messages=True)
async def cache(ctx):
    await ctx.send(f"Img: {img_cache} \n Ip: {ip}")

@cache.command()
async def reset(ctx):
    global img_cache
    img_cache= None
    await ctx.send(':white_check_mark: Image cache reset')

@cache.command()
async def ip_change(ctx, newip=ip):
    ip = newip
    await ctx.send(f':white_check_mark: Set ip to {newip}')

@cache.error
async def logging_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.reply("Sorry you can not use that command")
    else:
        await ctx.reply("Something went wrong")

@tasks.loop(seconds=60)
async def change_status():
    data = await fetchData()
    if data['status']=='online':
        activity = discord.Game(f"with {data['data'].players.online} friends | Online")
        await client.change_presence(activity=activity)
    elif data['status']=='offline':
        activity = discord.Game(f"Offline | Last checked {time.strftime('%H:%M:%S', time.localtime())}")
        await client.change_presence(status=discord.Status.dnd, activity=activity)
    else:
        activity = discord.Game(f"no server")
        await client.change_presence(status=discord.Status.dnd, activity=activity)

@client.event
async def on_ready():
    change_status.start()
    activity = discord.Game(name="Checking server", type=3)
    await client.change_presence(activity=activity)
    print('We have logged in as {0.user}'.format(client))

client.run(os.getenv('BOT_KEY'))
