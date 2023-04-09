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
    'iwo': 'iwo.mp3',
    'horn': 'horn.mp3',
    'airhorn': 'airhorn.mp3'
}


@app.on_event('startup')
async def startup():
    asyncio.create_task(run())


@app.post('/')
async def play_sound(body: PlaySound):
    guild = bot.get_guild(body.guild_id)
    member = guild.get_member(body.user_id)
    if not body.sound:
        return
    source = discord.FFmpegPCMAudio(f'./sounds/{sounds.get(body.sound)}')
    
    if member.voice:
        if not bot.voice_clients:
            voice_client = await member.voice.channel.connect()
        for client in bot.voice_clients:
            if client.guild.id == guild.id:
                if client.channel != member.voice.channel:
                    await client.disconnect()
                    voice_client = await member.voice.channel.connect()
                else:
                    voice_client = client
                break

        try:
            voice_client.play(source)
        except errors.ClientException:
            voice_client.stop()
            voice_client.play(source)
        
        return Response(status_code=status.HTTP_200_OK)
    
    return Response(status_code=status.HTTP_400_BAD_REQUEST)


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


async def run():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(e)
