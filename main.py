import asyncio
from threading import Thread

from src.sim868_cmd import check_unread_message, setup_module
from src.sim868_cmd_queue import receive_cmd_loop, request_check_message_event
from src.sim868_pwrkey import check_and_enable_gsm_module
from src.telegram_bot import send_message


async def main():
    await send_message("Бот запущен")
    await check_and_enable_gsm_module()
    receive_thread = Thread(target=receive_cmd_loop, args=[])
    receive_thread.start()
    try:
        await setup_module()
        await check_unread_message()
    except Exception as error:
        await send_message("Failed setup module because " + str(error))
        raise error
    while True:
        print("Waiting for messages...")
        request_check_message_event.wait(timeout=10)
        await check_unread_message()
        request_check_message_event.clear()


if __name__ == '__main__':
    print("Start")
    asyncio.run(main())
