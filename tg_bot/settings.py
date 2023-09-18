import logging
import sys

from aiogram import Dispatcher, Bot

from config import env

logger = logging.getLogger('BotTG')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout
                    )
TOKEN = env("TG_BOT_TOKEN")

dp = Dispatcher()
bot = Bot(TOKEN)
