import asyncio
import logging
import sys
from handlers.commands import command_start_handler, get_new_question_handler, check_answer_handler, \
    conversation_handler
from aiogram.filters import CommandStart
from aiogram import F, Dispatcher, Bot
from environs import Env


async def main() -> None:
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(get_new_question_handler, F.text == 'Новый вопрос')
    dp.message.register(conversation_handler, F.text == 'Сдаться')
    dp.message.register(check_answer_handler)
    await dp.start_polling(bot)


if __name__ == "__main__":
    env = Env()
    env.read_env('.env')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        stream=sys.stdout
                        )

    dp = Dispatcher()
    bot = Bot(env("TG_BOT_TOKEN"))

    # pool = redis.ConnectionPool(host=env('REDIS_HOST'), port=env('REDIS_PORT'), db=0, decode_responses=True)
    # redis = redis.Redis(connection_pool=pool)
    asyncio.run(main())
