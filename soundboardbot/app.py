import asyncio
import discord
from fastapi import FastAPI, Response, status
from discord import errors

from soundboardbot.bot import bot
from soundboardbot.constants import TOKEN, PlaySound, sounds

app = FastAPI()


async def run():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(e)

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
    source = discord.PCMVolumeTransformer(source)
    source.volume = volume
    
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
