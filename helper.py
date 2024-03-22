"""
A file/library containing misc helper functions.

TODO adjust to read test files, prompts etc

@author Mari Shenzhen Uy, Mohawk College, Mar 2024
@version 2.0
"""

def file_input(filename):
    """
    Loads each line of the file into a list and returns it.

    @param
    @return
    """
    lines = []
    with open(filename) as file:  # opens the file and assigns it to a variable
        for line in file:
            lines.append(line)  # the strip method removes extra whitespace
    return lines


def load_data():
    """
    This method returns a list of prompts and a list of corresponding answers

    @return questions: the data of the questions.txt file as a list
    @return answers: the data of the answers.txt file as a list
    """

    intent = list()

    # read file of intents line by line
    with open("intent.txt") as file:
        for line in file:
            line = r"" + line.strip() # remove trailing whitespace/newlines
            intent.append(line)

    questions = file_input("questions.txt")

    answers = file_input("answers.txt")

    return intent, questions, answers


