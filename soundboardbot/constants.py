import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
TOKEN = os.getenv('TOKEN')


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
        'volume': 0.7    
    },
    'airhorn': {
        'file': 'airhorn.mp3',
        'volume': 0.1
    }
}
