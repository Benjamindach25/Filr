from pyrogram import Client, filters
from info import CHANNELS
from database.ia_filterdb import save_file
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

media_filter = filters.document | filters.video | filters.audio

@Client.on_message(filters.chat(CHANNELS) & media_filter)
async def media(bot, message):
    """Media Handler"""
    try:
        for file_type in ("document", "video", "audio"):
            media = getattr(message, file_type, None)
            if media is not None:
                break
        else:
            logging.warning("No media found in the message.")
            return

        media.file_type = file_type
        media.caption = message.caption
        await save_file(media)
        logging.info(f"File saved: {media.file_type} with caption: {media.caption}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

