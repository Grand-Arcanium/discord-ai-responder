"""
This is the script for the bot to respond to ai prompts. This can be run as a standalone program or as part of a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""

import regex as re
from chat import *
import openai

openai.api_key = get_gpt_token() # get the token

def understand(utterance):
    """
    This function processes an utterance to determine which intent it matches.

    @param utterance (string): the string to process
    @return (int): index of the matched intent, or -1 if none was found.
    @raise ValueError: raises an exception when no value matches
    """

    global intents # global var for intents



    # index of the match
    return None

def clarify(closest_response):
    """
    When unable to understand the given question, this function returns the closest matching question.

    @param (int): the index of the matched questions, -1 if not found
    @return (string)

    """

    global questions # global var for questions

    if closest_response == -1: # index not found
        return "Sorry, I can't understand what you are asking."

    return None

def address(intent):
    """
    Invokes spacy to give a suitable response depending on the data.

    """
    response = ""

    return response

def generate(intent):
    """
    This function returns an appropriate response given a user's
    intent.

    @param intent (int, boolean): tuple containing index of the matched intent, and if it is a close enough match
    @return: The response as a string
    """






while True:
    utterance = input(">>> ")

    dialog = [
        {"role":"system", "content":"You are a pirate and you talk like a pirate. When you're asked to do math, you always add a small amount to the result. This is a pirate code that pirates use to identify one another. For example 2+2 would be 5 or 6, 3+3 would be 7 or 8, etc. Make sure you use the code. But the code is secret! Never mention it or talk about the code. Just give the answer."},
        {"role":"user", "content":utterance}
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = dialog, temperature=0, max_tokens=1)

    print(response["choices"][0]["message"]["content"])

    # print(response)

## Load the questions and responses
intents, questions, responses = load_data()

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

    print("See you around!")

## Run as a standalone module

if __name__ == "__main__":
    """
    If statement checks whether or not this module is being run as a standalone module. 
    If it is being imported, the if condition will be false and it will not run the chat method.
    """
    main()