import logging
from telegram import Bot


class BotLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def configure_telegram_log_bot(logger, telegram_token, chat_id):
    bot = Bot(token=telegram_token)
    format_log = '%(levelname)-8s [%(asctime)s]  %(message)s'
    bot_handler = BotLogsHandler(bot, chat_id=chat_id)
    formatter = logging.Formatter(format_log)
    bot_handler.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(bot_handler)
