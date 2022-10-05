import logging

from environs import Env
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from df_response import get_dialogflow_response
from log_handler import LogsHandler

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def reply(update: Update, context: CallbackContext) -> None:
    response = get_dialogflow_response(
        context.bot_data.get('google_project_name'),
        update.message.text,
        update.message.chat_id
    )
    if response:
        update.message.reply_text(response.query_result.fulfillment_text)


def main() -> None:
    env = Env()
    env.read_env()
    google_project_name = env.str('GOOGLE_PROJECT_NAME')
    tg_token = env.str('TELEGRAM_TOKEN')
    tg_loger_token = env.str('TELEGRAM_LOGGER_TOKEN')
    logger_chat_id = env('TG_LOGGER_CHAT_ID')
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )
    logger.addHandler(LogsHandler(tg_loger_token, logger_chat_id))
    while True:
        try:
            updater = Updater(tg_token)
            dispatcher = updater.dispatcher
            dispatcher.bot_data['google_project_name'] = google_project_name
            dispatcher.add_handler(CommandHandler("start", start))
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply))
            updater.start_polling()
            updater.idle()
        except Exception as err:
            logger.exception(err)


if __name__ == '__main__':
    main()
