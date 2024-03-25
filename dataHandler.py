import json
import time


def time_formatter(myTime):
    timeUnix = time.mktime(myTime.timetuple())
    return str(timeUnix)


def compare_time(currentTime, savedTime):
    try:
        valCurrent = float(currentTime)
        valPrev = float(savedTime)
        if valCurrent - valPrev >= 600:
            return True
        return False
    except ValueError:
        return False


def get_json():
    f = open("serverDialogues.json", 'r')
    myJson = dict(json.load(f))
    f.close()
    return myJson


def update_json(update):
    w = open("serverDialogues.json", 'w')
    json.dump(update, w)
    w.close()


def add_to_history(serverId, userId, msg, time):
    current_time = time_formatter(time)

    data = get_json()

    serverHistory = dict(data.get(str(serverId)))

    if not serverHistory.__contains__(str(userId)):
        data.get(str(serverId)).update({str(userId): {"history": [msg], "time": current_time}})
    else:
        userEntry = serverHistory.get(str(userId))
        if len(userEntry.get("history")) >= 10:
            data.get(str(serverId)).get(str(userId)).get("history").pop(0)
        if compare_time(current_time, userEntry.get("time")):
            data.get(str(serverId)).get(str(userId)).get("history").clear()
        data.get(str(serverId)).get(str(userId)).get("history").append(msg)
        data.get(str(serverId)).get(str(userId)).update({"time": current_time})

    update_json(data)


def get_dialogue_history(serverId, userId):
    data = get_json()

    serverHistory = dict(data.get(str(serverId)))

    if not serverHistory.__contains__(str(userId)):
        return []
    else:
        retVal = list(serverHistory.get(str(userId)).get("history"))
        if len(retVal) > 0:
            retVal.pop()

    return retVal


def create_server_memory(currentServers):
    changeBool = False

    data = get_json()

    for val in currentServers:
        if not data.__contains__(str(val.id)):
            data.update({str(val.id): {}})
            changeBool = True

    if changeBool:
        update_json(data)
