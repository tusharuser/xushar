import os
from os import getenv


if os.path.exists("local.env"):
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
