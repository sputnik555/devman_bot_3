import logging
import random

from environs import Env
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

from df_response import get_dialogflow_response
from log_handler import LogsHandler

logger = logging.getLogger(__name__)


def reply(event, vk_api, google_project_name):
    response = get_dialogflow_response(google_project_name, event.text, event.user_id)
    if response:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response.query_result.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def main():
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')
    google_project_name = env.str('GOOGLE_PROJECT_NAME')
    tg_loger_token = env.str('TELEGRAM_LOGGER_TOKEN')
    logger_chat_id = env('TG_LOGGER_CHAT_ID')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger.addHandler(LogsHandler(tg_loger_token, logger_chat_id))
    vk_session = VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply(event, vk_api, google_project_name)
    except Exception as err:
        logger.exception(err)


if __name__ == "__main__":
    main()
