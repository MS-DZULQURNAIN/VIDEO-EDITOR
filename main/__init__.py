from telethon import TelegramClient
from decouple import config
import logging
import time

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# variables
API_ID = config("26915599", default=None, cast=int)
API_HASH = config("76438a4fa64f9e43b3921a204a79e000", default=None)
BOT_TOKEN = config("5897361812:AAEMTxJoGlGudtfchrL2mSNSmv7Y4ODu3kw", default=None)
BOT_UN = config("MsVideoEDITOR_bot", default=None)
AUTH_USERS = config("5463819478", default=None, cast=int)
LOG_CHANNEL = config("mylogpubmsdeploy", default=None)
LOG_ID = config("LOG_ID", default=None)
FORCESUB = config("FORCESUB", default=None)
FORCESUB_UN = config("FORCESUB_UN", default=None)
ACCESS_CHANNEL = config("ACCESS_CHANNEL", default=None)
MONGODB_URI = config("MONGODB_URI", default=None)

Drone = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN) 
