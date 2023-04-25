import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dialog_flow import detect_intent_text
from telegram_logging import init_telegram_log_bot

load_dotenv()
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")

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


def send_response(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    session_id = update.message.chat_id
    text = update.message.text
    language_code = "ru"
    google_response = detect_intent_text(GOOGLE_PROJECT_ID, session_id, text, language_code)
    update.message.reply_text(google_response['text'])


def main() -> None:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    init_telegram_log_bot(logger, TELEGRAM_TOKEN, CHAT_ID)

    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, send_response))

    # log all errors
    dispatcher.add_error_handler(log_error)

    # Start the Bot
    updater.start_polling()

    logger.info('Telegram bot started')

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
