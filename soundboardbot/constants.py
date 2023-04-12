import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()
TOKEN = os.getenv('TOKEN')


class PlaySound(BaseModel):
    user_id: int
    sound: str


sounds = {
    'iwo': {
        'file': 'iwo.mp3',
        'volume': 1.0
    },
    'horn': {
        'file': 'horn.mp3',
        'volume': 0.7    
    },
    'airhorn': {
        'file': 'airhorn.mp3',
        'volume': 0.1
    },
    'fbi': {
        'file': 'fbi.mp3',
        'volume': 1.0
    },
    'sensational': {
        'file': 'sensational.mp3',
        'volume': 1.0
    },
    'stupid': {
        'file': 'stupid.mp3',
        'volume': 0.8
    }
}
