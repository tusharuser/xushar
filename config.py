import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
API_ID_KEY = Config.API_ID
API_HASH_KEY = Config.API_HASH
STRING_SESSION = Config.STRING_SESSION
MONGO_DB_URL = Config.MONGO_DB_URL
SIBYL = Config.SIBYL
ENFORCERS = Config.ENFORCERS
INSPECTORS = Config.INSPECTORS
Sibyl_logs = Config.Sibyl_logs
Sibyl_approved_logs = Config.Sibyl_approved_logs
GBAN_MSG_LOGS = Config.GBAN_MSG_LOGS
BOT_TOKEN = Config.BOT_TOKEN
