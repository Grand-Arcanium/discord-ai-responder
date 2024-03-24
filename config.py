"""
This file contains the bot's tokens and the way to import it into the program.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@version 1.0
"""


def read_token(filename: str):
    """
    Reads a token stored in a .txt file. Make sure to add the file as part of .gitignore before commit/use.

    @param filename name of the file
    @return token as a string
    """
    our = ""
    with open(filename, 'r') as file:
        out = file.read().strip()

    return out


bot_token = read_token("discord_token.txt")  # put file name containing discord token here

gpt_token = read_token("gpt_token.txt")  # put file name of containing token here


def get_discord_token():
    """
    Function to retrieve a Discord App token for use.

    @return (string): the token
    """
    return bot_token


def get_gpt_token():
    """
    Function to retrieve an OpenAI token for use.

    @return (string): the token
    """
    return gpt_token

