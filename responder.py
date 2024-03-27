"""
This is the script for the bot to send prompts and parse responses from Chat GPT.
This can be run as a standalone program or as part of a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""
import json

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
    # ok so i decided to base the first call on whether something is on or off topic
    # so this "understand" should be about passing a call, and getting back a score depending
    # on how on or off topic the statement is.
    # this score is passed on to generate, where we pass the history and current utterance
    # for the real response/answer
    # but this time there is a value for score that the ai will consider when making a response
    # low score = off-topic = acknowledge but dont ans and redirect bacl
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


def generate(intent, history, utterance):
    """
    Send the intent to the AI and get a response

    :param intent: dialog containing content to be sent to the model
    :return: the content of the response
    """

    # from understand, get the score and then include it into the current utterance
    # then prep it and send it with the new system prompt found in base_prompts
    # TODO get the new system prompt via base_prompts this time, append the score for the latest one
    #   mention in system prompt about the score found inbetween something like <score>
    #   unless send json? kinda annoying tho
    #   get back plain text

    topic_prompt = create_conversation(history, utterance, "topic_prompts.json", "responding")

    topic_prompt = tune_dialog(topic_prompt, intent, "topic_prompts.json")

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=topic_prompt, temperature=0,
                                              max_tokens=MAX_TOKEN)

    return response.choices[0].message.content


## Main Function

def main():
    """
    Implements a chat session in the shell.
    TODO match discord's chat implementation

    """
    print("Hello! My name is Brisbane!\nWhen you're done talking, just say 'goodbye'.")
    print()

    utterance = ""
    while True:
        utterance = input(">>> ")

        if utterance == "goodbye":
            break
        else:
            intent = understand(utterance)
            response = generate(intent)
        print(response)
        print()


## Run as a standalone module

if __name__ == "__main__":
    """
    If statement checks whether or not this module is being run as a standalone module. 
    If it is being imported, the if condition will be false and it will not run the chat method.
    """
    main()
