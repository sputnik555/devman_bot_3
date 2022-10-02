import logging

from environs import Env
from google.cloud import dialogflow
from telegram import Update, ForceReply, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

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


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext) -> None:
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(google_project_name, update.message.chat_id)
    text_input = dialogflow.TextInput(text=update.message.text, language_code='ru')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    update.message.reply_text(response.query_result.fulfillment_text)


def main() -> None:
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    google_project_name = env.str('GOOGLE_PROJECT_NAME')
    tg_token = env.str('TELEGRAM_TOKEN')
    tg_loger_token = env.str('TELEGRAM_LOGGER_TOKEN')
    logger_chat_id = env('TG_LOGGER_CHAT_ID')
    logger.addHandler(LogsHandler(tg_loger_token, logger_chat_id))
    while True:
        try:
            main()
        except Exception as err:
            logger.exception(err)
