import logging
import os
from pyrogram import Client
from dotenv import load_dotenv
import asyncio

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

load_dotenv()

# telegram
api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')

class TelegramBot:
    def __init__(self):
        self.api_id = api_id
        self.api_hash = api_hash
        self.bot_token = bot_token
        self.bot = None

    async def start_bot(self):
        self.bot = Client(
            "bot", api_id=int(api_id), api_hash=api_hash, bot_token=bot_token
            )
        await self.bot.start()

    async def send_message(self, chat_id, caption):
        if self.bot is None:
            await self.start_bot()
        await self.bot.send_message(chat_id=(chat_id), text=caption)
        await asyncio.sleep(60)

    async def get_entity(self, user_id):
        if self.bot is None:
            await self.start_bot()
        return await self.bot.get_users(user_id)
    