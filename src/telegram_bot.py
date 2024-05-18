
import telegram

from src.conf import TG_TOKEN, TG_CHAT_ID

bot = telegram.Bot(TG_TOKEN)

async def send_message(text: str):
    async with bot:
        await bot.send_message(
            chat_id=TG_CHAT_ID,
            text=text
        )
