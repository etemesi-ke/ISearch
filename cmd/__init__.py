#!/usr/bin/python3
"""
Command line interface for Groove
"""

import multiprocessing as mp
import os

import Search.DuckDuckGo.duck as duck
import Search.Google.google as google

if os.name == "posix":
    class Colors:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERL = '\033[4m'
        ENDC = '\033[0m'
        backBlack = '\033[40m'
        backRed = '\033[41m'
        backGreen = '\033[42m'
        backYellow = '\033[43m'
        backBlue = '\033[44m'
        backMagenta = '\033[45m'
        backCyan = '\033[46m'
        backWhite = '\033[47m'

        def disable(self):
            self.PURPLE = ''
            self.CYAN = ''
            self.BLUE = ''
            self.GREEN = ''
            self.YELLOW = ''
            self.RED = ''
            self.ENDC = ''
            self.BOLD = ''
            self.UNDERL = ''
            self.backBlack = ''
            self.backRed = ''
            self.backGreen = ''
            self.backYellow = ''
            self.backBlue = ''
            self.backMagenta = ''
            self.backCyan = ''
            self.backWhite = ''
            self.DARKCYAN = ''

    # if we are windows or something like that then define colors as nothing
else:
    class Colors:
        PURPLE = ''
        CYAN = ''
        DARKCYAN = ''
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        BOLD = ''
        UNDERL = ''
        ENDC = ''
        backBlack = ''
        backRed = ''
        backGreen = ''
        backYellow = ''
        backBlue = ''
        backMagenta = ''
        backCyan = ''
        backWhite = ''

        def disable(self):
            self.PURPLE = ''
            self.CYAN = ''
            self.BLUE = ''
            self.GREEN = ''
            self.YELLOW = ''
            self.RED = ''
            self.ENDC = ''
            self.BOLD = ''
            self.UNDERL = ''
            self.backBlack = ''
            self.backRed = ''
            self.backGreen = ''
            self.backYellow = ''
            self.backBlue = ''
            self.backMagenta = ''
            self.backCyan = ''
            self.backWhite = ''
            self.DARKCYAN = ''


def query_prompt():
    prompt = Colors.YELLOW + "Query to search >>> " + Colors.ENDC
    query = input(prompt)
    return query


def option_prompt():
    """
    Function to get options for the user's preferred  engines o search with
    :return: A list containing those options
    """
    options = {
        "1": "google",
        "2": "duck",
    }

    google_ = Colors.RED + Colors.BOLD + "1. Google\n" + Colors.ENDC
    duck_ = Colors.GREEN + Colors.BOLD + "2. Duck Duck Go\n" + Colors.ENDC
    print(google_ + duck_)
    question = input(Colors.RED + "Input any number between 1-2 or 'all' to select all options or specific numbers "
                                  "separated with spaces\n>>> "
                     + Colors.ENDC)
    if " " in question:
        # There is  more than one option
        choice = []
        for opt in question.split(" "):
            try:
                choice.append(options.__getitem__(opt))
            except KeyError:
                print(Colors.backRed + Colors.BOLD + "Input values between 1 and 2" + Colors.ENDC)
                option_prompt()
    elif question.startswith("all"):
        choice = options.values()
    else:
        if not question.isdigit():
            print(Colors.backRed + Colors.BOLD + "Input values between 1 and 2" + Colors.ENDC)
            option_prompt()
        choice = []
        if int(question) > 2:
            print(Colors.backRed + Colors.BOLD + "Input values between 1 and 2" + Colors.ENDC)
        else:
            try:
                choice.append(options.__getitem__(question))
            except KeyError:
                print(Colors.backRed + Colors.BOLD + "Input values between 1 and 2" + Colors.ENDC)
                option_prompt()
    return choice


def _handle_calls(opts, query):
    for opt in opts:
        mp.Process(target=generate_cmd_output, args=(opt, query)).start()


def generate_cmd_output(opt, query):
    """
    Generate a command line formatted output of the results from the search
    :param opt:The search engines to use
    :param query: Query to search
    """
    modules = {
        "google": google,
        "duck": duck
    }
    every_thing = ""
    data = modules.get(opt).Search(query).parse_source()
    for elements in data:
        title = Colors.RED + Colors.BOLD + elements[0] + Colors.ENDC
        link = "\t" + Colors.BLUE + Colors.UNDERL + elements[1] + Colors.ENDC
        text = "\n\t" + Colors.GREEN + elements[2] + Colors.ENDC
        every_thing = every_thing + title + link + text
    print(every_thing)


def run():
    print(Colors.PURPLE + Colors.BOLD + Colors.UNDERL
          + "GROOVE COMMAND LINE" + Colors.ENDC)
    query = query_prompt()
    option = option_prompt()
    _handle_calls(option, query)
