import time
import os
from helper import *

# Session time in seconds
SESSION_TIME = 600

# max history
MAX_HISTORY = 10

# file name for saving server dialogues
DIALOGUES = "server_dialogues.json"


def time_formatter(my_time):
    """
    Used to format a given datetime UTC value into unix mktime,
    for logic, storage, and comparison purposes
    :param my_time: UTC datetime obj to be parsed
    :return: float representing time in seconds since the UNIX epoch
    """
    time_unix = time.mktime(my_time.timetuple())
    return str(time_unix)


def compare_time(current_time, saved_time):
    """
    Function made to make a boolean evaluation to check
    whether a time difference between the current time and
    the saved time is greater than the maximum time allowed
    for a session with the bot
    :param current_time: the current time as a unix time value
    :param saved_time: the saved time as a unix time value
    :return: True if the difference between the two time values is greater than or equal to the maximum session time
    """
    global SESSION_TIME
    try:
        val_cur = float(current_time)
        val_prev = float(saved_time)
        if val_cur - val_prev >= SESSION_TIME:
            return True
        return False
    except ValueError:
        return False


def add_to_history(server_id, user_id, msg, msg_time):
    """
    Function used to add a new message to the conversation history
    of a user, it searches the JSON file for the server id, then the user id
    and once it has found the list of all messages from that user, it adds
    it into memory, if that would make it so there were 10 or more items
    it would then delete the oldest one, messages are deleted 10 minutes
    after the last message in the conversation has been sent
    :param server_id: Id of the server from which the message to be added comes
    :param user_id: Id of the user sending in the message
    :param msg: Content of the message
    :param msg_time: UTC datetime object representing at which time the message was sent
    :return: None
    """
    current_time = time_formatter(msg_time)

    data = get_json(DIALOGUES)  # read from file

    # getting each key if it exists, or add one if it doesn't
    server_data = data.setdefault(str(server_id), {})
    user_data = server_data.setdefault(str(user_id), {"history": [], "time": ""})

    # get time and history for a user
    user_history = user_data.get("history")
    user_time = user_data.get("time")

    if user_history:  # there's a history
        if compare_time(current_time, user_time):  # check if older than 10 mins
            user_history.clear()

        if len(user_history) >= MAX_HISTORY:  # history reached max capacity
            user_history.pop(0)

        # add to history
        user_history.append(msg)
        user_data.update({"history": user_history, "time": current_time})

    else:  # history is empty
        user_data.update({"history": [msg], "time": current_time})

    update_json(DIALOGUES, data)


def get_dialogue_history(server_id, user_id):
    """
    Function to retrieve the message history from a user in a given server
    based on the combination of the server and the user's Id's
    :param server_id: Id of the server we are consulting
    :param user_id: Id of the user whose history we are consulting
    :return: A list of up to 9 previous messages the user has sent
    """
    data = get_json(DIALOGUES)

    serverHistory = dict(data.get(str(server_id)))

    if not serverHistory.__contains__(str(user_id)):
        return []
    else:
        retVal = list(serverHistory.get(str(user_id)).get("history"))
        retVal.pop()

    return retVal


def create_server_memory(currentServers):
    """
    Function used at start up of the bot to do two things, to first create the required
    JSON file if not exists, and then to populate it with key pair values where the
    key is each server to which this bot has been associated with and the value is a
    dictionary to hold said discord server's data

    :param currentServers: a list of the current servers this bot is associated with
    :return: None
    """
    changeBool = False

    if not os.path.exists(DIALOGUES):  # create the file
        create_json_file(DIALOGUES)

    if os.path.getsize(DIALOGUES) == 0:  # file is empty
        data = {}
    else:
        data = get_json(DIALOGUES)

    for val in currentServers:
        if not data.__contains__(str(val.id)):
            data.update({str(val.id): {}})
            changeBool = True

    if changeBool:
        update_json(DIALOGUES, data)
