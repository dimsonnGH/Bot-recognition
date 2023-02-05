from dotenv import load_dotenv
import os
import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from dialog_flow import detect_intent_text


load_dotenv()
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")


def echo(event, vk_api):
    session_id = event.user_id
    text = event.text
    language_code = "ru"
    google_response = detect_intent_text(GOOGLE_PROJECT_ID, session_id, text, language_code)
    if google_response['is_fallback']:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=google_response['text'],
        random_id=random.randint(1,1000)
    )


def main():
    load_dotenv()
    VK_API_KEY = os.getenv("VK_API_KEY")

    vk_session = vk.VkApi(token=VK_API_KEY)

    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)




if __name__ == "__main__":
    main()