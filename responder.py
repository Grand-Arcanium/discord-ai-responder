"""
This is the script for the bot to send prompts and parse responses from Chat GPT.
This can be run as a standalone program or as part of a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""
import json
import time
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
    Prepare the prompt and the message to send, it does this via a specialized System prompt that tells the
    API to first detect the tone, relevancy score and reasoning for said score (and the question being asked)
    of the user's utterance, this being our 1st API call

    :param utterance: the user's message
    :param history: the history of messages
    :return: dialog containing system + assistant prompts and user message
    """
    # ok so I decided to base the first call on whether something is on or off-topic
    # so this "understand" should be about passing a call, and getting back a score depending
    # on how on or off-topic the statement is.
    # this score is passed on to generate, where we pass the history and current utterance
    # for the real response/answer
    # but this time there is a value for score that the AI will consider when making a response
    # low score = off-topic = acknowledge but do not ans and redirect back
    # high score = on-topic = ans normally
    # middle = answer briefly ish, but mainly redirect it back

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
    Send the intent JSON to the AI and get a response based on the score, a tuned System prompt and
    the relevant training prompts being used to better direct it, our second API call

    :param intent: dialog containing content to be sent to the model
    :param history: the dialog history with the user up until now (last 10 messages)
    :param utterance: the latest message from the user
    :return: the content of the response
    """

    # from understand, get the score, tone and reasoning, based on utterance and user history
    topic_prompt = create_conversation(history, utterance, "topic_prompts.json", "responding")
    # then prep it by including it into the current dialog and utterance...
    topic_prompt = tune_dialog(topic_prompt, intent, "topic_prompts.json")
    # and send it with the new system prompt found in base_prompts
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
