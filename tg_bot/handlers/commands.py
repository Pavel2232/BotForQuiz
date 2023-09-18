import random
from aiogram.types import Message
import textwrap
from config.config import redis, QUIZ_DICT
from keyboards.reply import get_quiz_keyboard
from utils.utils import get_questions, get_random_question


async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, я бот для викторины!", reply_markup=get_quiz_keyboard())


async def get_new_question_handler(message: Message) -> None:
    question = get_random_question(get_questions(QUIZ_DICT))
    redis.set(message.from_user.id, question)
    await message.answer(text=f'{question}')


async def check_answer_handler(message: Message) -> None:
    answer = get_questions(QUIZ_DICT).get(f'{redis.get(message.from_user.id)}')
    if message.text != answer:
        await message.answer('Неправильно… Попробуешь ещё раз?')
    else:
        await message.answer('Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
                             reply_markup=get_quiz_keyboard())


async def conversation_handler(message: Message) -> None:
    full_answer = get_questions(QUIZ_DICT).get(f'{redis.get(message.from_user.id)}')
    await message.answer(text=textwrap.dedent(f'''
        Правильный ответ: {full_answer}
        Для следующего вопроса нажми «Новый вопрос»'''),
                         reply_markup=get_quiz_keyboard())
