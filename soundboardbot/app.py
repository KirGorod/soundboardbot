import asyncio
import discord
from fastapi import FastAPI, Response, status
from discord import errors

from soundboardbot.bot import bot
from soundboardbot.constants import TOKEN, PlaySound, sounds

app = FastAPI()
bot = bot


async def run():
    try:
        await bot.start(TOKEN)
    except Exception as e:
        print(e)
        
        
def play_sound(voice_client, source, volume):
    try:
        voice_client.play(source)
        voice_client.source.volume = volume
    except errors.ClientException as e:
        print(e)
        voice_client.stop()
        voice_client.play(source)
        voice_client.source.volume = volume


@app.on_event('startup')
async def startup():
    asyncio.create_task(run())


@app.post('/')
async def play_sound_cmd(body: PlaySound):
    try:
        user = bot.get_user(body.user_id)
    except Exception as e:
        print(e)
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
    if not body.sound:
        return

    file_name = sounds.get(body.sound).get('file')
    if file_name is None:
        return Response(content='No sound found', status_code=status.HTTP_400_BAD_REQUEST)

    volume = sounds.get(body.sound).get('volume')
    source = discord.FFmpegPCMAudio(f'./sounds/{file_name}')
    source = discord.PCMVolumeTransformer(source)
    source.volume = volume
    
    for guild in user.mutual_guilds:
        for channel in guild.voice_channels:
            for channel_member in channel.members:
                if channel_member.id == user.id:
                    member = channel_member
                    break

    if not member:
        return Response(content='No member found', status_code=status.HTTP_400_BAD_REQUEST)
        
    if member.voice:
        user_voice_channel = member.voice.channel
    else:
        return Response(content='Member not found in any channel', status_code=status.HTTP_400_BAD_REQUEST)
  
    voice_client = None
    if not bot.voice_clients:
        voice_client = await user_voice_channel.connect()

    try:
        voice_client = await user_voice_channel.connect()
        play_sound(voice_client, source, volume)
    except errors.ClientException as e:
        print(e)
        for client in bot.voice_clients:
            if client.guild == member.guild:
                voice_client = client
                break

        if voice_client.channel != user_voice_channel:
            await voice_client.disconnect()
            await user_voice_channel.connect()
        play_sound(voice_client, source, volume)
            
    return Response(status_code=status.HTTP_200_OK)
