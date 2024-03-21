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

spacy.cli.download("en_core_web_md")
nlp = spacy.load("en_core_web_md")
matcher = Matcher(nlp.vocab)

