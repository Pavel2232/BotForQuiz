import logging
import sys
import vk_api as vk
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll
from handlers.commands import get_question, check_answer_handler, conversation_handler

if __name__ == "__main__":
    env = Env()
    env.read_env('.env')

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        stream=sys.stdout
                        )

    vk_session = vk.VkApi(token=env('VK_BOT_TOKEN'))
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logging.getLogger('BotVK')
    logging.info('Бот запущен')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Новый вопрос':
                get_question(event, vk_api)
            elif event.text == 'Сдаться':
                conversation_handler(event, vk_api)
            else:
                check_answer_handler(event, vk_api)
