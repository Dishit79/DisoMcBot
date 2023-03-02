from discord.ext.commands import Greedy, Context # or a subclass of yours
from typing import Literal, Optional
import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

prefix = os.getenv('PREFIX')

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix=prefix)

@client.event
async def on_ready():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
           await client.load_extension(f'cogs.{filename[:-3]}')

    activity = discord.Game(name="Checking server", type=3)
    await client.change_presence(activity=activity)
    print('We have logged in as {0.user}'.format(client))


@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["reload", "refresh", "clear"]] = None) -> None:
    if not guilds:
        if spec == "reload":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "refresh":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "clear":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


client.run(os.getenv('BOT_KEY'))
