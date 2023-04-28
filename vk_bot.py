import logging
from dotenv import load_dotenv
import os
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import detect_intent_text
from telegram_logging import init_telegram_log_bot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def send_response(event, vk_api, google_project_id):
    session_id = event.user_id
    text = event.text
    language_code = "ru"
    google_response = detect_intent_text(google_project_id, session_id, text, language_code)
    if google_response['is_fallback']:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=google_response['text'],
        random_id=random.randint(1, 1000)
    )


def main():
    load_dotenv()

    google_project_id = os.getenv("GOOGLE_PROJECT_ID")
    VK_API_KEY = os.getenv("VK_API_KEY")
    vk_session = vk.VkApi(token=VK_API_KEY)
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

    init_telegram_log_bot(logger, TELEGRAM_TOKEN, CHAT_ID)

    logger.info('VK bot started')

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_response(event, vk_api, google_project_id)


if __name__ == "__main__":
    main()
