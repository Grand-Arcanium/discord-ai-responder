"""
A file/library containing misc helper functions.

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@author Mauricio Canul, Mohawk College, Mar 2024
@version 2.0
"""
import json


def get_json(filename: str) -> dict:
    """
    Read json data from a file.
    :param filename: name of the file
    :return: the data as a dict
    """
    f = open(filename, 'r')
    data = dict(json.load(f))
    f.close()
    return data


def update_json(filename: str, update: dict):
    """
    Write to a json file.
    :param filename: name of the file
    :param update: a dict containing json data
    """
    w = open(filename, 'w')
    json.dump(update, w)
    w.close()


def create_json_file(filename: str):
    """
    Create a json file if it doesn't exist
    :param filename: name of the file
    """
    with open(filename, 'w'):
        pass  # don't write anything
