import logging

from google.cloud import dialogflow
from telegram import Bot


class LogsHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)

    def __init__(self, logger_chat_id, chat_id):
        logging.Handler.__init__(self)
        self.chat_id = chat_id
        self.bot = Bot(logger_chat_id)


def get_dialogflow_response(google_project_name, message, chat_id):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(google_project_name, chat_id)
    text_input = dialogflow.TextInput(text=message, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    if not response.query_result.intent.is_fallback:
        return response
