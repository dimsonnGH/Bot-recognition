import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dialog_flow import detect_intent_text
from telegram_logging import init_telegram_log_bot
from functools import partial

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def log_error(update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Здравствуйте, {user.full_name}.')


def send_response(update: Update, context: CallbackContext, google_project_id) -> None:
    """Echo the user message."""
    session_id = update.message.chat_id
    text = update.message.text
    language_code = "ru"
    google_response = detect_intent_text(google_project_id, session_id, text, language_code)
    update.message.reply_text(google_response['text'])


def main() -> None:
    load_dotenv()

    google_project_id = os.getenv("GOOGLE_PROJECT_ID")
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    init_telegram_log_bot(logger, TELEGRAM_TOKEN, CHAT_ID)

    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    send_response_from_google = partial(send_response, google_project_id=google_project_id)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_response_from_google))

    dispatcher.add_error_handler(log_error)

    updater.start_polling()

    logger.info('Telegram bot started')

    updater.idle()


if __name__ == '__main__':
    main()
