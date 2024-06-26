import time
import os
from helper import *

#Session time in seconds
SESSION_TIME = 600

# max history
MAX_HISTORY = 10

# file name for saving server dialogues
DIALOGUES = "server_dialogues.json"


def time_formatter(myTime):
    timeUnix = time.mktime(myTime.timetuple())
    return str(timeUnix)


def compare_time(currentTime, savedTime):
    global SESSION_TIME
    try:
        valCurrent = float(currentTime)
        valPrev = float(savedTime)
        if valCurrent - valPrev >= SESSION_TIME:
            return True
        return False
    except ValueError:
        return False


def add_to_history(serverId, userId, msg, time):
    current_time = time_formatter(time)

    data = get_json(DIALOGUES)  # read from file

    # getting each key if it exists, or add one if it doesn't
    server_data = data.setdefault(str(serverId), {})

    user_data = server_data.setdefault(str(userId), {"history": [], "time": ""})
    user_history = user_data.get("history")
    user_time = user_data.get("time")

    if user_history:  # there's a history
        if compare_time(current_time, user_time):  # check if older than 10mins
            user_history.clear()

        if len(user_history) >= MAX_HISTORY:  # history reached max capacity
            user_history.pop(0)

        # add to history
        user_history.append(msg)
        user_data.update({"history": user_history, "time": current_time})

    else:  # history is empty
        user_data.update({"history": [msg], "time": current_time})

    update_json(DIALOGUES, data)


def get_dialogue_history(serverId, userId):
    data = get_json(DIALOGUES)

    serverHistory = dict(data.get(str(serverId)))

    if not serverHistory.__contains__(str(userId)):
        return []
    else:
        retVal = list(serverHistory.get(str(userId)).get("history"))

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
