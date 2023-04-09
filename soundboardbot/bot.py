import discord
import re

from discord.ext import commands
from discord.ext import commands

from soundboardbot.constants import sounds

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')


@bot.command(name='join')
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command(name='leave')
async def leave(ctx):
    await ctx.voice_client.disconnect()
    

@bot.command(name='info')
async def info(ctx, tag):
    tag = re.sub(r'\D', '', tag)
    await ctx.send(f'User ID: {tag}, Guild ID: {ctx.guild.id}')
    

@bot.command(name='list')
async def list_sounds(ctx):
    available_sounds = "\n".join([sound for sound in sounds.keys()])
    message = f"List of all available sounds:\n{available_sounds}"
    await ctx.send(message)
