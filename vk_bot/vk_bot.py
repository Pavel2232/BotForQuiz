import logging

from vk_api.longpoll import VkEventType
from settings import longpoll, vk_api

if __name__ == "__main__":
    from handlers.commands import get_question, check_answer_handler, conversation_handler

    logging.getLogger('BotVK')
    logging.info('Бот запущен')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Новый вопрос':
                get_question(event, vk_api)
            elif event.text == 'Сдаться':
                conversation_handler(event, vk_api)
            elif event.text == 'Мой счёт':
                pass
            else:
                check_answer_handler(event, vk_api)
