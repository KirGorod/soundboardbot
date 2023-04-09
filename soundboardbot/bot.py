import os
import asyncio
import discord
import re
from dotenv import load_dotenv
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from discord.ext import commands
from discord.ext import commands
from discord import errors

load_dotenv()

TOKEN = os.getenv('TOKEN')
intents = discord.Intents.all()

app = FastAPI()
bot = commands.Bot(command_prefix='!', intents=intents)


class PlaySound(BaseModel):
    user_id: int
    guild_id: int
    sound: str


sounds = {
    'iwo': {
        'file': 'iwo.mp3',
        'volume': 1
    },
    'horn': {
        'file': 'horn.mp3',
        'volume': 1    
    },
    'airhorn': {
        'file': 'airhorn.mp3',
        'volume': 0.1
    }
}


@app.on_event('startup')
async def startup():
    asyncio.create_task(run())


@app.post('/')
async def play_sound(body: PlaySound):
    try:
        # guild = bot.get_guild(body.guild_id)
        # member = guild.get_member(body.user_id)
        member = bot.get_user(body.user_id)
        bot_obj = bot
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    if not body.sound:
        return

    file_name = sounds.get(body.sound).get('file')
    volume = sounds.get(body.sound).get('volume')
    source = discord.FFmpegPCMAudio(f'./sounds/{file_name}')
    
    for guild in bot.guilds:
        member = guild.get_member(body.user_id)
        if member:
            break
    
    if not member:
        return Response(content='No member found', status_code=status.HTTP_400_BAD_REQUEST)
        
    user_voice_channel = member.voice.channel
    if not user_voice_channel:
        return Response(content='No voice channel', status_code=status.HTTP_400_BAD_REQUEST)
    
    voice_client = None
    for client in bot.voice_clients:
        if client.channel == user_voice_channel:
            voice_client = client
            break

    if not voice_client:
        voice_client = await user_voice_channel.connect()

    try:
        voice_client.play(source)
        voice_client.source.volume = volume
    except errors.ClientException:
        voice_client.stop()
        voice_client.play(source)
        voice_client.source.volume = volume
    
    return Response(status_code=status.HTTP_200_OK)
    

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send('pong')
9

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


async def run():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(e)
