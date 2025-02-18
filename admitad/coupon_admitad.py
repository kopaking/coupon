import logging
import os
from pyrogram import Client
from dotenv import load_dotenv
import requests
import json
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

load_dotenv()

# telegram
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
allowed_user_id = os.getenv('ALLOWED_USER_ID')
channelid_global = os.getenv('CHANNELID_GLOBAL')
channelid_br = os.getenv('CHANNELID_BR')

# admitad
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
base64_header = os.getenv('BASE64_HEADER')
affiliate_id = os.getenv('AFFILIATE_ID')
w_id = os.getenv('W_ID')







