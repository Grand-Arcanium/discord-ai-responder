"""
This is the script for the bot to send prompts and parse responses from Chat GPT.
This can be run as a standalone program or as part of a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 2.0
"""

import datetime
import data_handler

from config import get_gpt_token
from chat import *
from openai import OpenAI

my_api_key = get_gpt_token()  # get token
client = OpenAI(api_key=my_api_key)

MAX_TOKEN = 200


def understand(utterance, history):
    """
    Prepare the prompt and the message to send

    :param utterance: the user's message
    :param history: the history of messages
    :return: dialog containing system + assistant prompts and user message
    """

    # get the system prompt for relevance (is it on or off-topic)
    topic_prompt = create_conversation(history, utterance, "topic_prompts.json", "understanding")

    response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=topic_prompt,
                                              response_format={"type": "json_object"}, temperature=0,
                                              max_tokens=MAX_TOKEN)

    # result should be in json with the proper keys
    response_json = eval(response.choices[0].message.content)

    print(response_json)

    return response_json


def generate(intent, utterance, history):
    """
    Send the intent and a history to the AI and get a response

    :param intent: dialog containing content to be sent to the model
    :return: the content of the response
    """

    topic_prompt = create_conversation(history, utterance, "topic_prompts.json", "responding")

    topic_prompt = tune_dialog(topic_prompt, intent, "topic_prompts.json")

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=topic_prompt, temperature=0,
                                              max_tokens=MAX_TOKEN)

    return response.choices[0].message.content


## Main Function

def main():
    """
    Implements a chat session in the shell.

    """
    print("Hello! My name is Brisbane!\nWhen you're done talking, just say 'goodbye'.")
    print()

    class Object(object):
        pass

    obj = Object()
    obj.id = "1"

    data_handler.create_server_memory([obj])

    utterance = ""
    while True:
        utterance = input(">>> ")

        data_handler.add_to_history(1, "user", utterance, datetime.datetime.utcnow())
        history = data_handler.get_dialogue_history(1, "user")

        if utterance == "goodbye":
            break
        else:
            intent = understand(utterance, history)
            response = generate(intent, utterance, history)
        print(response)
        print()


## Run as a standalone module

if __name__ == "__main__":
    """
    If statement checks whether or not this module is being run as a standalone module. 
    If it is being imported, the if condition will be false and it will not run the chat method.
    """
    main()
