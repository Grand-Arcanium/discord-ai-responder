"""
This is the script for the bot to send prompts and parse responses from Chat GPT.
This can be run as a standalone program or as part of a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""

from config import get_gpt_token
import openai
from openai import OpenAI

my_api_key = get_gpt_token()  # get token
client = OpenAI(api_key=my_api_key)


def understand(utterance):
    """
    Prepare the prompt and the message to send
    TODO include role:assistant for prompt engineering, and include past conversation here
        also move this to chat as part of chat flow + adjust prompts easier + testing? generate can stay here tho

    :param utterance: the user's message
    :return: dialog containing system + assistant prompts and user message
    """

    prompt = "Conversation"  # todo get prompt from chat.py?

    dialog = [
        {"role": "system",
         "content": prompt},
        {"role": "user", "content": utterance}
    ]

    return dialog


def generate(intent):
    """
    Send the intent to the AI and get a response

    TODO allow easy change of temp and fix max tokens

    :param intent: dialog containing content to be sent to Chat GPT
    :return: the content of the response
    """

    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=intent, temperature=0, max_tokens=64)
    print(response)
    return response.choices[0].message.content


## Main Function

def main():
    """
    Implements a chat session in the shell.

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
