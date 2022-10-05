import logging

from telegram import Bot


class LogsHandler(logging.Handler):

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)

    def __init__(self, logger_chat_id, chat_id):
        logging.Handler.__init__(self)
        self.chat_id = chat_id
        self.bot = Bot(logger_chat_id)
