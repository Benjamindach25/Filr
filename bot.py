import logging
import logging.config
import datetime

# Configure logging based on your requirements (replace with actual logging setup)
logging.basicConfig(level=logging.INFO)

from pyrogram import Client, __version__
from plugins.clone import restart_bots
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from Script import script
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL
from utils import temp
from datetime import date, datetime
import pytz
from typing import Union, Optional, AsyncGenerator
from pyrogram import types

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))
        await restart_bots()
        logging.info(f"{me.first_name} with Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat sequentially.
        Refer to the official Pyrogram documentation for the most up-to-date usage.
        """
        # ... (implementation using get_messages)

# Assuming tobot is another instance of Bot
tobot = Bot()

apps = [tobot]
for ape in apps:
    ape.start()


app = Bot()
app.run()
