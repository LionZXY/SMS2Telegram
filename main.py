import asyncio

from src.sim868_pwrkey import  check_and_enable_gsm_module
from src.telegram_bot import send_message


async def main():
    await send_message("Бот запущен")
    await check_and_enable_gsm_module()


if __name__ == '__main__':
    print("Start")
    asyncio.run(main())
