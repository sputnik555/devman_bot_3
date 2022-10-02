import logging
import random

import vk_api
from environs import Env
from google.cloud import dialogflow
from telegram import Bot
from vk_api.longpoll import VkLongPoll, VkEventType

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class LogsHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)

    def __init__(self, logger_chat_id, chat_id):
        logging.Handler.__init__(self)
        self.chat_id = chat_id
        self.bot = Bot(logger_chat_id)


def reply(event, vk_api, google_project_name):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(google_project_name, event.user_id)
    text_input = dialogflow.TextInput(text=event.text, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if response.query_result.intent.is_fallback:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=response.query_result.fulfillment_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')
    google_project_name = env.str('GOOGLE_PROJECT_NAME')
    tg_loger_token = env.str('TELEGRAM_LOGGER_TOKEN')
    logger_chat_id = env('TG_LOGGER_CHAT_ID')
    logger.addHandler(LogsHandler(tg_loger_token, logger_chat_id))

    vk_session = vk_api.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply(event, vk_api, google_project_name)
    except Exception as err:
        logger.exception(err)
