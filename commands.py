from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_default_commands(bot: Bot):
    return await bot.set_my_commands(
        commands=[
            BotCommand("user_stat", "Общая статистика пользователя"),
            BotCommand("org_stat", "Cтатистика по репозиториям организации"),
            BotCommand("bot_stat", "Статистика, которую собирает бот"),
            BotCommand("repos_stat", "Список репозиториев организации или пользователя")
        ],
        scope=BotCommandScopeDefault()
    )