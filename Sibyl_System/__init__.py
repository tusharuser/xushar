"""Gets ENV vars or Config vars then calls class."""
from telethon import events
import aiohttp
from telethon.sessions import StringSession
import os
from motor import motor_asyncio
import re
import asyncio


ENV = bool(os.environ.get('ENV', False))
if ENV:
    API_ID_KEY = int(os.environ.get('API_ID_KEY', None))
    API_HASH_KEY = os.environ.get('API_HASH_KEY', None)
    STRING_SESSION = os.environ.get('STRING_SESSION', None)
    HEROKU_API_KEY = os.environ.get('HEROKU_API_KEY', None)
    HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME', None)
    RAW_SIBYL = os.environ.get("SIBYL", "")
    RAW_ENFORCERS = os.environ.get("ENFORCERS", "")
    SIBYL = list(int(x) for x in os.environ.get("SIBYL", "").split())
    INSPECTORS = list(int(x) for x in os.environ.get("INSPECTORS", "").split())
    ENFORCERS = list(int(x) for x in os.environ.get("ENFORCERS", "").split())
    MONGO_DB_URL = os.environ.get('MONGO_DB_URL')
    Sibyl_logs = int(os.environ.get('Sibyl_logs', None))
    Sibyl_approved_logs = int(os.environ.get('Sibyl_Approved_Logs', None))
    GBAN_MSG_LOGS = int(os.environ.get('GBAN_MSG_LOGS', None))
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
else:
    import config as Config
    API_ID_KEY = Config.API_ID_KEY
    API_HASH_KEY = Config.API_HASH_KEY
    STRING_SESSION = Config.STRING_SESSION
    MONGO_DB_URL = Config.MONGO_DB_URL
    SIBYL = Config.SIBYL
    ENFORCERS = Config.ENFORCERS
    INSPECTORS = Config.INSPECTORS
    Sibyl_logs = Config.Sibyl_logs
    Sibyl_approved_logs = Config.Sibyl_approved_logs
    GBAN_MSG_LOGS = Config.GBAN_MSG_LOGS
    BOT_TOKEN = Config.BOT_TOKEN

INSPECTORS.extend(SIBYL)
ENFORCERS.extend(INSPECTORS)

session = aiohttp.ClientSession()

MONGO_CLIENT = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)

from .client_class import SibylClient
System = SibylClient(
    StringSession(STRING_SESSION),
    API_ID_KEY,
    API_HASH_KEY)

collection = MONGO_CLIENT['Sibyl']['Main']

async def make_collections() -> str:
    if await collection.count_documents({'_id': 1}, limit=1) == 0:
        dictw = {"_id": 1}
        dictw["blacklisted"] = []
        await collection.insert_one(dictw)

    if await collection.count_documents({'_id': 2}, limit=1) == 0:
        dictw = {"_id": 2, "Type": "Wlc Blacklist"}
        dictw["blacklisted_wlc"] = []
        await collection.insert_one(dictw)
    if await collection.count_documents({'_id': 3}, limit=1) == 0:
        dictw = {"_id": 3, "Type": "Gban:List"}
        dictw["victim"] = []
        dictw["gbanners"] = []
        dictw["reason"] = []
        dictw["proof_id"] = []
        await collection.insert_one(dictw)
    return ""

def system_cmd(pattern=None, allow_sibyl=True,
               allow_enforcer=False, allow_inspectors = False, allow_slash=True, force_reply = False, **args):
    if pattern and allow_slash:
        args["pattern"] = re.compile(r"[\?\.!/]" + pattern)
    else:
        args["pattern"] = re.compile(r"[\?\.!]" + pattern)
    if allow_sibyl and allow_enforcer:
        args["from_users"] = ENFORCERS
    elif allow_inspectors and allow_sibyl:
        args["from_users"] = INSPECTORS
    else:
        args["from_users"] = SIBYL
    if force_reply:
        args["func"] = lambda e: True if e.message.reply_to_msg_id else False
    return events.NewMessage(**args)
