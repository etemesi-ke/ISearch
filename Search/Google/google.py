#!/usr/bin/python3

"""
Main Module for Google  Scraping
"""

# Google have a way of making scrapers NOT scrap their pages
# (Yet they scrap ours)
# So am scraping the scrapers
# Using their scrapers
# Hahahahaha (Evil maniac laugh)


import logging
import os
import urllib.parse

GOOGLE = "https://www.google.com/"
GOOGLE_ADV = "https://www.google.com/advanced_search"
GOOGLE_IMG = "https://image.google.com/"
GOOGLE_VID = "https://video.google.com"


def _build_url(absolute, rel):
    """:param absolute: Absolute part of the url"
        :param rel: Relative part of the url
    """
    return urllib.parse.urljoin(absolute, rel)


def _return_country_url(country):
    """
    Inline function to return a google url with a country code domain
    :param country_code:
    :return:A google custom url with a domain name
    If the domain name doesn't exist send a warning and revert to global url
    """
    main = "https://www.google"
    with open(os.getcwd() + "/country.txt") as codes:
        for code in codes.readlines():
            # This is a waste of CPU time if there is a way of improving it
            # Help will highly be appreciated
            if country in code:
                code = (code.split(":"))[1].strip("\n")
                return main + code
            else:
                continue
        else:
            # If it all fails
            logging.warning("Country code for '%s' not found, reverting to global" % country)
            return GOOGLE


def _replace_spaces_with_plus(string):
    return string.replace(" ", "+")


class Search():
    def __init__(self, query, lang="en", country="worldwide", intitle=None, inurl=None, site=None, filetype=None,
                 link=None, cache=None, info=None, stock=None):
        """
        This is the topmost module for Google Search

        ---------------------------------------------------------------
        :param query:
        :param lang:Language to get the results in
        :param country: Get country specific results or worldwide(.com)
        --------------------------------------------------------------------
        Advanced Google terms
        ---------------------------------------------------------------------
        :param intitle Search for pages with specific titles
        :param inurl: Search for pages with specific urls
        :param site: Search only in a specific site
        :param filetype: Search for a specific type of file
        :param link: Search for pages linking ot other pages
        :param info: Information about a certain site
        :param stock: Search about stock info
        """
        self.query = _replace_spaces_with_plus(query)
        self.lang = "&ln=" + lang
        if not country == "worldwide":
            base = _build_url(_return_country_url(country), "/search")
        else:
            base = _build_url(GOOGLE, "")
        extra = _replace_spaces_with_plus(query)
        if intitle:
            extra = extra + _replace_spaces_with_plus("+intitle:" + intitle)
        if inurl:
            extra = extra + _replace_spaces_with_plus("+inurl:" + inurl)
        if site:
            extra = extra + _replace_spaces_with_plus("+site:" + site)
        if filetype:
            extra = extra + _replace_spaces_with_plus("+filetype:" + filetype)
        if link:
            extra = extra + _replace_spaces_with_plus("+link:" + link)
        if cache:
            extra = extra + _replace_spaces_with_plus("+cache:" + cache)
        if info:
            extra = extra + _replace_spaces_with_plus("+info:" + info)
        if stock:
            extra = extra + _replace_spaces_with_plus("+stock:" + stock)
        url = self.build_query(base, extra)

    def build_query(self, base, params):
        """
        Build a google query and ensure it is parsed correctly
        :param params: Parameters fo the query
        :param base : Base url
        :return: a full google url with the query
        """
        form = "?q=" + self.query + params + self.lang
        print(base + form)
        return base + form
