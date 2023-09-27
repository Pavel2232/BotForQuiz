import random
import textwrap

from environs import Env

from config.db import redis, QUIZ_DICT
from utils.work_wtih_questions import get_random_question, get_questions
from keyboards.keyboard import get_start_keyboard

env = Env()
Env.read_env('env')

def get_question(event, vk_api) -> None:
    question = get_random_question(get_questions(QUIZ_DICT))
    redis.set(event.user_id, question)
    vk_api.messages.send(
        peer_id=env('PEER_ID'),
        user_id=event.user_id,
        message=question,
        random_id=random.randint(1, 1000),
        keyboard=get_start_keyboard()
    )


def check_answer_handler(event, vk_api) -> None:
    answer = get_questions(QUIZ_DICT).get(redis.get(event.user_id))
    if event.text != answer:
        vk_api.messages.send(
            peer_id=env('PEER_ID'),
            user_id=event.user_id,
            message='Неправильно… Попробуешь ещё раз?',
            random_id=random.randint(1, 1000),
            keyboard=get_start_keyboard()
        )
    else:
        vk_api.messages.send(
            peer_id=env('PEER_ID'),
            user_id=event.user_id,
            message='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
            random_id=random.randint(1, 1000),
            keyboard=get_start_keyboard()
        )


def conversation_handler(event, vk_api) -> None:
    full_answer = get_questions(QUIZ_DICT).get(redis.get(event.user_id))
    vk_api.messages.send(
        peer_id=env('PEER_ID'),
        user_id=event.user_id,
        message=textwrap.dedent(f'''
        Правильный ответ: {full_answer}
        Для следующего вопроса нажми «Новый вопрос»'''),
        random_id=random.randint(1, 1000),
        keyboard=get_start_keyboard()
    )
