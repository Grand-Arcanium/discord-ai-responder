"""
This is the script for the bot to send prompts and parse responses from Chat GPT.
This can be run as a standalone program or as part of a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 2.2
"""

import datetime
import data_handler
import openai

from config import get_gpt_token
from chat import *
from openai import OpenAI

my_api_key = get_gpt_token()  # get token
client = OpenAI(api_key=my_api_key)

MAX_TOKEN = 200  # max tokens to receive from ai

api_error = False

def understand(utterance: str, history: list):
    """
    Prepare the prompt and the message to send. It does this via a specialized System prompt that tells the
    API to first detect the tone, relevancy score and reasoning for said score (and the question being asked)
    of the user's utterance. This is the 1st API call, and its values will be passed to the 2nd API Call to
    process the actual user utterance

    :param utterance: the user's message
    :param history: the history of messages
    :return: dialog containing system + assistant prompts and user message
    """

    # check if currently being run on console
    is_console = __name__ == "__main__"

    # get the system prompt for relevance (is it on or off-topic)
    topic_prompt = create_conversation(history, utterance, "understanding")

    global api_error
    api_error = False

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo-1106", messages=topic_prompt,
                                              response_format={"type": "json_object"}, temperature=0,
                                              max_tokens=MAX_TOKEN, stop="\n")
    except openai.error.Timeout as e:
        response = json_error(e)

    except openai.APIError as e:
        response = json_error(e)

    except openai.RateLimitError as e:
        response = json_error(e)

    # other errors are not covered in this assignment as it is assumed that the token/authentication is valid

    # result should be in json with the proper keys
    if api_error:
        response_json = response
    else:
        response_json = eval(response.choices[0].message.content)

    # low score = off-topic = acknowledge but do not ans and redirect back
    # high score = on-topic = ans normally
    # middle = answer briefly-ish, but mainly redirect it to topic
    if not is_console:
        print(response_json)

    return response_json

def json_error(e):
    """
    Prepare error in the same format as the 1st API call response.
    :param e: the error from OpenAPI
    :return: a formatted json
    """
    global api_error
    api_error = True

    response_json = {
        "score": 0,
        "tone": "default"
    }

    error_message = "Unfortunately, there has been an error and you couldn't\
         analyze the user's statement. The error code was: " + e.message + ".\
         Do not address the user's statement, and instead, apologize to the " + \
         "user for being unable to reply, but do not mention the specific error."

    response_json.update({"explanation" : error_message})  # add to response

    return response_json


def generate(intent: str, utterance: str, history: list):
    """
    Send the intent JSON to the AI and get a response based on the score, a tuned System prompt and
    the relevant training prompts being used to better direct it, our second API call

    :param intent: dialog containing content to be sent to the model
    :param history: the dialog history with the user up until now (last 10 messages)
    :param utterance: the latest message from the user
    :return: the content of the response
    """

    # check if currently being run on console
    is_console = __name__ == "__main__"

    # reset error
    api_error = False

    # from understand, get the score, tone and reasoning, based on utterance and user history
    topic_prompt = create_conversation(history, utterance, "responding")
    # then prep it by including it into the current dialog and utterance...
    topic_prompt = tune_dialog(topic_prompt, intent)
    # and send it with the second system prompt found in prompt file

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=topic_prompt, temperature=0,
                                              max_tokens=MAX_TOKEN, stop="\n")
    except openai.error.Timeout as e:
        response = "Sorry, I cannot process your statement at this moment. Can you please repeat it?"
        api_error = True
        if not is_console:
            print(f"OpenAPI AI has encountered an error: {e}")

    except openai.APIError as e:
        response = "Sorry, I cannot process your statement at this moment. Can you please repeat it?"
        api_error = True
        if not is_console:
            print(f"OpenAPI AI has encountered an error: {e}")

    except openai.RateLimitError as e:
        response = "Sorry, I cannot process your statement at this moment. Can you please repeat it?"
        api_error = True
        if not is_console:
            print(f"OpenAPI AI has encountered an error: {e}")

    if api_error:
        return response
    else:
        return response.choices[0].message.content


## Main Function

def main():
    """
    Implements a chat session in the shell.
    """
    print("Hello! My name is Brisbane, your friendly coding assistant!\nWhen you're done talking, just say 'goodbye'.")
    print()

    # create a dummy obj as a substitute for an object containing a server id
    class Object(object):
        pass

    obj = Object()
    obj.id = "1"

    data_handler.create_server_memory([obj])  # prepare the history

    while True:
        utterance = input(">>> ")

        # add user input to history
        data_handler.add_to_history(1, "user", utterance, datetime.datetime.utcnow())
        history = data_handler.get_dialogue_history(1, "user")

        if utterance.lower() == "goodbye":  # exit
            break
        else:  # create a response
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
