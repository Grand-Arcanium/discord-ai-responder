import time
import os
from helper import *

#Session time in seconds
SESSION_TIME = 600

# max history
MAX_HISTORY = 10

# file name for saving server dialogues
DIALOGUES = "server_dialogues.json"


def time_formatter(my_time):
    time_unix = time.mktime(my_time.timetuple())
    return str(time_unix)


def compare_time(current_time, saved_time):
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
    data = get_json(DIALOGUES)

    serverHistory = dict(data.get(str(server_id)))

    if not serverHistory.__contains__(str(user_id)):
        return []
    else:
        retVal = list(serverHistory.get(str(user_id)).get("history"))

    return retVal


def create_server_memory(currentServers):
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
