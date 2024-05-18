import asyncio
from threading import Thread

from src.sim868_cmd import check_unread_message
from src.sim868_cmd_queue import receive_cmd_loop
from src.sim868_pwrkey import check_and_enable_gsm_module
from src.telegram_bot import send_message


async def main():
    await send_message("Бот запущен")
    await check_and_enable_gsm_module()
    receive_thread = Thread(target=receive_cmd_loop, args=[])
    receive_thread.start()
    await check_unread_message()
    receive_thread.join()


if __name__ == '__main__':
    print("Start")
    asyncio.run(main())
