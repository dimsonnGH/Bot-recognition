import os
import sys
import argparse
import json
import pathlib
from pprint import pprint
from dotenv import load_dotenv

def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    from google.cloud import dialogflow

    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print(f"Intent created: {display_name}")

def create_intents(intents):

    base_dir = os.path.dirname(__file__)
    dotenv_path = os.path.join(base_dir, 'venv\.env')
    load_dotenv(dotenv_path)
    GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")

    for display_name in intents:
        intent = intents[display_name]
        training_phrases_parts = intent['questions']
        message_texts = [intent['answer'],]
        create_intent(GOOGLE_PROJECT_ID, display_name, training_phrases_parts, message_texts)


def main():

    parser = argparse.ArgumentParser(description='Creating intents for DialogFlow')
    parser.add_argument('file_path', type=pathlib.Path, help='Intents json file path')
    args = parser.parse_args()

    json_file_path = args.file_path

    try:
        with open(json_file_path, 'r', encoding='utf-8') as intents_json_file:
            intents = json.load(intents_json_file)
            create_intents(intents)
    except FileNotFoundError as e:
        print(f'Define the file name in -f argument')
        sys.exit(1)

if __name__ == '__main__':
    main()
