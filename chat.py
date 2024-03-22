"""
This contains the flow of of the chat as a script that the bot uses to remember context and prepare prompts.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 1.0
"""

MAX_CONTEXT = 10  # max number of items in context, as to keep token costs low

def get_context():
    """
    Get the context of the conversation thus far.
    :return:
    """


def add_context(context):
    """
    Append a new line to the context.
    If adding a line would make the context grow larger than MAX_CONTEXT,
    this will dequeue the oldest context in favor of the newest.

    :param context: add context from user input

    """

def get_prompt():
    """
    Prepare prompts to setup bot

    TODO able to switch from the built one and ones loaded from the file
    :return:
    """

