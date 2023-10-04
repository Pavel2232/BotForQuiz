import json
import logging
import os
import random
import sys
import textwrap
from pathlib import Path
import redis
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll

from keyboards.keyboard import get_start_keyboard


def get_question(event, vk_api, redis_db) -> None:
    with open(f'{Path(__file__).resolve().parent.parent.joinpath(os.getenv("QUIZ_DICT"))}', 'r', encoding='UTF-8') as f:
        question = random.choice(list(json.load(f).keys()))
    redis_db.set(event.user_id, question)
    vk_api.messages.send(
        peer_id=os.getenv('PEER_ID'),
        user_id=event.user_id,
        message=question,
        random_id=random.randint(1, 1000),
        keyboard=get_start_keyboard()
    )


def check_answer_handler(event, vk_api, redis_db) -> None:
    with open(f'{Path(__file__).resolve().parent.parent.joinpath(os.getenv("QUIZ_DICT"))}', 'r', encoding='UTF-8') as f:
        answer = json.load(f).get(redis_db.get(event.user_id))
    if event.text != answer:
        vk_api.messages.send(
            peer_id=os.getenv('PEER_ID'),
            user_id=event.user_id,
            message='Неправильно… Попробуешь ещё раз?',
            random_id=random.randint(1, 1000),
            keyboard=get_start_keyboard()
        )
    else:
        vk_api.messages.send(
            peer_id=os.getenv('PEER_ID'),
            user_id=event.user_id,
            message='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»',
            random_id=random.randint(1, 1000),
            keyboard=get_start_keyboard()
        )


def conversation_handler(event, vk_api, redis_db) -> None:
    with open(f'{Path(__file__).resolve().parent.parent.joinpath(os.getenv("QUIZ_DICT"))}', 'r', encoding='UTF-8') as f:
        full_answer = json.load(f).get(redis_db.get(event.user_id))
    vk_api.messages.send(
        peer_id=os.getenv('PEER_ID'),
        user_id=event.user_id,
        message=textwrap.dedent(f'''
        Правильный ответ: {full_answer}
        Для следующего вопроса нажми «Новый вопрос»'''),
        random_id=random.randint(1, 1000),
        keyboard=get_start_keyboard()
    )


if __name__ == "__main__":
    load_dotenv(Path(__file__).resolve().parent.parent.joinpath('.env'))
    pool = redis.ConnectionPool(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')), db=0,
                                decode_responses=True)
    redis_db = redis.Redis(connection_pool=pool)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        stream=sys.stdout
                        )

    vk_session = vk.VkApi(token=os.getenv('VK_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logging.info('Бот запущен')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Новый вопрос':
                get_question(event, vk_api, redis_db)
            elif event.text == 'Сдаться':
                conversation_handler(event, vk_api, redis_db)
            else:
                check_answer_handler(event, vk_api, redis_db)
