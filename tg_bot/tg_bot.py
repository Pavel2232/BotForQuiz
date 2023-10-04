import redis
import asyncio
import json
import logging
import os
import random
import sys
import textwrap
from pathlib import Path
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram import F, Dispatcher, Bot
from dotenv import load_dotenv
from keyboards.reply import get_quiz_keyboard
from functools import partial


async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, я бот для викторины!", reply_markup=get_quiz_keyboard())


async def get_new_question_handler(message: Message, redis_db) -> None:
    with open(f'{Path(__file__).resolve().parent.parent.joinpath(os.getenv("QUIZ_DICT"))}', 'r', encoding='UTF-8') as f:
        question = random.choice(list(json.load(f).keys()))
    redis_db.set(message.from_user.id, question)
    await message.answer(text=question)


async def check_answer_handler(message: Message, redis_db) -> None:
    with open(f'{Path(__file__).resolve().parent.parent.joinpath(os.getenv("QUIZ_DICT"))}', 'r', encoding='UTF-8') as f:
        answer = json.load(f).get(redis_db.get(message.from_user.id))
    if message.text != answer:
        await message.answer('Неправильно… Попробуешь ещё раз?')
    else:
        await message.answer('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
                             reply_markup=get_quiz_keyboard())


async def conversation_handler(message: Message, redis_db) -> None:
    with open(f'{Path(__file__).resolve().parent.parent.joinpath(os.getenv("QUIZ_DICT"))}', 'r', encoding='UTF-8') as f:
        full_answer = json.load(f).get(redis_db.get(message.from_user.id))
    await message.answer(text=textwrap.dedent(f'''
        Правильный ответ: {full_answer}
        Для следующего вопроса нажми «Новый вопрос»'''),
                         reply_markup=get_quiz_keyboard())


if __name__ == "__main__":
    load_dotenv(Path(__file__).resolve().parent.parent.joinpath('.env'))

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        stream=sys.stdout
                        )
    pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=0,
                                decode_responses=True)
    redis_db = redis.Redis(connection_pool=pool)
    dp = Dispatcher()
    bot = Bot(os.getenv('TG_BOT_TOKEN'))
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(partial(get_new_question_handler, redis_db=redis_db), F.text == 'Новый вопрос')
    dp.message.register(partial(conversation_handler, redis_db=redis_db), F.text == 'Сдаться')
    dp.message.register(partial(check_answer_handler, redis_db=redis_db))
    asyncio.run(dp.start_polling(bot))
