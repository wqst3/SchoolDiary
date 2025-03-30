from dotenv import load_dotenv
from os import getenv
from aiogram import Bot, Dispatcher

load_dotenv()

token = (getenv("BOT_TOKEN_API"))

bot = Bot(token)
dp = Dispatcher()
