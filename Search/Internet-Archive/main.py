"""
Internet archive search download upload everything stuff
Thank you Jacob M.  Johnson for your beautiful API
"""

import internetarchive


def login(username, password):
    internetarchive.configure(username, password)


class Search:
    def __init__(self, query):
        self.query = query

    def search_ia(self):
        pass
