import logging
import sys

from vk_api.longpoll import VkLongPoll
import vk_api as vk

from config import env

logger = logging.getLogger('BotVK')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout
                    )

vk_session = vk.VkApi(token=env('VK_BOT_TOKEN'))
vk_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)