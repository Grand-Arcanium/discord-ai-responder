"""
This is the script for the bot to send prompts and parse responses from Chat GPT. This can be run as a standalone program or as part of a discord bot.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""

from config import get_gpt_token
from helper import *
import spacy
from spacy.matcher import Matcher

import openai

openai.api_key = get_gpt_token()

print("Arrr, I'm a pirate bot!")

while True:
    utterance = input(">>> ")

    dialog = [
        {"role":"system", "content":""}, # insert prompt here
        {"role":"user", "content":utterance} # user utterance
    ]

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = dialog, temperature=0, max_tokens=1)

    print(response["choices"][0]["message"]["content"])

    # print(response)