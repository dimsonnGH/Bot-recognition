import logging
from dotenv import load_dotenv
import os
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import detect_intent_text
from telegram_logging import configure_telegram_log_bot

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
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    load_dotenv()

    google_project_id = os.getenv("GOOGLE_PROJECT_ID")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    vk_api_key = os.getenv("VK_API_KEY")
    vk_session = vk.VkApi(token=vk_api_key)

    configure_telegram_log_bot(logger, telegram_token, chat_id)

    logger.info('VK bot started')

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            send_response(event, vk_api, google_project_id)


if __name__ == "__main__":
    main()
