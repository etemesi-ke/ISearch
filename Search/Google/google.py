#!/usr/bin/python3

import urllib.parse

import bs4
import requests

GOOGLE = "https://www.google.com/"


def get_request(request):
    url = parse_url(request)
    return requests.get(url).content


def parse_url(url):
    abc = "search?q="
    url = urllib.parse.urljoin(GOOGLE, abc + url)
    return url


class Search():
    def __init__(self, query, ln="en", images=False, pages=1):
        self.query = query
        self.lang = ln
        self.images = images
        self.pages = pages
        self.search()

    def search(self):
        """
        Search Google :)
        Did not find a good enough module so i did what I do best
        (Hopefully better than cooking)
        Made my own :) :)
        Happy non-api Googleing
        """
        results = []

        qry_rslt = get_request(self.query)
        soup_parser = bs4.BeautifulSoup(qry_rslt, "lxml")
        for soup in soup_parser.find_all("div", atts={"id": "search"}):
            pass
        print(results)


Search("Hello")
