from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Початок роботи",
        ),
        BotCommand(
            command="report",
            description="Сформувати звіт"
        ),
        BotCommand(
            command="cancel",
            description="Відмінити дію"
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
