import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from core.handlers.basic import router
from core.settings import BOT_TOKEN
from core.utils.commands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)


async def stop_bot(bot: Bot):
    pass


async def main() -> None:
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.include_routers(router)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
        stream=sys.stdout
    )
    asyncio.run(main())
