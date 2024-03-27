"""
This contains the flow of of the chat as a script that the bot uses to remember context and prepare prompts.

TODO ok so i wanted to separate the functions so i can format only the history, or only the current utterance, etc.
    that way when we have to modify the current utterance separately from the history, it is possible
@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""
from helper import get_json

CONVO_FILE = "topic_prompts.json"
SYSTEM_FILE = "base_prompts.json"
MAX_CONTEXT = 10  # max number of items in context, as to keep token costs low


def create_conversation(history, utterance, filename):
    """
    Reads a file containing prompt data, then prepares the history into proper prompt form to be appended

    :return: list containing all the prompts
    """

    convo = create_system_prompts(filename)

    dialog = [convo]

    for statement in history:
        dialog.append({"role": "user", "content": statement})

    dialog.append({"role": "user", "content": utterance})

    return dialog

def create_system_prompts(filename):
    prompts = get_json(filename)

    return prompts

def prepare_history(history):
    """
    Prepare the history into proper prompt format

    :param history:
    :return:
    """
    dialog = []

    for statement in history:
        dialog.append({"role": "user", "content": statement})
    return dialog
