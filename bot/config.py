from __future__ import annotations

import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from package.settings import BOT_TOKEN, GPT_TOKEN
from package.read_messages import read_messages
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from openai import AsyncOpenAI

logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('bot.log')

formatter = logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(Levelname)s] - %(name)s (%(filename)s).%(funcName)s(%(Lineno)d) - %(message)s"
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(file_handler)


storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(storage=storage)
bot_messages = read_messages("texts.json")
client = AsyncOpenAI(api_key=GPT_TOKEN)
scheduler = AsyncIOScheduler()
