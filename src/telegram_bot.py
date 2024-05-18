from datetime import datetime

import telegram
from telegram import TextQuote
from telegram.helpers import escape_markdown

from src.conf import TG_TOKEN, TG_CHAT_ID

bot = telegram.Bot(TG_TOKEN)


async def send_sms_message(sender: str, time: datetime, text: str):
    text_block = 'Сообщение от `' + escape_markdown(sender, version=2) + time.strftime("` %d числа в %H:%M:\n\n")
    lines = escape_markdown(text, version=2).split("\n")
    text_block = text_block + '\n'.join("> " + line for line in lines)
    async with bot:
        await bot.send_message(
            chat_id=TG_CHAT_ID,
            text=text_block,
            parse_mode="MarkdownV2"
        )


async def send_message(text: str):
    async with bot:
        await bot.send_message(
            chat_id=TG_CHAT_ID,
            text=text
        )
