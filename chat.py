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


def create_conversation(history, utterance, filename, target=""):
    """
    Reads a file containing prompt data, then prepares the history into proper prompt form to be appended

    :return: list containing all the prompts
    """
    dialog = get_json(filename)
    if target != "" and dict(dialog).__contains__(target):
        dialog = dialog.get(target)

    for statement in history:
        dialog.append({"role": "user", "content": statement})

    dialog.append({"role": "user", "content": utterance})

    return dialog


def tune_dialog(dialog: list, json_val: dict, filename: str):
    tunningString = dialog[0]["content"]

    file = get_json(filename)

    if file.__contains__("score"):
        scoreArr = file.get("score")
        score = json_val.get("score")
        if score <= len(scoreArr) and not score < 0:
            tunningString += scoreArr[score]
        else:
            tunningString += scoreArr[0]
    if file.__contains__("tone"):
        toneObj = dict(file.get("tone"))
        tone = json_val.get("tone")
        if toneObj.__contains__(tone):
            tunningString += toneObj.get(tone)
        else:
            tunningString += toneObj.get("default")

    tunningString += "You have also figured out that " + json_val.get("explanation") \
                     + " and you may respond accordingly"
    print("finalized string:", tunningString)
    dialog[0]["content"] = tunningString
    print("in dialog:", dialog)
    return dialog


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
