from commands import set_default_commands
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage

GitParser = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(GitParser, storage=storage)

async def default_commands(bot: Bot):
    await set_default_commands(bot)

async def on_shutdown(dp):
    await GitParser.close()
    await storage.close()

async def on_startup(dp):
    await default_commands(GitParser)


if __name__ == '__main__':
    from handlers import dp
    from aiogram import executor

    executor.start_polling(dp, on_shutdown=on_shutdown)